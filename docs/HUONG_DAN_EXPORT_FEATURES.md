# 📤 HƯỚNG DẪN: EXPORT FEATURES
## Xuất dữ liệu ra nhiều định dạng

### 🎯 **MỤC TIÊU**
Thêm tính năng xuất dữ liệu ra CSV, Excel, JSON cho user download.

### 📋 **YÊU CẦU KIẾN THỨC**
- ✅ Flask routing và response
- ✅ Pandas cơ bản (sẽ hướng dẫn)
- ✅ File handling
- ⚠️ **Không cần**: Complex data processing

### 🔧 **BƯỚC 1: Cài đặt thư viện cần thiết**

**Sửa file:** `config/requirements.txt`

Thêm vào cuối file:
```text
pandas==2.1.0
openpyxl==3.1.2
xlsxwriter==3.1.9
```

**Cài đặt thư viện:**
```bash
# Activate virtual environment
env\Scripts\activate

# Cài đặt thư viện mới
pip install pandas openpyxl xlsxwriter

# Hoặc cài từ requirements
pip install -r config\requirements.txt
```

### 🔧 **BƯỚC 2: Tạo Export Functions**

**Tạo file mới:** `src/export_handler.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Export Handler - Xuất dữ liệu ra nhiều định dạng
"""

import pandas as pd
import json
import io
import os
from datetime import datetime
from flask import Response, send_file
import pymssql

class ExportHandler:
    def __init__(self, config_reader):
        self.config_reader = config_reader
    
    def lay_du_lieu_bang(self, ten_bang, database_name=None, limit=None, where_clause=None, order='auto'):
        """
        Lấy dữ liệu từ bảng để export
        """
        try:
            config = self.config_reader()
            if database_name:
                config['database'] = database_name
            
            ket_noi = pymssql.connect(
                server=config['server'],
                port=config['port'],
                user=config['user'],
                password=config['password'],
                database=config['database']
            )
            
            # Xây dựng câu truy vấn
            if limit and limit != '0':
                limit_clause = f"TOP {limit}"
            else:
                limit_clause = ""
            
            # Xử lý ORDER BY
            if order == 'random':
                order_clause = "ORDER BY NEWID()"
            elif order == 'auto':
                order_clause = ""
            else:
                order_clause = ""
            
            # Xử lý WHERE
            if where_clause:
                where_sql = f"WHERE {where_clause}"
            else:
                where_sql = ""
            
            query = f"SELECT {limit_clause} * FROM [{ten_bang}] {where_sql} {order_clause}"
            
            # Sử dụng pandas để đọc dữ liệu
            df = pd.read_sql(query, ket_noi)
            ket_noi.close()
            
            return df
            
        except Exception as e:
            print(f"Lỗi lấy dữ liệu export: {e}")
            return None
    
    def export_csv(self, ten_bang, database_name=None, **kwargs):
        """
        Xuất dữ liệu ra CSV
        """
        try:
            df = self.lay_du_lieu_bang(ten_bang, database_name, **kwargs)
            if df is None:
                return None
            
            # Tạo CSV trong memory
            csv_buffer = io.StringIO()
            df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
            csv_content = csv_buffer.getvalue()
            csv_buffer.close()
            
            # Tạo response
            filename = f"{ten_bang}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            response = Response(
                csv_content,
                mimetype='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Type': 'text/csv; charset=utf-8'
                }
            )
            
            return response
            
        except Exception as e:
            print(f"Lỗi export CSV: {e}")
            return None
    
    def export_excel(self, ten_bang, database_name=None, **kwargs):
        """
        Xuất dữ liệu ra Excel với formatting
        """
        try:
            df = self.lay_du_lieu_bang(ten_bang, database_name, **kwargs)
            if df is None:
                return None
            
            # Tạo Excel trong memory
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                # Ghi dữ liệu vào sheet
                df.to_excel(writer, sheet_name='Data', index=False)
                
                # Lấy workbook và worksheet để formatting
                workbook = writer.book
                worksheet = writer.sheets['Data']
                
                # Format header
                header_format = workbook.add_format({
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'fg_color': '#3498db',
                    'font_color': 'white',
                    'border': 1
                })
                
                # Format data cells
                data_format = workbook.add_format({
                    'border': 1,
                    'text_wrap': True,
                    'valign': 'top'
                })
                
                # Apply formatting
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    # Auto-adjust column width
                    max_len = max(
                        df[value].astype(str).map(len).max(),
                        len(str(value))
                    )
                    worksheet.set_column(col_num, col_num, min(max_len + 2, 30))
                
                # Thêm info sheet
                info_df = pd.DataFrame({
                    'Thông tin': [
                        'Tên bảng',
                        'Database',
                        'Số dòng',
                        'Số cột',
                        'Ngày xuất',
                        'Thời gian xuất'
                    ],
                    'Giá trị': [
                        ten_bang,
                        database_name or 'default',
                        len(df),
                        len(df.columns),
                        datetime.now().strftime('%d/%m/%Y'),
                        datetime.now().strftime('%H:%M:%S')
                    ]
                })
                
                info_df.to_excel(writer, sheet_name='Info', index=False)
            
            excel_buffer.seek(0)
            
            # Tạo filename
            filename = f"{ten_bang}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            return send_file(
                excel_buffer,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        except Exception as e:
            print(f"Lỗi export Excel: {e}")
            return None
    
    def export_json(self, ten_bang, database_name=None, **kwargs):
        """
        Xuất dữ liệu ra JSON với metadata
        """
        try:
            df = self.lay_du_lieu_bang(ten_bang, database_name, **kwargs)
            if df is None:
                return None
            
            # Chuyển DataFrame thành dict
            data_dict = df.to_dict('records')
            
            # Tạo JSON structure với metadata
            export_data = {
                'metadata': {
                    'table_name': ten_bang,
                    'database': database_name or 'default',
                    'export_time': datetime.now().isoformat(),
                    'total_rows': len(df),
                    'total_columns': len(df.columns),
                    'columns': list(df.columns),
                    'data_types': df.dtypes.astype(str).to_dict()
                },
                'data': data_dict
            }
            
            # Serialize to JSON
            json_content = json.dumps(export_data, ensure_ascii=False, indent=2, default=str)
            
            # Tạo filename
            filename = f"{ten_bang}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            response = Response(
                json_content,
                mimetype='application/json',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Type': 'application/json; charset=utf-8'
                }
            )
            
            return response
            
        except Exception as e:
            print(f"Lỗi export JSON: {e}")
            return None
    
    def export_summary_report(self, ten_bang, database_name=None):
        """
        Tạo báo cáo tổng kết về dữ liệu (Excel với nhiều sheet)
        """
        try:
            df = self.lay_du_lieu_bang(ten_bang, database_name, limit='1000')
            if df is None:
                return None
            
            excel_buffer = io.BytesIO()
            
            with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
                # Sheet 1: Sample Data (100 dòng đầu)
                sample_df = df.head(100)
                sample_df.to_excel(writer, sheet_name='Sample Data', index=False)
                
                # Sheet 2: Data Summary
                summary_data = {
                    'Column': list(df.columns),
                    'Data Type': [df[col].dtype for col in df.columns],
                    'Null Count': [df[col].isnull().sum() for col in df.columns],
                    'Unique Count': [df[col].nunique() for col in df.columns],
                    'Sample Value': [df[col].iloc[0] if len(df) > 0 else '' for col in df.columns]
                }
                summary_df = pd.DataFrame(summary_data)
                summary_df.to_excel(writer, sheet_name='Data Summary', index=False)
                
                # Sheet 3: Statistics (cho numeric columns)
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    stats_df = df[numeric_cols].describe()
                    stats_df.to_excel(writer, sheet_name='Statistics')
                
                # Sheet 4: Info
                info_data = {
                    'Metric': [
                        'Table Name',
                        'Database',
                        'Total Rows',
                        'Total Columns',
                        'Numeric Columns',
                        'Text Columns',
                        'Date Columns',
                        'Export Time'
                    ],
                    'Value': [
                        ten_bang,
                        database_name or 'default',
                        len(df),
                        len(df.columns),
                        len(df.select_dtypes(include=['number']).columns),
                        len(df.select_dtypes(include=['object']).columns),
                        len(df.select_dtypes(include=['datetime']).columns),
                        datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    ]
                }
                info_df = pd.DataFrame(info_data)
                info_df.to_excel(writer, sheet_name='Report Info', index=False)
                
                # Format all sheets
                workbook = writer.book
                header_format = workbook.add_format({
                    'bold': True,
                    'fg_color': '#3498db',
                    'font_color': 'white',
                    'border': 1
                })
                
                for sheet_name in writer.sheets:
                    worksheet = writer.sheets[sheet_name]
                    worksheet.set_row(0, None, header_format)
            
            excel_buffer.seek(0)
            
            filename = f"{ten_bang}_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            
            return send_file(
                excel_buffer,
                as_attachment=True,
                download_name=filename,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            
        except Exception as e:
            print(f"Lỗi export summary report: {e}")
            return None
```

### 🔧 **BƯỚC 3: Thêm Export Routes vào Flask**

**Sửa file:** `src/tableau_universal_connector.py`

**Thêm import:**
```python
from export_handler import ExportHandler
```

**Thêm sau khai báo dashboard_gallery:**
```python
# Khởi tạo Export Handler
export_handler = ExportHandler(doc_cau_hinh_database)
```

**Thêm routes (trước route `if __name__ == '__main__':`:**

```python
@app.route('/export/<format>/<table_name>')
def export_data(format, table_name):
    """
    Export dữ liệu ra nhiều định dạng
    """
    database_name = request.args.get('database', None)
    limit = request.args.get('limit', '1000')
    where_clause = request.args.get('where', None)
    order = request.args.get('order', 'auto')
    
    export_params = {
        'limit': limit,
        'where_clause': where_clause,
        'order': order
    }
    
    try:
        if format.lower() == 'csv':
            result = export_handler.export_csv(table_name, database_name, **export_params)
        elif format.lower() == 'excel':
            result = export_handler.export_excel(table_name, database_name, **export_params)
        elif format.lower() == 'json':
            result = export_handler.export_json(table_name, database_name, **export_params)
        elif format.lower() == 'report':
            result = export_handler.export_summary_report(table_name, database_name)
        else:
            return jsonify({
                "success": False,
                "error": f"Định dạng '{format}' không được hỗ trợ. Hỗ trợ: csv, excel, json, report"
            }), 400
        
        if result is None:
            return jsonify({
                "success": False,
                "error": "Không thể export dữ liệu. Kiểm tra kết nối database và tên bảng."
            }), 500
        
        return result
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Lỗi export: {str(e)}"
        }), 500

@app.route('/api/export-options/<table_name>')
def get_export_options(table_name):
    """
    Lấy các tùy chọn export cho bảng
    """
    database_name = request.args.get('database', None)
    
    try:
        # Lấy sample data để estimate file size
        sample_df = export_handler.lay_du_lieu_bang(table_name, database_name, limit='10')
        if sample_df is None:
            return jsonify({
                "success": False,
                "error": "Không thể truy cập bảng dữ liệu"
            })
        
        # Get row count estimate
        config = doc_cau_hinh_database()
        if database_name:
            config['database'] = database_name
            
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        con_tro = ket_noi.cursor()
        con_tro.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        total_rows = con_tro.fetchone()[0]
        ket_noi.close()
        
        # Estimate file sizes (rough)
        estimated_csv_size = total_rows * len(sample_df.columns) * 10  # bytes
        estimated_excel_size = estimated_csv_size * 1.5
        estimated_json_size = estimated_csv_size * 2
        
        export_options = {
            "table_info": {
                "name": table_name,
                "database": database_name or 'default',
                "total_rows": total_rows,
                "columns": len(sample_df.columns),
                "column_names": list(sample_df.columns)
            },
            "formats": [
                {
                    "format": "csv",
                    "name": "CSV File",
                    "description": "Comma-separated values, mở được bằng Excel",
                    "estimated_size_mb": round(estimated_csv_size / 1024 / 1024, 2),
                    "recommended_for": "Excel analysis, data processing"
                },
                {
                    "format": "excel",
                    "name": "Excel File", 
                    "description": "Excel workbook với formatting và multiple sheets",
                    "estimated_size_mb": round(estimated_excel_size / 1024 / 1024, 2),
                    "recommended_for": "Business reports, presentations"
                },
                {
                    "format": "json",
                    "name": "JSON File",
                    "description": "JavaScript Object Notation với metadata",
                    "estimated_size_mb": round(estimated_json_size / 1024 / 1024, 2),
                    "recommended_for": "API integration, web development"
                },
                {
                    "format": "report",
                    "name": "Summary Report",
                    "description": "Excel report với statistics và data analysis",
                    "estimated_size_mb": round(estimated_excel_size * 0.7 / 1024 / 1024, 2),
                    "recommended_for": "Data exploration, quick insights"
                }
            ],
            "export_limits": [
                {"value": "100", "label": "100 dòng (Demo)"},
                {"value": "1000", "label": "1,000 dòng (Tiêu chuẩn)"}, 
                {"value": "5000", "label": "5,000 dòng (Lớn)"},
                {"value": "0", "label": "Tất cả dòng (Toàn bộ)"}
            ]
        }
        
        return jsonify({
            "success": True,
            "options": export_options
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
```

### 🔧 **BƯỚC 4: Thêm Export UI vào giao diện**

**Sửa template trong `TABLEAU_WDC_TEMPLATE`:**

**Thêm CSS (trong phần `<style>`):**
```css
.export-section {
    background: #f8f9fa;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    padding: 20px;
    margin-top: 20px;
}

.export-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 15px;
}

.export-btn {
    background: linear-gradient(45deg, #28a745, #20c997);
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 5px;
    font-size: 14px;
    cursor: pointer;
    transition: transform 0.2s;
    text-decoration: none;
    display: inline-block;
}

.export-btn:hover {
    transform: translateY(-2px);
}

.export-btn.csv { background: linear-gradient(45deg, #28a745, #20c997); }
.export-btn.excel { background: linear-gradient(45deg, #007bff, #0056b3); }
.export-btn.json { background: linear-gradient(45deg, #ffc107, #e0a800); }
.export-btn.report { background: linear-gradient(45deg, #6f42c1, #59359a); }

@media (max-width: 768px) {
    .export-buttons {
        flex-direction: column;
    }
    
    .export-btn {
        width: 100%;
        margin-bottom: 5px;
    }
}
```

**Thêm HTML export section (sau phần database-info):**
```html
<div class="export-section" id="exportSection" style="display: none;">
    <strong>📤 Xuất Dữ Liệu</strong>
    <p>Tải dữ liệu về máy tính của bạn với nhiều định dạng khác nhau:</p>
    
    <div class="export-buttons">
        <button type="button" class="export-btn csv" onclick="exportData('csv')">
            📊 Tải CSV
        </button>
        <button type="button" class="export-btn excel" onclick="exportData('excel')">
            📈 Tải Excel
        </button>
        <button type="button" class="export-btn json" onclick="exportData('json')">
            🔗 Tải JSON
        </button>
        <button type="button" class="export-btn report" onclick="exportData('report')">
            📋 Báo Cáo Tổng Kết
        </button>
    </div>
    
    <div id="exportStatus" style="margin-top: 10px; font-size: 14px;"></div>
</div>
```

**Thêm JavaScript (trong phần `<script>`):**

```javascript
// Global export functions
function showExportSection() {
    var database = document.getElementById('databaseSelect').value;
    var selectedTables = getSelectedTables();
    var exportSection = document.getElementById('exportSection');
    
    if (database && selectedTables.length > 0) {
        exportSection.style.display = 'block';
        loadExportOptions(selectedTables[0], database);
    } else {
        exportSection.style.display = 'none';
    }
}

function loadExportOptions(tableName, database) {
    var statusDiv = document.getElementById('exportStatus');
    statusDiv.innerHTML = '🔄 Đang tải thông tin export...';
    
    var apiUrl = `/api/export-options/${tableName}`;
    if (database) {
        apiUrl += `?database=${encodeURIComponent(database)}`;
    }
    
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var info = data.options.table_info;
                statusDiv.innerHTML = `
                    📊 <strong>${info.name}</strong> - ${info.total_rows.toLocaleString()} dòng, ${info.columns} cột<br>
                    💾 Ước tính kích thước file: CSV (~${data.options.formats[0].estimated_size_mb}MB), 
                    Excel (~${data.options.formats[1].estimated_size_mb}MB)
                `;
            } else {
                statusDiv.innerHTML = '⚠️ Không thể tải thông tin export: ' + (data.error || 'Unknown error');
            }
        })
        .catch(error => {
            statusDiv.innerHTML = '❌ Lỗi kết nối: ' + error.message;
        });
}

function exportData(format) {
    var database = document.getElementById('databaseSelect').value;
    var selectedTables = getSelectedTables();
    var limit = document.getElementById('limitSelect').value;
    var where = document.getElementById('whereInput').value;
    var order = document.getElementById('orderSelect').value;
    
    if (!database || selectedTables.length === 0) {
        alert('Vui lòng chọn database và bảng dữ liệu trước');
        return;
    }
    
    var tableName = selectedTables[0]; // Export bảng đầu tiên
    var statusDiv = document.getElementById('exportStatus');
    
    // Build export URL
    var exportUrl = `/export/${format}/${tableName}`;
    var params = [];
    
    if (database) params.push(`database=${encodeURIComponent(database)}`);
    if (limit) params.push(`limit=${encodeURIComponent(limit)}`);
    if (where) params.push(`where=${encodeURIComponent(where)}`);
    if (order) params.push(`order=${encodeURIComponent(order)}`);
    
    if (params.length > 0) {
        exportUrl += '?' + params.join('&');
    }
    
    // Show loading status
    statusDiv.innerHTML = `🔄 Đang xuất ${format.toUpperCase()}... Vui lòng đợi...`;
    
    // Create invisible download link
    var downloadLink = document.createElement('a');
    downloadLink.href = exportUrl;
    downloadLink.style.display = 'none';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
    
    // Update status after delay
    setTimeout(function() {
        statusDiv.innerHTML = `✅ Đã bắt đầu tải ${format.toUpperCase()}. Kiểm tra thư mục Downloads của bạn.`;
    }, 2000);
}

// Update existing event handlers
document.getElementById('databaseSelect').addEventListener('change', function() {
    var selectedDatabase = this.value;
    if (selectedDatabase) {
        loadTableList(selectedDatabase);
    } else {
        document.getElementById('tablesContainer').innerHTML = '<div style="color: #7f8c8d; font-style: italic;">Chọn database trước để hiển thị danh sách bảng...</div>';
        updateSelectedTablesCount();
        document.getElementById('exportSection').style.display = 'none';
    }
});

// Existing updateSelectedTablesCount function - modify to show export
function updateSelectedTablesCount() {
    var selectedCheckboxes = document.querySelectorAll('input[name="selectedTables"]:checked');
    var countElement = document.getElementById('selectedTablesCount');
    countElement.textContent = selectedCheckboxes.length;
    
    // Show/hide export section
    showExportSection();
    
    // Update "Chọn tất cả" checkbox state
    var selectAllCheckbox = document.getElementById('selectAllTables');
    var allCheckboxes = document.querySelectorAll('input[name="selectedTables"]');
    
    if (selectAllCheckbox && allCheckboxes.length > 0) {
        if (selectedCheckboxes.length === 0) {
            selectAllCheckbox.indeterminate = false;
            selectAllCheckbox.checked = false;
        } else if (selectedCheckboxes.length === allCheckboxes.length) {
            selectAllCheckbox.indeterminate = false;
            selectAllCheckbox.checked = true;
        } else {
            selectAllCheckbox.indeterminate = true;
            selectAllCheckbox.checked = false;
        }
    }
}
```

### 🧪 **BƯỚC 5: Test Export Features**

**Chạy server và test:**
```bash
python src\tableau_universal_connector.py
```

**URLs để test:**
- `http://127.0.0.1:5002` - Main page với export buttons
- `http://127.0.0.1:5002/export/csv/table_name?database=db_name&limit=100`
- `http://127.0.0.1:5002/api/export-options/table_name?database=db_name`

**Checklist test:**
- ✅ Export section hiển thị khi chọn bảng?
- ✅ CSV download hoạt động?
- ✅ Excel download với formatting?
- ✅ JSON download với metadata?
- ✅ Summary Report với multiple sheets?
- ✅ Export options API trả về đúng info?

### 🎨 **BƯỚC 6: Thêm Export History (Bonus)**

**Tạo file:** `scripts/tao_export_history.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo bảng lưu lịch sử export
"""

import sqlite3
from datetime import datetime

def tao_bang_export_history():
    ket_noi = sqlite3.connect('database/dashboard_gallery.db')
    con_tro = ket_noi.cursor()
    
    con_tro.execute('''
    CREATE TABLE IF NOT EXISTS export_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        table_name TEXT NOT NULL,
        database_name TEXT,
        export_format TEXT NOT NULL,
        export_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        file_size_bytes INTEGER,
        row_count INTEGER,
        status TEXT DEFAULT 'completed',
        download_count INTEGER DEFAULT 0
    )
    ''')
    
    ket_noi.commit()
    ket_noi.close()
    print("✅ Đã tạo bảng export_history")

if __name__ == '__main__':
    tao_bang_export_history()
```

### 🐛 **TROUBLESHOOTING**

**Lỗi thiếu pandas:**
```bash
pip install pandas openpyxl xlsxwriter
```

**File Excel bị lỗi:**
```python
# Check engine xlsxwriter có cài đúng không
pip list | grep xlsxwriter
```

**Download không hoạt động:**
- Kiểm tra browser block download
- Check antivirus software
- Test với file size nhỏ trước

**Memory error với file lớn:**
```python
# Sử dụng chunk processing cho file lớn
for chunk in pd.read_sql(query, connection, chunksize=1000):
    # Process chunk by chunk
```

### 🎉 **KẾT QUẢ MONG ĐỢI**

Sau khi hoàn thành:
- ✅ Export CSV với UTF-8 encoding
- ✅ Export Excel với formatting và multiple sheets
- ✅ Export JSON với metadata đầy đủ
- ✅ Summary Report với data analysis
- ✅ Export options API với file size estimates
- ✅ Mobile-friendly export interface
- ✅ Export history tracking (bonus)

### 📝 **COMMIT MESSAGE**
```bash
git add .
git commit -m "Thêm Export Features đầy đủ

- Export CSV, Excel, JSON, Summary Report
- Excel với formatting và multiple sheets
- JSON với metadata đầy đủ
- Export options API với file size estimates
- Mobile-responsive export interface
- Pandas integration cho data processing
- Export history tracking
- Error handling và user feedback"
```

### ➡️ **BƯỚC TIẾP THEO**
Hoàn thành rồi chuyển sang: `HUONG_DAN_USER_AUTHENTICATION.md`
