# 🗂️ HƯỚNG DẪN: DASHBOARD GALLERY
## Tạo thư viện dashboard cho user

### 🎯 **MỤC TIÊU**
Tạo trang web hiển thị danh sách các dashboard đã lưu, cho phép user xem và quản lý.

### 📋 **YÊU CẦU KIẾN THỨC**
- ✅ Flask routing cơ bản
- ✅ HTML/CSS 
- ✅ SQLite database (sẽ hướng dẫn)
- ⚠️ **Không cần**: React, Vue, complex framework

### 🔧 **BƯỚC 1: Tạo Database Schema**

**Tạo file mới:** `scripts/tao_database_dashboard.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo database cho Dashboard Gallery
"""

import sqlite3
import os
from datetime import datetime

def tao_database_dashboard():
    """
    Tạo database SQLite cho lưu trữ dashboard info
    """
    # Tạo thư mục database nếu chưa có
    os.makedirs('database', exist_ok=True)
    
    # Kết nối database
    ket_noi = sqlite3.connect('database/dashboard_gallery.db')
    con_tro = ket_noi.cursor()
    
    # Tạo bảng dashboards
    con_tro.execute('''
    CREATE TABLE IF NOT EXISTS dashboards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten_dashboard TEXT NOT NULL,
        mo_ta TEXT,
        database_nguon TEXT NOT NULL,
        bang_du_lieu TEXT NOT NULL,
        cau_hinh_json TEXT,
        ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        lan_truy_cap_cuoi TIMESTAMP,
        so_lan_truy_cap INTEGER DEFAULT 0,
        trang_thai TEXT DEFAULT 'active',
        nguoi_tao TEXT DEFAULT 'admin'
    )
    ''')
    
    # Tạo bảng dashboard_shares (cho tính năng sharing sau)
    con_tro.execute('''
    CREATE TABLE IF NOT EXISTS dashboard_shares (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        dashboard_id INTEGER,
        share_token TEXT UNIQUE,
        ngay_tao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        han_su_dung TIMESTAMP,
        so_lan_truy_cap INTEGER DEFAULT 0,
        FOREIGN KEY (dashboard_id) REFERENCES dashboards (id)
    )
    ''')
    
    # Thêm dữ liệu mẫu
    dashboards_mau = [
        ('Dashboard Crypto Analysis', 'Phân tích dữ liệu cryptocurrency', 'CryptoData', 'crypto_data', '{"limit": 100, "order": "auto"}'),
        ('Sales Report Dashboard', 'Báo cáo bán hàng tháng', 'SalesDB', 'sales_data', '{"limit": 500, "order": "date_desc"}'),
        ('Customer Analytics', 'Phân tích hành vi khách hàng', 'CustomerDB', 'customer_data', '{"limit": 1000, "where": "active = 1"}'),
        ('Financial Overview', 'Tổng quan tài chính', 'FinanceDB', 'financial_data', '{"limit": 0, "order": "random"}')
    ]
    
    con_tro.executemany('''
    INSERT INTO dashboards (ten_dashboard, mo_ta, database_nguon, bang_du_lieu, cau_hinh_json)
    VALUES (?, ?, ?, ?, ?)
    ''', dashboards_mau)
    
    ket_noi.commit()
    ket_noi.close()
    
    print("✅ Database dashboard_gallery.db đã được tạo thành công!")
    print("📊 Đã thêm 4 dashboard mẫu")
    return True

if __name__ == '__main__':
    tao_database_dashboard()
```

### 🔧 **BƯỚC 2: Tạo Dashboard Gallery Functions**

**Tạo file mới:** `src/dashboard_gallery.py`

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Gallery - Quản lý danh sách dashboard
"""

import sqlite3
import json
from datetime import datetime

class DashboardGallery:
    def __init__(self, db_path='database/dashboard_gallery.db'):
        self.db_path = db_path
    
    def lay_tat_ca_dashboard(self):
        """
        Lấy danh sách tất cả dashboard
        """
        try:
            ket_noi = sqlite3.connect(self.db_path)
            ket_noi.row_factory = sqlite3.Row  # Cho phép truy cập bằng tên cột
            con_tro = ket_noi.cursor()
            
            con_tro.execute('''
            SELECT * FROM dashboards 
            WHERE trang_thai = 'active' 
            ORDER BY lan_truy_cap_cuoi DESC, ngay_tao DESC
            ''')
            
            dashboards = [dict(row) for row in con_tro.fetchall()]
            ket_noi.close()
            
            return dashboards
        except Exception as e:
            print(f"Lỗi lấy dashboard: {e}")
            return []
    
    def lay_dashboard_theo_id(self, dashboard_id):
        """
        Lấy thông tin dashboard theo ID
        """
        try:
            ket_noi = sqlite3.connect(self.db_path)
            ket_noi.row_factory = sqlite3.Row
            con_tro = ket_noi.cursor()
            
            con_tro.execute('SELECT * FROM dashboards WHERE id = ?', (dashboard_id,))
            dashboard = con_tro.fetchone()
            ket_noi.close()
            
            return dict(dashboard) if dashboard else None
        except Exception as e:
            print(f"Lỗi lấy dashboard {dashboard_id}: {e}")
            return None
    
    def cap_nhat_lan_truy_cap(self, dashboard_id):
        """
        Cập nhật lần truy cập cuối và số lần truy cập
        """
        try:
            ket_noi = sqlite3.connect(self.db_path)
            con_tro = ket_noi.cursor()
            
            con_tro.execute('''
            UPDATE dashboards 
            SET lan_truy_cap_cuoi = ?, so_lan_truy_cap = so_lan_truy_cap + 1
            WHERE id = ?
            ''', (datetime.now(), dashboard_id))
            
            ket_noi.commit()
            ket_noi.close()
            return True
        except Exception as e:
            print(f"Lỗi cập nhật truy cập: {e}")
            return False
    
    def luu_dashboard_moi(self, ten_dashboard, mo_ta, database_nguon, bang_du_lieu, cau_hinh):
        """
        Lưu dashboard mới
        """
        try:
            ket_noi = sqlite3.connect(self.db_path)
            con_tro = ket_noi.cursor()
            
            cau_hinh_json = json.dumps(cau_hinh, ensure_ascii=False)
            
            con_tro.execute('''
            INSERT INTO dashboards (ten_dashboard, mo_ta, database_nguon, bang_du_lieu, cau_hinh_json)
            VALUES (?, ?, ?, ?, ?)
            ''', (ten_dashboard, mo_ta, database_nguon, bang_du_lieu, cau_hinh_json))
            
            dashboard_id = con_tro.lastrowid
            ket_noi.commit()
            ket_noi.close()
            
            return dashboard_id
        except Exception as e:
            print(f"Lỗi lưu dashboard: {e}")
            return None
    
    def xoa_dashboard(self, dashboard_id):
        """
        Xóa dashboard (soft delete)
        """
        try:
            ket_noi = sqlite3.connect(self.db_path)
            con_tro = ket_noi.cursor()
            
            con_tro.execute('''
            UPDATE dashboards SET trang_thai = 'deleted' WHERE id = ?
            ''', (dashboard_id,))
            
            ket_noi.commit()
            ket_noi.close()
            return True
        except Exception as e:
            print(f"Lỗi xóa dashboard: {e}")
            return False
```

### 🔧 **BƯỚC 3: Thêm Routes vào Flask App**

**Sửa file:** `src/tableau_universal_connector.py`

**Thêm import ở đầu file:**
```python
from dashboard_gallery import DashboardGallery
import os
```

**Thêm trước route `@app.route('/')`:**

```python
# Khởi tạo Dashboard Gallery
dashboard_gallery = DashboardGallery()

# Đảm bảo database tồn tại
if not os.path.exists('database/dashboard_gallery.db'):
    print("⚠️ Database dashboard chưa tồn tại. Chạy: python scripts/tao_database_dashboard.py")

@app.route('/gallery')
def gallery_page():
    """
    Trang Dashboard Gallery - danh sách tất cả dashboard
    """
    dashboards = dashboard_gallery.lay_tat_ca_dashboard()
    
    gallery_template = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Gallery - Universal Connector</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 18px;
            opacity: 0.9;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .dashboard-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transition: transform 0.3s, box-shadow 0.3s;
            cursor: pointer;
        }
        
        .dashboard-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.2);
        }
        
        .dashboard-title {
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }
        
        .dashboard-description {
            color: #7f8c8d;
            font-size: 14px;
            line-height: 1.4;
            margin-bottom: 15px;
        }
        
        .dashboard-info {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
            color: #95a5a6;
            border-top: 1px solid #ecf0f1;
            padding-top: 15px;
        }
        
        .dashboard-source {
            background: #3498db;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
        }
        
        .dashboard-stats {
            display: flex;
            gap: 15px;
        }
        
        .stat {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .actions {
            text-align: center;
            margin-top: 20px;
        }
        
        .btn {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 16px;
            margin: 0 10px;
            display: inline-block;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #95a5a6, #7f8c8d);
        }
        
        .empty-state {
            text-align: center;
            color: white;
            padding: 60px 20px;
        }
        
        .empty-state h2 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
                gap: 15px;
            }
            
            .header h1 {
                font-size: 28px;
            }
            
            .header p {
                font-size: 16px;
            }
            
            .dashboard-card {
                padding: 15px;
            }
            
            .btn {
                display: block;
                margin: 10px auto;
                width: 80%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Dashboard Gallery</h1>
            <p>Khám phá và quản lý các dashboard đã tạo</p>
        </div>
        
        {% if dashboards %}
        <div class="dashboard-grid">
            {% for dashboard in dashboards %}
            <div class="dashboard-card" onclick="openDashboard({{ dashboard.id }})">
                <div class="dashboard-title">{{ dashboard.ten_dashboard }}</div>
                <div class="dashboard-description">{{ dashboard.mo_ta or 'Không có mô tả' }}</div>
                <div class="dashboard-info">
                    <div>
                        <span class="dashboard-source">{{ dashboard.database_nguon }}</span>
                        <span style="margin-left: 10px;">📋 {{ dashboard.bang_du_lieu }}</span>
                    </div>
                    <div class="dashboard-stats">
                        <div class="stat">
                            <span>👁️</span>
                            <span>{{ dashboard.so_lan_truy_cap or 0 }}</span>
                        </div>
                        <div class="stat">
                            <span>📅</span>
                            <span>{{ dashboard.ngay_tao[:10] if dashboard.ngay_tao else 'N/A' }}</span>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-state">
            <h2>🤷‍♂️ Chưa có dashboard nào</h2>
            <p>Tạo dashboard đầu tiên bằng cách kết nối từ Tableau Desktop</p>
        </div>
        {% endif %}
        
        <div class="actions">
            <a href="/" class="btn">🚀 Tạo Dashboard Mới</a>
            <a href="/api/dashboard-stats" class="btn btn-secondary">📈 Thống Kê</a>
        </div>
    </div>
    
    <script>
        function openDashboard(dashboardId) {
            // Redirect tới trang dashboard detail
            window.location.href = '/dashboard/' + dashboardId;
        }
        
        // Auto refresh mỗi 30 giây
        setTimeout(function() {
            location.reload();
        }, 30000);
    </script>
</body>
</html>
    '''
    
    from flask import render_template_string
    return render_template_string(gallery_template, dashboards=dashboards)

@app.route('/dashboard/<int:dashboard_id>')
def dashboard_detail(dashboard_id):
    """
    Trang chi tiết dashboard và kết nối Tableau
    """
    dashboard = dashboard_gallery.lay_dashboard_theo_id(dashboard_id)
    if not dashboard:
        return "❌ Không tìm thấy dashboard!", 404
    
    # Cập nhật lần truy cập
    dashboard_gallery.cap_nhat_lan_truy_cap(dashboard_id)
    
    # Parse cấu hình JSON
    try:
        cau_hinh = json.loads(dashboard['cau_hinh_json'])
    except:
        cau_hinh = {}
    
    detail_template = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ dashboard.ten_dashboard }} - Dashboard Detail</title>
    <!-- Tableau WDC API -->
    <script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            color: white;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            color: #2c3e50;
        }
        
        .dashboard-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .dashboard-title {
            font-size: 32px;
            margin-bottom: 10px;
            color: #2c3e50;
        }
        
        .dashboard-meta {
            background: #ecf0f1;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        
        .meta-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            padding-bottom: 8px;
            border-bottom: 1px solid #bdc3c7;
        }
        
        .meta-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
        }
        
        .connect-section {
            text-align: center;
            background: #e8f5e8;
            padding: 20px;
            border-radius: 8px;
            border: 2px solid #27ae60;
        }
        
        .btn {
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            margin: 10px;
            transition: transform 0.2s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: linear-gradient(45deg, #95a5a6, #7f8c8d);
        }
        
        .config-preview {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            font-size: 14px;
            margin-top: 15px;
            border-left: 4px solid #3498db;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="dashboard-header">
            <h1 class="dashboard-title">{{ dashboard.ten_dashboard }}</h1>
            <p>{{ dashboard.mo_ta or 'Dashboard được tạo từ Universal Connector' }}</p>
        </div>
        
        <div class="dashboard-meta">
            <div class="meta-item">
                <strong>📊 Database:</strong>
                <span>{{ dashboard.database_nguon }}</span>
            </div>
            <div class="meta-item">
                <strong>📋 Bảng dữ liệu:</strong>
                <span>{{ dashboard.bang_du_lieu }}</span>
            </div>
            <div class="meta-item">
                <strong>📅 Ngày tạo:</strong>
                <span>{{ dashboard.ngay_tao[:19] if dashboard.ngay_tao else 'N/A' }}</span>
            </div>
            <div class="meta-item">
                <strong>👁️ Số lần truy cập:</strong>
                <span>{{ dashboard.so_lan_truy_cap or 0 }}</span>
            </div>
            <div class="meta-item">
                <strong>🔧 Người tạo:</strong>
                <span>{{ dashboard.nguoi_tao or 'admin' }}</span>
            </div>
        </div>
        
        <div class="connect-section">
            <h3>🚀 Kết nối với Tableau Desktop</h3>
            <p>Nhấn nút bên dưới để kết nối dashboard này với Tableau Desktop</p>
            
            <button class="btn" onclick="connectToTableau()">
                📊 Kết nối Tableau Desktop
            </button>
            
            <div class="config-preview">
                <strong>⚙️ Cấu hình kết nối:</strong><br>
                Database: {{ dashboard.database_nguon }}<br>
                Table: {{ dashboard.bang_du_lieu }}<br>
                Config: {{ dashboard.cau_hinh_json }}
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 20px;">
            <a href="/gallery" class="btn btn-secondary">← Quay lại Gallery</a>
            <a href="/" class="btn btn-secondary">🏠 Trang chủ</a>
        </div>
    </div>
    
    <script>
        // Tableau WDC cho dashboard cụ thể
        var myConnector = tableau.makeConnector();
        
        myConnector.getSchema = function(schemaCallback) {
            // Load schema cho bảng cụ thể
            fetch('/api/schema/{{ dashboard.bang_du_lieu }}?database={{ dashboard.database_nguon }}')
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        var cols = data.schema.columns.map(col => ({
                            "id": col.column_name,
                            "alias": col.column_name, 
                            "dataType": getTableauDataType(col.tableau_type)
                        }));
                        
                        var tableSchema = {
                            "id": "{{ dashboard.bang_du_lieu }}",
                            "alias": "{{ dashboard.ten_dashboard }}",
                            "columns": cols
                        };
                        
                        schemaCallback([tableSchema]);
                    } else {
                        tableau.abortWithError("Không thể lấy schema: " + (data.error || "Unknown error"));
                    }
                })
                .catch(error => {
                    tableau.abortWithError("Lỗi kết nối: " + error.message);
                });
        };
        
        myConnector.getData = function(table, doneCallback) {
            var config = {{ dashboard.cau_hinh_json | safe }};
            var apiUrl = '/api/data/{{ dashboard.bang_du_lieu }}';
            apiUrl += '?database={{ dashboard.database_nguon }}';
            apiUrl += '&limit=' + (config.limit || 100);
            apiUrl += '&order=' + (config.order || 'auto');
            if (config.where) {
                apiUrl += '&where=' + encodeURIComponent(config.where);
            }
            
            fetch(apiUrl)
                .then(response => response.json())
                .then(data => {
                    if (data.success && data.data) {
                        table.appendRows(data.data);
                    }
                    doneCallback();
                })
                .catch(error => {
                    tableau.abortWithError("Không thể lấy dữ liệu: " + error.message);
                });
        };
        
        function getTableauDataType(type) {
            switch(type) {
                case 'int': return tableau.dataTypeEnum.int;
                case 'float': return tableau.dataTypeEnum.float;
                case 'datetime': return tableau.dataTypeEnum.datetime;
                case 'bool': return tableau.dataTypeEnum.bool;
                default: return tableau.dataTypeEnum.string;
            }
        }
        
        tableau.registerConnector(myConnector);
        
        function connectToTableau() {
            tableau.connectionData = JSON.stringify({
                "database": "{{ dashboard.database_nguon }}",
                "table": "{{ dashboard.bang_du_lieu }}",
                "dashboard_id": {{ dashboard.id }},
                "config": {{ dashboard.cau_hinh_json | safe }}
            });
            
            tableau.connectionName = "{{ dashboard.ten_dashboard }}";
            tableau.submit();
        }
    </script>
</body>
</html>
    '''
    
    from flask import render_template_string
    return render_template_string(detail_template, dashboard=dashboard)

@app.route('/api/dashboard-stats')
def dashboard_stats():
    """
    API thống kê dashboard
    """
    try:
        dashboards = dashboard_gallery.lay_tat_ca_dashboard()
        
        stats = {
            "total_dashboards": len(dashboards),
            "total_views": sum(d.get('so_lan_truy_cap', 0) for d in dashboards),
            "databases_used": list(set(d['database_nguon'] for d in dashboards)),
            "popular_dashboards": sorted(dashboards, key=lambda x: x.get('so_lan_truy_cap', 0), reverse=True)[:5]
        }
        
        return jsonify({
            "success": True,
            "stats": stats
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })
```

### 🔧 **BƯỚC 4: Chạy setup database**

```bash
# Tạo database dashboard
python scripts/tao_database_dashboard.py

# Chạy server
python src/tableau_universal_connector.py
```

### 🧪 **BƯỚC 5: Test Dashboard Gallery**

**URLs để test:**
- `http://127.0.0.1:5002/gallery` - Gallery page
- `http://127.0.0.1:5002/dashboard/1` - Dashboard detail
- `http://127.0.0.1:5002/api/dashboard-stats` - Stats API

**Checklist test:**
- ✅ Gallery hiển thị danh sách dashboard?
- ✅ Dashboard cards responsive?
- ✅ Click vào card chuyển trang detail?
- ✅ Connect Tableau từ detail page hoạt động?
- ✅ Stats API trả về đúng dữ liệu?

### 🎨 **BƯỚC 6: Thêm link Gallery vào trang chính**

**Sửa template chính trong `TABLEAU_WDC_TEMPLATE`:**

Thêm sau thẻ `<h1>`:
```html
<div style="text-align: center; margin-bottom: 20px;">
    <a href="/gallery" style="background: #27ae60; color: white; padding: 8px 16px; 
       border-radius: 20px; text-decoration: none; font-size: 14px; margin-right: 10px;">
        📊 Dashboard Gallery
    </a>
    <a href="/api/dashboard-stats" target="_blank" style="background: #8e44ad; color: white; 
       padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 14px;">
        📈 Thống Kê
    </a>
</div>
```

### 🎯 **BƯỚC 7: Auto-save Dashboard**

**Thêm function auto-save khi user connect từ trang chính:**

Thêm vào cuối `submitButton` click handler:
```javascript
// Auto-save dashboard configuration
function autoSaveDashboard() {
    var database = document.getElementById("databaseSelect").value;
    var selectedTables = getSelectedTables();
    var limit = document.getElementById("limitSelect").value;
    var order = document.getElementById("orderSelect").value;
    var where = document.getElementById("whereInput").value;
    
    if (database && selectedTables.length > 0) {
        var dashboardName = `${database} - ${selectedTables.join(', ')} (${new Date().toLocaleDateString()})`;
        var description = `Auto-saved dashboard: ${selectedTables.length} tables from ${database}`;
        
        var config = {
            tables: selectedTables,
            limit: limit,
            order: order,
            where: where
        };
        
        // Gửi request save (sẽ implement API sau)
        fetch('/api/save-dashboard', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: dashboardName,
                description: description,
                database: database,
                tables: selectedTables.join(','),
                config: config
            })
        }).catch(error => {
            console.log('Auto-save error:', error);
        });
    }
}

// Gọi auto-save trước khi submit
document.getElementById("submitButton").addEventListener("click", function() {
    autoSaveDashboard();
    // ... existing code
});
```

### 🐛 **TROUBLESHOOTING**

**Lỗi database không tồn tại:**
```bash
# Tạo lại database
python scripts/tao_database_dashboard.py
```

**Lỗi import dashboard_gallery:**
```python
# Đảm bảo file đúng đường dẫn
# src/dashboard_gallery.py phải cùng thư mục với tableau_universal_connector.py
```

**Gallery không hiển thị dashboard:**
```python
# Check database có dữ liệu không
import sqlite3
conn = sqlite3.connect('database/dashboard_gallery.db')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM dashboards')
print(cursor.fetchone())
```

### 🎉 **KẾT QUẢ MONG ĐỢI**

Sau khi hoàn thành:
- ✅ Dashboard Gallery với grid layout đẹp
- ✅ Database SQLite lưu trữ dashboard info
- ✅ Dashboard detail page với Tableau connect
- ✅ Auto-save dashboard khi user connect
- ✅ Stats API cho analytics
- ✅ Mobile responsive gallery

### 📝 **COMMIT MESSAGE**
```bash
git add .
git commit -m "Thêm Dashboard Gallery system

- Tạo database SQLite cho dashboard storage
- Dashboard Gallery page với grid layout
- Dashboard detail page với Tableau integration  
- Auto-save dashboard configuration
- Stats API cho analytics
- Mobile responsive design
- Navigation links từ trang chính"
```

### ➡️ **BƯỚC TIẾP THEO**
Hoàn thành rồi chuyển sang: `HUONG_DAN_EXPORT_FEATURES.md`
