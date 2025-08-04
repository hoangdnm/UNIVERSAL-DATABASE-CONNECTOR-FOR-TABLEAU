#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tableau Universal Web Data Connector - API linh hoạt
Dự án tốt nghiệp - Kết nối Tableau với bất kỳ SQL Server database nào

Tính năng: Tự động đọc cấu hình database và schema
"""

from flask import Flask, render_template_string, jsonify, request
from datetime import datetime
import json
import os

app = Flask(__name__)

def doc_cau_hinh_database():
    """
    Đọc cấu hình database từ file
    """
    config_path = "config/database_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Cấu hình mặc định
        return {
            'server': '127.0.0.1',
            'port': 1433,
            'user': 'sa',
            'password': 'YourStrong!Pass123',
            'database': 'master'
        }

def lay_danh_sach_database():
    """
    Lấy danh sách tất cả databases có sẵn
    """
    config = doc_cau_hinh_database()
    
    try:
        import pymssql
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='master'
        )
        
        con_tro = ket_noi.cursor()
        con_tro.execute("SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb') ORDER BY name")
        
        database_list = [db[0] for db in con_tro.fetchall()]
        ket_noi.close()
        return database_list
        
    except Exception as e:
        print(f"Lỗi lấy danh sách database: {e}")
        return []

def lay_danh_sach_bang(database_name=None):
    """
    Lấy danh sách tất cả bảng trong database
    """
    config = doc_cau_hinh_database()
    if database_name:
        config['database'] = database_name
    
    try:
        import pymssql
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        con_tro = ket_noi.cursor()
        con_tro.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """)
        
        bang_list = [bang[0] for bang in con_tro.fetchall()]
        ket_noi.close()
        return bang_list
        
    except Exception as e:
        print(f"Lỗi lấy danh sách bảng: {e}")
        return []

def doc_schema_bang(ten_bang):
    """
    Đọc schema của bảng từ file hoặc tự động phát hiện
    """
    schema_path = f"config/schema_{ten_bang}.json"
    
    if os.path.exists(schema_path):
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        # Tự động phát hiện schema
        return tu_dong_phat_hien_schema(ten_bang)

def tu_dong_phat_hien_schema(ten_bang, database_name=None):
    """
    Tự động phát hiện schema của bảng
    """
    config = doc_cau_hinh_database()
    if database_name:
        config['database'] = database_name
    
    try:
        import pymssql
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        con_tro = ket_noi.cursor()
        con_tro.execute(f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{ten_bang}'
        ORDER BY ORDINAL_POSITION
        """)
        
        cot_list = con_tro.fetchall()
        
        columns = []
        for ten_cot, data_type in cot_list:
            # Chuyển đổi SQL Server data type sang Tableau data type
            if data_type in ['int', 'bigint', 'smallint', 'tinyint']:
                tableau_type = 'int'
            elif data_type in ['decimal', 'numeric', 'float', 'real', 'money']:
                tableau_type = 'float'
            elif data_type in ['datetime', 'datetime2', 'date', 'time']:
                tableau_type = 'datetime'
            elif data_type in ['bit']:
                tableau_type = 'bool'
            else:
                tableau_type = 'string'
            
            columns.append({
                'column_name': ten_cot,
                'sql_type': data_type,
                'tableau_type': tableau_type
            })
        
        ket_noi.close()
        
        return {
            'table_name': ten_bang,
            'columns': columns,
            'database': config['database']
        }
        
    except Exception as e:
        print(f"Lỗi phát hiện schema: {e}")
        return None

# Template HTML linh hoạt
TABLEAU_WDC_TEMPLATE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Tableau Universal Database Connector</title>
    
    <!-- Tableau WDC API -->
    <script src="https://connectors.tableau.com/libs/tableauwdc-2.3.latest.js" type="text/javascript"></script>
    
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            padding: 30px;
        }
        
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        
        select, input {
            width: 100%;
            padding: 10px;
            border: 2px solid #ecf0f1;
            border-radius: 5px;
            font-size: 16px;
            box-sizing: border-box;
        }
        
        select:focus, input:focus {
            outline: none;
            border-color: #3498db;
        }
        
        button {
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
            transition: transform 0.2s;
        }
        
        button:hover {
            transform: translateY(-2px);
        }
        
        .info {
            background: #e8f5e8;
            border: 1px solid #27ae60;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 10px;
            border-radius: 5px;
            margin-top: 20px;
            font-size: 14px;
        }
        
        .database-info {
            background: #e3f2fd;
            border: 1px solid #2196f3;
            padding: 15px;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Tableau Universal Database Connector</h1>
        <p class="subtitle">Kết nối Tableau với bất kỳ SQL Server database nào</p>
        
        <div class="info">
            <strong>🎓 Dự án tốt nghiệp - Tính năng nâng cao:</strong>
            <ul>
                <li><strong>Universal Connection:</strong> Kết nối với bất kỳ SQL Server database nào</li>
                <li><strong>Auto Schema Detection:</strong> Tự động phát hiện cấu trúc bảng</li>
                <li><strong>Dynamic Data Loading:</strong> Tải dữ liệu linh hoạt theo cấu hình</li>
                <li><strong>Tableau Integration:</strong> Tương thích hoàn toàn với Tableau Desktop</li>
            </ul>
        </div>
        
        <div class="form-group">
            <label for="databaseSelect">Chọn database:</label>
            <select id="databaseSelect">
                <option value="">Đang tải danh sách database...</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="tableSelect">Chọn bảng dữ liệu:</label>
            <select id="tableSelect">
                <option value="">Chọn database trước...</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="limitSelect">Số lượng dòng dữ liệu:</label>
            <select id="limitSelect">
                <option value="10">10 dòng (Test nhanh)</option>
                <option value="50">50 dòng (Demo cơ bản)</option>
                <option value="100" selected>100 dòng (Hiển thị tiêu chuẩn)</option>
                <option value="500">500 dòng (Dataset lớn)</option>
                <option value="1000">1000 dòng (Toàn bộ - nếu có)</option>
                <option value="0">Tất cả dòng (Không giới hạn)</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="orderSelect">Sắp xếp theo:</label>
            <select id="orderSelect">
                <option value="auto">Tự động (theo cột đầu tiên)</option>
                <option value="random">Ngẫu nhiên</option>
                <option value="custom">Tùy chỉnh (nhập SQL WHERE)</option>
            </select>
        </div>
        
        <div class="form-group" id="customWhere" style="display: none;">
            <label for="whereInput">Điều kiện WHERE (SQL):</label>
            <input type="text" id="whereInput" placeholder="VD: column_name > 100 AND other_column = 'value'">
        </div>
        
        <button type="button" id="submitButton">🚀 Kết nối với Tableau Desktop</button>
        
        <div class="database-info">
            <strong>📊 Thông tin kết nối:</strong>
            <div id="databaseInfo">Đang tải thông tin database...</div>
        </div>
        
        <div class="warning">
            <strong>⚠️ Lưu ý:</strong> 
            <ul>
                <li>Đảm bảo SQL Server đang chạy và có thể truy cập</li>
                <li>Kiểm tra file cấu hình config/database_config.json</li>
                <li>Chạy python scripts/cau_hinh_database.py để cấu hình kết nối</li>
            </ul>
        </div>
    </div>

    <script type="text/javascript">
        (function() {
            // Load thông tin database và bảng
            loadDatabaseInfo();
            loadDatabaseList();
            
            // Xử lý sự kiện thay đổi database
            document.getElementById('databaseSelect').addEventListener('change', function() {
                var selectedDatabase = this.value;
                if (selectedDatabase) {
                    loadTableList(selectedDatabase);
                } else {
                    document.getElementById('tableSelect').innerHTML = '<option value="">Chọn database trước...</option>';
                }
            });
            
            // Xử lý sự kiện thay đổi order
            document.getElementById('orderSelect').addEventListener('change', function() {
                var customWhere = document.getElementById('customWhere');
                if (this.value === 'custom') {
                    customWhere.style.display = 'block';
                } else {
                    customWhere.style.display = 'none';
                }
            });
            
            function loadDatabaseInfo() {
                fetch('/api/database-info')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('databaseInfo').innerHTML = 
                                `<strong>Server:</strong> ${data.server}:${data.port}<br>
                                 <strong>Database hiện tại:</strong> ${data.database}<br>
                                 <strong>Số bảng:</strong> ${data.table_count} bảng`;
                        }
                    })
                    .catch(error => console.error('Error loading database info:', error));
            }
            
            function loadDatabaseList() {
                fetch('/api/databases')
                    .then(response => response.json())
                    .then(data => {
                        var databaseSelect = document.getElementById('databaseSelect');
                        databaseSelect.innerHTML = '';
                        
                        if (data.success && data.databases.length > 0) {
                            // Thêm option mặc định
                            var defaultOption = document.createElement('option');
                            defaultOption.value = '';
                            defaultOption.textContent = 'Chọn database...';
                            databaseSelect.appendChild(defaultOption);
                            
                            data.databases.forEach(database => {
                                var option = document.createElement('option');
                                option.value = database;
                                option.textContent = database;
                                databaseSelect.appendChild(option);
                            });
                        } else {
                            var option = document.createElement('option');
                            option.textContent = 'Không tìm thấy database nào';
                            databaseSelect.appendChild(option);
                        }
                    })
                    .catch(error => {
                        console.error('Error loading databases:', error);
                        document.getElementById('databaseSelect').innerHTML = '<option>Lỗi tải danh sách database</option>';
                    });
            }
            
            function loadTableList(database) {
                var apiUrl = database ? `/api/tables?database=${encodeURIComponent(database)}` : '/api/tables';
                
                fetch(apiUrl)
                    .then(response => response.json())
                    .then(data => {
                        var tableSelect = document.getElementById('tableSelect');
                        tableSelect.innerHTML = '';
                        
                        if (data.success && data.tables.length > 0) {
                            data.tables.forEach(table => {
                                var option = document.createElement('option');
                                option.value = table;
                                option.textContent = table;
                                tableSelect.appendChild(option);
                            });
                        } else {
                            var option = document.createElement('option');
                            option.textContent = 'Không tìm thấy bảng nào';
                            tableSelect.appendChild(option);
                        }
                    })
                    .catch(error => {
                        console.error('Error loading tables:', error);
                        document.getElementById('tableSelect').innerHTML = '<option>Lỗi tải danh sách bảng</option>';
                    });
            }
            
            // Khởi tạo Tableau WDC
            var myConnector = tableau.makeConnector();
            
            // Định nghĩa schema động
            myConnector.getSchema = function(schemaCallback) {
                var connectionData = JSON.parse(tableau.connectionData);
                var tableName = connectionData.table;
                var database = connectionData.database;
                
                // Lấy schema từ server
                var schemaUrl = `/api/schema/${tableName}`;
                if (database) {
                    schemaUrl += `?database=${encodeURIComponent(database)}`;
                }
                
                fetch(schemaUrl)
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            var cols = data.schema.columns.map(col => ({
                                "id": col.column_name,
                                "alias": col.column_name,
                                "dataType": getTableauDataType(col.tableau_type)
                            }));
                            
                            var tableSchema = {
                                "id": tableName,
                                "alias": `Dữ liệu từ ${database}.${tableName}`,
                                "columns": cols
                            };
                            
                            schemaCallback([tableSchema]);
                        } else {
                            tableau.abortWithError("Không thể lấy schema của bảng");
                        }
                    })
                    .catch(error => {
                        console.error("Lỗi lấy schema:", error);
                        tableau.abortWithError("Lỗi kết nối server");
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
            
            // Lấy dữ liệu
            myConnector.getData = function(table, doneCallback) {
                var connectionData = JSON.parse(tableau.connectionData);
                
                var apiUrl = `/api/data/${connectionData.table}?limit=${connectionData.limit}&order=${connectionData.order}`;
                if (connectionData.database) {
                    apiUrl += `&database=${encodeURIComponent(connectionData.database)}`;
                }
                if (connectionData.where) {
                    apiUrl += `&where=${encodeURIComponent(connectionData.where)}`;
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
                        console.error("Lỗi khi lấy dữ liệu:", error);
                        tableau.abortWithError("Không thể lấy dữ liệu từ API");
                    });
            };
            
            // Đăng ký connector
            tableau.registerConnector(myConnector);
            
            // Xử lý sự kiện submit
            document.getElementById("submitButton").addEventListener("click", function() {
                var database = document.getElementById("databaseSelect").value;
                var table = document.getElementById("tableSelect").value;
                var limit = document.getElementById("limitSelect").value;
                var order = document.getElementById("orderSelect").value;
                var where = document.getElementById("whereInput").value;
                
                if (!database) {
                    alert("Vui lòng chọn database");
                    return;
                }
                
                if (!table) {
                    alert("Vui lòng chọn bảng dữ liệu");
                    return;
                }
                
                tableau.connectionData = JSON.stringify({
                    "database": database,
                    "table": table,
                    "limit": limit,
                    "order": order,
                    "where": where
                });
                
                tableau.connectionName = `${database}.${table} (${limit === '0' ? 'Tất cả' : limit} dòng)`;
                tableau.submit();
            });
        })();
    </script>
</body>
</html>
'''

# Routes
@app.route('/')
def tableau_wdc():
    """
    Trang chính của Tableau Universal Database Connector
    """
    return render_template_string(TABLEAU_WDC_TEMPLATE)

@app.route('/api/database-info')
def database_info():
    """
    Lấy thông tin database hiện tại
    """
    try:
        config = doc_cau_hinh_database()
        bang_list = lay_danh_sach_bang()
        
        return jsonify({
            "success": True,
            "server": config['server'],
            "port": config['port'],
            "database": config['database'],
            "table_count": len(bang_list)
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/databases')
def list_databases():
    """
    Lấy danh sách tất cả databases
    """
    try:
        database_list = lay_danh_sach_database()
        return jsonify({
            "success": True,
            "databases": database_list
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "databases": []
        })

@app.route('/api/tables')
def list_tables():
    """
    Lấy danh sách tất cả bảng trong database
    """
    try:
        database_name = request.args.get('database', None)
        bang_list = lay_danh_sach_bang(database_name)
        return jsonify({
            "success": True,
            "tables": bang_list,
            "database": database_name or doc_cau_hinh_database()['database']
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "tables": []
        })

@app.route('/api/schema/<table_name>')
def get_table_schema(table_name):
    """
    Lấy schema của bảng
    """
    try:
        database_name = request.args.get('database', None)
        schema = tu_dong_phat_hien_schema(table_name, database_name)
        if schema:
            return jsonify({
                "success": True,
                "schema": schema
            })
        else:
            return jsonify({
                "success": False,
                "error": "Không thể lấy schema"
            })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/data/<table_name>')
def get_table_data(table_name):
    """
    Lấy dữ liệu từ bảng
    """
    try:
        config = doc_cau_hinh_database()
        database_name = request.args.get('database', None)
        if database_name:
            config['database'] = database_name
            
        limit = request.args.get('limit', '100')
        order = request.args.get('order', 'auto')
        where_clause = request.args.get('where', '')
        
        import pymssql
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        con_tro = ket_noi.cursor()
        
        # Xây dựng câu truy vấn
        if limit == '0':
            limit_clause = ""
        else:
            limit_clause = f"TOP {limit}"
        
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
        
        query = f"SELECT {limit_clause} * FROM [{table_name}] {where_sql} {order_clause}"
        
        con_tro.execute(query)
        ket_qua = con_tro.fetchall()
        
        # Lấy tên cột
        schema = tu_dong_phat_hien_schema(table_name, database_name)
        if schema:
            columns = [col['column_name'] for col in schema['columns']]
        else:
            columns = [desc[0] for desc in con_tro.description]
        
        # Chuyển đổi dữ liệu
        du_lieu_json = []
        for dong in ket_qua:
            dong_dict = {}
            for i, gia_tri in enumerate(dong):
                if isinstance(gia_tri, datetime):
                    dong_dict[columns[i]] = gia_tri.isoformat()
                elif gia_tri is None:
                    dong_dict[columns[i]] = None
                else:
                    dong_dict[columns[i]] = gia_tri
            du_lieu_json.append(dong_dict)
        
        ket_noi.close()
        
        return jsonify({
            "success": True,
            "data": du_lieu_json,
            "count": len(du_lieu_json),
            "table": table_name,
            "database": config['database'],
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "message": f"Lấy dữ liệu từ bảng {table_name} thành công"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "data": []
        })

if __name__ == '__main__':
    print("🌐 TABLEAU UNIVERSAL DATABASE CONNECTOR")
    print("=" * 55)
    print("🚀 Đang khởi động server...")
    print("🔗 URL cho Tableau: http://127.0.0.1:5002")
    print("📊 Cấu hình database: config/database_config.json")
    print("")
    print("🎯 TÍNH NĂNG NÂNG CAO:")
    print("  ✅ Kết nối với bất kỳ SQL Server database nào")
    print("  ✅ Tự động phát hiện schema của bảng")
    print("  ✅ Linh hoạt chọn bảng và số lượng dữ liệu")
    print("  ✅ Hỗ trợ câu truy vấn WHERE tùy chỉnh")
    print("")
    print("⏹️  Nhấn Ctrl+C để dừng server")
    print("=" * 55)
    
    app.run(debug=True, host='127.0.0.1', port=5002)
