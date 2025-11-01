#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template_string, jsonify, request
from datetime import datetime
import json
import os
import sys

# Them thu muc src vao path de import duoc database_connector
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import module ket noi database
import database_connector as db_conn


app = Flask(__name__)

def doc_cau_hinh_database():
    """
    Đọc cấu hình database từ file
    """
    return db_conn.doc_cau_hinh_database()

def lay_danh_sach_database():
    """
    Lấy danh sách tất cả databases có sẵn
    """
    return db_conn.lay_danh_sach_database()

def lay_danh_sach_bang(database_name=None):
    """
    Lấy danh sách tất cả bảng trong database
    """
    return db_conn.lay_danh_sach_bang(database_name)

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
        db_name = database_name
    else:
        db_name = config['database']
    
    try:
        columns = db_conn.lay_schema_bang(ten_bang, db_name)
        
        return {
            'table_name': ten_bang,
            'columns': columns,
            'database': db_name
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
        
        .table-checkbox {
            display: flex;
            align-items: center;
            padding: 8px;
            margin: 5px 0;
            border-radius: 4px;
            cursor: pointer;
            transition: background-color 0.2s;
        }
        
        .table-checkbox:hover {
            background-color: #f8f9fa;
        }
        
        .table-checkbox input[type="checkbox"] {
            margin-right: 10px;
            width: auto;
        }
        
        .table-checkbox label {
            margin: 0;
            cursor: pointer;
            font-weight: normal;
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
                <li><strong>Multi-Table Focus:</strong> 🆕 Chọn và kết hợp nhiều bảng cùng lúc</li>
                <li><strong>Dynamic Data Loading:</strong> Tải dữ liệu linh hoạt theo cấu hình</li>
                <li><strong>Tableau Integration:</strong> Tương thích hoàn toàn với Tableau Desktop</li>
            </ul>
        </div>
        
        <div class="form-group">
            <label>Chọn database (có thể chọn nhiều):</label>
            <div id="databasesContainer" style="max-height: 150px; overflow-y: auto; border: 2px solid #ecf0f1; border-radius: 5px; padding: 10px; background: white;">
                <div style="color: #7f8c8d; font-style: italic;">Đang tải danh sách database...</div>
            </div>
            <div style="margin-top: 5px; font-size: 12px; color: #7f8c8d;">
                <span id="selectedDatabasesCount">0</span> database đã chọn
            </div>
        </div>
        
        <div class="form-group">
            <label>Chọn các bảng dữ liệu (có thể chọn nhiều):</label>
            <div id="tablesContainer" style="max-height: 250px; overflow-y: auto; border: 2px solid #ecf0f1; border-radius: 5px; padding: 10px; background: white;">
                <div style="color: #7f8c8d; font-style: italic;">Chọn database trước để hiển thị danh sách bảng...</div>
            </div>
            <div style="margin-top: 5px; font-size: 12px; color: #7f8c8d;">
                <span id="selectedTablesCount">0</span> bảng đã chọn
            </div>
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
        // Global functions cần thiết cho HTML inline events
        
        // ===== FUNCTIONS CHO DATABASE CHECKBOXES =====
        function toggleAllDatabases() {
            var selectAllCheckbox = document.getElementById('selectAllDatabases');
            var databaseCheckboxes = document.querySelectorAll('input[name="selectedDatabases"]');
            
            databaseCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAllCheckbox.checked;
            });
            
            updateSelectedDatabasesCount();
            loadTablesFromSelectedDatabases();
        }
        
        // ===== FUNCTION LOAD BẢNG TỪ NHIỀU DATABASE =====
        function loadTablesFromSelectedDatabases() {
            var selectedDatabases = getSelectedDatabases();
            console.log('🔄 Đang tải bảng từ', selectedDatabases.length, 'database(s):', selectedDatabases);
            
            var tablesContainer = document.getElementById('tablesContainer');
            
            if (selectedDatabases.length === 0) {
                tablesContainer.innerHTML = '<div style="color: #7f8c8d; font-style: italic;">Chọn database trước để hiển thị danh sách bảng...</div>';
                updateSelectedTablesCount();
                return;
            }
            
            tablesContainer.innerHTML = '<div style="color: #7f8c8d; font-style: italic;">Đang tải bảng...</div>';
            
            // Load bảng từ từng database
            Promise.all(selectedDatabases.map(database => 
                fetch(`/api/tables?database=${encodeURIComponent(database)}`)
                    .then(response => response.json())
                    .then(data => ({ database, data }))
            ))
            .then(results => {
                tablesContainer.innerHTML = '';
                
                // Thêm checkbox "Chọn tất cả"
                var selectAllDiv = document.createElement('div');
                selectAllDiv.className = 'table-checkbox';
                selectAllDiv.innerHTML = `
                    <input type="checkbox" id="selectAllTables" onchange="toggleAllTables()">
                    <label for="selectAllTables"><strong>Chọn tất cả bảng</strong></label>
                `;
                tablesContainer.appendChild(selectAllDiv);
                
                // Thêm đường phân cách
                var separator = document.createElement('hr');
                separator.style.margin = '10px 0';
                tablesContainer.appendChild(separator);
                
                // Hiển thị bảng từ từng database
                results.forEach(result => {
                    var database = result.database;
                    var data = result.data;
                    
                    if (data.success && data.tables && data.tables.length > 0) {
                        // Thêm header database
                        var dbHeader = document.createElement('div');
                        dbHeader.style.cssText = 'font-weight: bold; color: #2980b9; margin-top: 15px; margin-bottom: 8px; padding: 5px; background: #ecf0f1; border-radius: 4px;';
                        dbHeader.textContent = `━━━ ${database} (${data.tables.length} bảng) ━━━`;
                        tablesContainer.appendChild(dbHeader);
                        
                        // Thêm checkbox cho từng bảng với format DB.Table
                        data.tables.forEach(table => {
                            var tableDiv = document.createElement('div');
                            tableDiv.className = 'table-checkbox';
                            var tableId = `${database}.${table}`;
                            tableDiv.innerHTML = `
                                <input type="checkbox" id="table_${tableId.replace(/\./g, '_')}" name="selectedTables" value="${tableId}" onchange="updateSelectedTablesCount()">
                                <label for="table_${tableId.replace(/\./g, '_')}">  • ${table}</label>
                            `;
                            tablesContainer.appendChild(tableDiv);
                        });
                    }
                });
                
                updateSelectedTablesCount();
                console.log('✅ Đã tải xong bảng từ', selectedDatabases.length, 'database(s)');
            })
            .catch(error => {
                console.error('❌ Error loading tables:', error);
                tablesContainer.innerHTML = '<div style="color: #dc3545; font-style: italic;">Lỗi tải danh sách bảng</div>';
            });
        }
        
        function updateSelectedDatabasesCount(shouldLoadTables) {
            console.log('🔍 updateSelectedDatabasesCount called, shouldLoadTables:', shouldLoadTables);
            var selectedCheckboxes = document.querySelectorAll('input[name="selectedDatabases"]:checked');
            var countElement = document.getElementById('selectedDatabasesCount');
            
            console.log('📊 Selected databases:', selectedCheckboxes.length);
            
            if (countElement) {
                countElement.textContent = selectedCheckboxes.length;
            }
            
            // Cập nhật trạng thái "Chọn tất cả"
            var selectAllCheckbox = document.getElementById('selectAllDatabases');
            var allCheckboxes = document.querySelectorAll('input[name="selectedDatabases"]');
            
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
            
            // Chỉ tự động load bảng khi user thay đổi selection (không phải lúc init)
            if (shouldLoadTables !== false) {
                loadTablesFromSelectedDatabases();
            }
        }
        
        function getSelectedDatabases() {
            var selectedCheckboxes = document.querySelectorAll('input[name="selectedDatabases"]:checked');
            return Array.from(selectedCheckboxes).map(checkbox => checkbox.value);
        }
        
        // ===== FUNCTIONS CHO TABLE CHECKBOXES =====
        function toggleAllTables() {
            var selectAllCheckbox = document.getElementById('selectAllTables');
            var tableCheckboxes = document.querySelectorAll('input[name="selectedTables"]');
            
            tableCheckboxes.forEach(checkbox => {
                checkbox.checked = selectAllCheckbox.checked;
            });
            
            updateSelectedTablesCount();
        }
        
        function updateSelectedTablesCount() {
            var selectedCheckboxes = document.querySelectorAll('input[name="selectedTables"]:checked');
            var countElement = document.getElementById('selectedTablesCount');
            
            if (countElement) {
                countElement.textContent = selectedCheckboxes.length;
            }
            
            // Cập nhật trạng thái "Chọn tất cả"
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
        
        function getSelectedTables() {
            var selectedCheckboxes = document.querySelectorAll('input[name="selectedTables"]:checked');
            return Array.from(selectedCheckboxes).map(checkbox => checkbox.value);
        }
        
        (function() {
            // Đọc URL parameters (hỗ trợ cả format cũ và mới)
            function getUrlParams() {
                const params = new URLSearchParams(window.location.search);
                return {
                    // Format mới: databases=DB1,DB2,DB3
                    databases: params.get('databases') ? params.get('databases').split(',') : 
                               // Format cũ: database=DB1 (backwards compatible)
                               (params.get('database') ? [params.get('database')] : []),
                    // tables với format DB.Table hoặc Table
                    tables: params.get('tables') ? params.get('tables').split(',') : []
                };
            }
            
            // Load thông tin database và bảng
            loadDatabaseInfo();
            loadDatabaseList();
            
            // Xử lý URL parameters sau khi load xong database list
            const urlParams = getUrlParams();
            if (urlParams.databases.length > 0) {
                console.log('🔗 Phát hiện URL parameters:', urlParams);
                // Đợi một chút để database list load xong
                setTimeout(function() {
                    // Chọn các database
                    urlParams.databases.forEach(function(dbName) {
                        const checkbox = document.getElementById('db_' + dbName);
                        if (checkbox) {
                            checkbox.checked = true;
                            console.log('✅ Đã chọn database:', dbName);
                        }
                    });
                    updateSelectedDatabasesCount();
                    
                    // Load bảng từ các database đã chọn
                    loadTablesFromSelectedDatabases();
                    
                    // Đợi tables load xong rồi mới check các bảng
                    if (urlParams.tables.length > 0) {
                        setTimeout(function() {
                            urlParams.tables.forEach(function(tableName) {
                                // tableName có thể là "DB.Table" hoặc "Table"
                                const tableId = 'table_' + tableName.replace(/\./g, '_');
                                const checkbox = document.getElementById(tableId);
                                if (checkbox) {
                                    checkbox.checked = true;
                                    console.log('✅ Đã chọn bảng:', tableName);
                                }
                            });
                            updateSelectedTablesCount();
                        }, 1500);
                    }
                }, 500);
            }
            
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
                console.log('🔄 Đang tải thông tin database...');
                fetch('/api/database-info')
                    .then(response => {
                        console.log('📡 Database info response status:', response.status);
                        return response.json();
                    })
                    .then(data => {
                        console.log('📊 Database info response:', data);
                        if (data.success) {
                            document.getElementById('databaseInfo').innerHTML = 
                                `<strong>Server:</strong> ${data.server}:${data.port}<br>
                                 <strong>Database hiện tại:</strong> ${data.database}<br>
                                 <strong>Số bảng:</strong> ${data.table_count} bảng`;
                        } else {
                            document.getElementById('databaseInfo').innerHTML = 
                                `<span style="color: red;">Lỗi: ${data.error || 'Không thể tải thông tin database'}</span>`;
                        }
                    })
                    .catch(error => {
                        console.error('❌ Error loading database info:', error);
                        document.getElementById('databaseInfo').innerHTML = 
                            `<span style="color: red;">Lỗi kết nối: ${error.message}</span>`;
                    });
            }
            
            function loadDatabaseList() {
                console.log('🔄 Đang tải danh sách database...');
                fetch('/api/databases')
                    .then(response => {
                        console.log('📡 Response status:', response.status);
                        return response.json();
                    })
                    .then(data => {
                        console.log('📊 Database API response:', data);
                        var databasesContainer = document.getElementById('databasesContainer');
                        databasesContainer.innerHTML = '';
                        
                        if (data.success && data.databases && data.databases.length > 0) {
                            console.log('✅ Tìm thấy', data.databases.length, 'database(s)');
                            
                            // Thêm checkbox "Chọn tất cả"
                            var selectAllDiv = document.createElement('div');
                            selectAllDiv.className = 'table-checkbox';
                            selectAllDiv.innerHTML = `
                                <input type="checkbox" id="selectAllDatabases" onchange="toggleAllDatabases()">
                                <label for="selectAllDatabases"><strong>Chọn tất cả database</strong></label>
                            `;
                            databasesContainer.appendChild(selectAllDiv);
                            
                            // Thêm đường phân cách
                            var separator = document.createElement('hr');
                            separator.style.margin = '10px 0';
                            databasesContainer.appendChild(separator);
                            
                            // Thêm checkbox cho từng database
                            data.databases.forEach(database => {
                                var dbDiv = document.createElement('div');
                                dbDiv.className = 'table-checkbox';
                                dbDiv.innerHTML = `
                                    <input type="checkbox" id="db_${database}" name="selectedDatabases" value="${database}" onchange="updateSelectedDatabasesCount()">
                                    <label for="db_${database}">${database}</label>
                                `;
                                databasesContainer.appendChild(dbDiv);
                                console.log('➕ Đã thêm database:', database);
                            });
                            
                            // Init: chỉ update count, không load tables
                            updateSelectedDatabasesCount(false);
                        } else {
                            console.log('❌ Không tìm thấy database hoặc lỗi:', data);
                            databasesContainer.innerHTML = `<div style="color: #dc3545; font-style: italic;">${data.success ? 'Không tìm thấy database nào' : ('Lỗi: ' + (data.error || 'Unknown error'))}</div>`;
                        }
                    })
                    .catch(error => {
                        console.error('❌ Error loading databases:', error);
                        document.getElementById('databasesContainer').innerHTML = '<div style="color: #dc3545; font-style: italic;">Lỗi tải danh sách database</div>';
                    });
            }
            
            function loadTableList(database) {
                console.log('🔄 Đang tải danh sách bảng cho database:', database);
                var apiUrl = database ? `/api/tables?database=${encodeURIComponent(database)}` : '/api/tables';
                console.log('📡 API URL:', apiUrl);
                
                fetch(apiUrl)
                    .then(response => {
                        console.log('📡 Tables response status:', response.status);
                        return response.json();
                    })
                    .then(data => {
                        console.log('📊 Tables API response:', data);
                        var tablesContainer = document.getElementById('tablesContainer');
                        tablesContainer.innerHTML = '';
                        
                        if (data.success && data.tables && data.tables.length > 0) {
                            console.log('✅ Tìm thấy', data.tables.length, 'bảng');
                            
                            // Tạo checkbox "Chọn tất cả"
                            var selectAllDiv = document.createElement('div');
                            selectAllDiv.className = 'table-checkbox';
                            selectAllDiv.innerHTML = `
                                <input type="checkbox" id="selectAllTables" onchange="toggleAllTables()">
                                <label for="selectAllTables"><strong>Chọn tất cả bảng</strong></label>
                            `;
                            tablesContainer.appendChild(selectAllDiv);
                            
                            // Thêm đường phân cách
                            var separator = document.createElement('hr');
                            separator.style.margin = '10px 0';
                            tablesContainer.appendChild(separator);
                            
                            data.tables.forEach(table => {
                                var tableDiv = document.createElement('div');
                                tableDiv.className = 'table-checkbox';
                                tableDiv.innerHTML = `
                                    <input type="checkbox" id="table_${table}" name="selectedTables" value="${table}" onchange="updateSelectedTablesCount()">
                                    <label for="table_${table}">${table}</label>
                                `;
                                tablesContainer.appendChild(tableDiv);
                                console.log('➕ Đã thêm bảng:', table);
                            });
                            
                            updateSelectedTablesCount();
                        } else {
                            console.log('❌ Không tìm thấy bảng hoặc lỗi:', data);
                            tablesContainer.innerHTML = `<div style="color: #dc3545; font-style: italic;">${data.success ? 'Không tìm thấy bảng nào trong database này' : ('Lỗi: ' + (data.error || 'Unknown error'))}</div>`;
                        }
                    })
                    .catch(error => {
                        console.error('❌ Error loading tables:', error);
                        document.getElementById('tablesContainer').innerHTML = '<div style="color: #dc3545; font-style: italic;">Lỗi tải danh sách bảng</div>';
                    });
            }
            
            // Khởi tạo Tableau WDC
            var myConnector = tableau.makeConnector();
            
            // Định nghĩa schema động - mỗi bảng riêng biệt (KHÔNG kết hợp)
            myConnector.getSchema = function(schemaCallback) {
                var connectionData = JSON.parse(tableau.connectionData);
                var selectedTables = connectionData.tables;
                var database = connectionData.database;
                
                if (!selectedTables || selectedTables.length === 0) {
                    tableau.abortWithError("Không có bảng nào được chọn");
                    return;
                }
                
                console.log(`🔄 Tạo schema cho ${selectedTables.length} bảng riêng biệt...`);
                
                // Tạo schema riêng cho từng bảng (KHÔNG kết hợp)
                var allSchemas = [];
                var processedCount = 0;
                
                selectedTables.forEach(function(tableName) {
                    var schemaUrl = `/api/schema/${tableName}`;
                    if (database) {
                        schemaUrl += `?database=${encodeURIComponent(database)}`;
                    }
                    
                    fetch(schemaUrl)
                        .then(response => response.json())
                        .then(data => {
                                if (data.success) {
                                // Validate server response
                                if (!data.schema || !Array.isArray(data.schema.columns)) {
                                    console.error('❌ Response schema missing or malformed for', tableName, data);
                                    tableau.abortWithError(`Server returned invalid schema for ${tableName}`);
                                    return;
                                }

                                var cols = data.schema.columns.map(function(col) {
                                    // Basic validation per-column
                                    if (!col || !col.column_name) {
                                        console.error('❌ Column metadata missing column_name:', col, 'for table', tableName);
                                        return null;
                                    }
                                    return {
                                        "id": String(col.column_name),
                                        "alias": String(col.column_name),
                                        "dataType": getTableauDataType(col.tableau_type)
                                    };
                                }).filter(function(c){ return c !== null; });

                                // Ensure columns is not empty
                                if (!cols || cols.length === 0) {
                                    console.error('❌ No columns returned for', tableName, data.schema);
                                    tableau.abortWithError(`Schema for ${tableName} contains no columns`);
                                    return;
                                }

                                // Mỗi bảng là một table riêng biệt trong Tableau
                                // QUAN TRỌNG: Tableau yêu cầu id chỉ chứa [a-zA-Z0-9_]
                                // Thay dấu '.' bằng '_' trong id, nhưng giữ nguyên alias
                                var tableSchema = {
                                    "id": String(tableName).replace(/\./g, '_'),  // SAMPLE.dbo.GIAODICH -> SAMPLE_dbo_GIAODICH
                                    "alias": `${tableName} (${database})`,         // Hiển thị: SAMPLE.dbo.GIAODICH (SAMPLE)
                                    "columns": cols
                                };
                                
                                allSchemas.push(tableSchema);
                                processedCount++;
                                
                                console.log(`✅ Đã tạo schema cho bảng: ${tableName} (id: ${tableSchema.id})`);
                                
                                // Khi đã xử lý xong tất cả bảng
                                if (processedCount === selectedTables.length) {
                                    console.log(`🎉 Hoàn thành tạo ${allSchemas.length} table schema riêng biệt`);
                                    schemaCallback(allSchemas);
                                }
                            } else {
                                tableau.abortWithError(`Không thể lấy schema của bảng ${tableName}`);
                            }
                        })
                        .catch(error => {
                            console.error(`Lỗi lấy schema bảng ${tableName}:`, error);
                            tableau.abortWithError(`Lỗi kết nối server khi lấy schema ${tableName}`);
                        });
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
            
            // Lấy dữ liệu cho từng bảng riêng biệt (KHÔNG kết hợp)
            myConnector.getData = function(table, doneCallback) {
                var connectionData = JSON.parse(tableau.connectionData);
                var selectedTables = connectionData.tables;
                
                if (!selectedTables || selectedTables.length === 0) {
                    tableau.abortWithError("Không có bảng nào được chọn");
                    return;
                }
                
                // Tìm bảng nào đang được load dựa trên table.tableInfo.id
                // LƯU Ý: id đã được replace '.' -> '_', cần map ngược lại
                var tableId = table.tableInfo.id;  // VD: "SAMPLE_dbo_GIAODICH"
                console.log(`🔄 Đang tải dữ liệu cho table id: ${tableId}`);
                
                // Tìm tên bảng gốc từ selectedTables
                var currentTableName = null;
                for (var i = 0; i < selectedTables.length; i++) {
                    var originalName = selectedTables[i];
                    var normalizedId = originalName.replace(/\./g, '_');
                    if (normalizedId === tableId) {
                        currentTableName = originalName;
                        break;
                    }
                }
                
                if (!currentTableName) {
                    tableau.abortWithError(`Không tìm thấy bảng với id: ${tableId}`);
                    return;
                }
                
                console.log(`🔄 Đang tải dữ liệu cho bảng: ${currentTableName}`);
                
                // API endpoint cho bảng hiện tại (dùng tên gốc có dấu chấm)
                var apiUrl = `/api/data/${currentTableName}?limit=${connectionData.limit}&order=${connectionData.order}`;
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
                            console.log(`✅ Đã tải ${data.data.length} dòng từ bảng ${currentTableName}`);
                            table.appendRows(data.data);
                        } else {
                            console.warn(`⚠️ Không có dữ liệu từ bảng ${currentTableName}`);
                        }
                        doneCallback();
                    })
                    .catch(error => {
                        console.error(`❌ Lỗi khi lấy dữ liệu bảng ${currentTableName}:`, error);
                        tableau.abortWithError(`Không thể lấy dữ liệu từ bảng ${currentTableName}`);
                    });
            };
            
            // Đăng ký connector
            tableau.registerConnector(myConnector);
            
            // Xử lý sự kiện submit cho nhiều database & nhiều bảng
            document.getElementById("submitButton").addEventListener("click", function() {
                var selectedDatabases = getSelectedDatabases();
                var selectedTables = getSelectedTables();
                var limit = document.getElementById("limitSelect").value;
                var order = document.getElementById("orderSelect").value;
                var where = document.getElementById("whereInput").value;
                
                if (selectedDatabases.length === 0) {
                    alert("Vui lòng chọn ít nhất một database");
                    return;
                }
                
                if (selectedTables.length === 0) {
                    alert("Vui lòng chọn ít nhất một bảng dữ liệu");
                    return;
                }
                
                // Connection data với format mới
                tableau.connectionData = JSON.stringify({
                    "databases": selectedDatabases,  // Array của database names
                    "tables": selectedTables,         // Array format: ["DB.Table", "DB2.Table2"]
                    "limit": limit,
                    "order": order,
                    "where": where
                });
                
                // Tạo tên connection
                if (selectedDatabases.length === 1 && selectedTables.length === 1) {
                    tableau.connectionName = `${selectedTables[0]} (${limit === '0' ? 'Tất cả' : limit} dòng)`;
                } else if (selectedDatabases.length === 1) {
                    tableau.connectionName = `${selectedDatabases[0]} - ${selectedTables.length} bảng`;
                } else {
                    tableau.connectionName = `${selectedDatabases.length} databases - ${selectedTables.length} bảng`;
                }
                
                console.log("🚀 Kết nối Tableau với:", {
                    databases: selectedDatabases,
                    tables: selectedTables,
                    limit: limit
                });
                
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

@app.route('/api/schema/<path:table_name>')
def get_table_schema(table_name):
    """
    Lấy schema của bảng - hỗ trợ format Database.Schema.Table
    """
    try:
        # Parse table_name để tách database (nếu có)
        # Format có thể là: "Table", "Schema.Table", hoặc "Database.Schema.Table"
        parts = table_name.split('.')
        
        if len(parts) == 3:
            # Format: Database.Schema.Table
            extracted_db = parts[0]
            schema_table = f"{parts[1]}.{parts[2]}"  # Schema.Table
            database_name = extracted_db
            print(f"🔍 Parse format Database.Schema.Table: db='{extracted_db}', table='{schema_table}'")
        elif len(parts) == 2:
            # Format: Schema.Table (dùng database từ query param hoặc config)
            schema_table = table_name  # Giữ nguyên Schema.Table
            database_name = request.args.get('database', None)
            print(f"🔍 Parse format Schema.Table: table='{schema_table}', database='{database_name}'")
        else:
            # Format: Table (chỉ có tên bảng)
            schema_table = table_name
            database_name = request.args.get('database', None)
            print(f"🔍 Parse format Table: table='{schema_table}', database='{database_name}'")
        
        print(f"🔍 Đang lấy schema cho: table='{schema_table}', database='{database_name}'")
        
        schema = tu_dong_phat_hien_schema(schema_table, database_name)
        if schema and schema.get('columns'):
            print(f"✅ Tìm thấy {len(schema.get('columns', []))} cột cho bảng '{schema_table}'")
            return jsonify({
                "success": True,
                "schema": schema
            })
        else:
            print(f"❌ Không tìm thấy schema cho bảng '{schema_table}'")
            return jsonify({
                "success": False,
                "error": f"Không thể lấy schema cho bảng '{schema_table}'"
            })
    except Exception as e:
        print(f"❌ Lỗi khi lấy schema: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/api/data/<path:table_name>')
def get_table_data(table_name):
    """
    Lấy dữ liệu từ bảng - hỗ trợ format Database.Schema.Table
    """
    try:
        config = doc_cau_hinh_database()
        
        # Parse table_name để tách database (nếu có)
        parts = table_name.split('.')
        
        if len(parts) == 3:
            # Format: Database.Schema.Table
            extracted_db = parts[0]
            schema_table = f"{parts[1]}.{parts[2]}"  # Schema.Table
            database_name = extracted_db
            print(f"🔍 Parse format Database.Schema.Table: db='{extracted_db}', table='{schema_table}'")
        elif len(parts) == 2:
            # Format: Schema.Table
            schema_table = table_name
            database_name = request.args.get('database', None)
            print(f"🔍 Parse format Schema.Table: table='{schema_table}', database='{database_name}'")
        else:
            # Format: Table
            schema_table = table_name
            database_name = request.args.get('database', None)
            print(f"🔍 Parse format Table: table='{schema_table}', database='{database_name}'")
        
        db_name = database_name if database_name else config['database']
            
        limit = request.args.get('limit', '1000')
        order = request.args.get('order', 'auto')
        where_clause = request.args.get('where', '')
        
        print(f"🔄 Đang lấy dữ liệu: table='{schema_table}', database='{db_name}', limit={limit}")
        
        # Xây dựng câu truy vấn
        if limit == '0':
            limit_clause = ""
            limit_int = 0
        else:
            limit_clause = f"TOP {limit}"
            limit_int = int(limit)
        
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
        
        query = f"SELECT {limit_clause} * FROM [{schema_table}] {where_sql} {order_clause}"
        
        # Lay du lieu bang module moi
        du_lieu_json, columns = db_conn.lay_du_lieu_bang(schema_table, db_name, limit_int)
        
        print(f"✅ Đã lấy {len(du_lieu_json)} dòng từ '{schema_table}'")
        
        return jsonify({
            "success": True,
            "data": du_lieu_json,
            "count": len(du_lieu_json),
            "table": schema_table,
            "database": db_name,
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "message": f"Lấy dữ liệu từ bảng {schema_table} thành công"
        })
        
    except Exception as e:
        print(f"❌ Lỗi khi lấy dữ liệu: {e}")
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
    print("🎯 TÍNH NĂNG NÂNG CẤP - FOCUS NHIỀU BẢNG:")
    print("  ✅ Chọn nhiều bảng cùng lúc bằng checkbox")
    print("  ✅ Mỗi bảng là một dataset riêng biệt trong Tableau")
    print("  ✅ KHÔNG tự động kết hợp dữ liệu")
    print("  ✅ User có thể chọn từng bảng để phân tích")
    print("  ✅ Hỗ trợ câu truy vấn WHERE tùy chỉnh")
    print("")

    print("⏹️  Nhấn Ctrl+C để dừng server")
    print("=" * 55)
    
    app.run(debug=True, host='127.0.0.1', port=5002)
