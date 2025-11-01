# -*- coding: utf-8 -*-
"""
Module ket noi SQL Server
Ho tro ca pymssql (SQL Auth) va pyodbc (Windows Auth)
"""

import pyodbc
import pymssql
import json
import os


def doc_cau_hinh_database():
    """
    Doc cau hinh database tu file
    """
    # Tim file config
    possible_paths = [
        "config/database_config.json",
        "../config/database_config.json",
    ]
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    config_path_1 = os.path.join(project_dir, "config", "database_config.json")
    
    possible_paths.insert(0, config_path_1)
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            with open(abs_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    # Cau hinh mac dinh (container hiện tại)
    return {
        'server': '127.0.0.1',
        'port': 1433,  # Container đang dùng port 1433
        'user': 'sa',
        'password': 'YourStrong!Pass123',
        'database': 'master',
        'windows_auth': False
    }


def tao_ket_noi(database_name=None):
    """
    Tao ket noi SQL Server
    Tu dong chon pymssql hoac pyodbc tuy theo cau hinh
    """
    config = doc_cau_hinh_database()
    
    if database_name:
        config['database'] = database_name
    
    windows_auth = config.get('windows_auth', False)
    
    if windows_auth:
        # Dung pyodbc voi Windows Authentication
        return tao_ket_noi_pyodbc(config)
    else:
        # Dung pymssql voi SQL Server Authentication
        return tao_ket_noi_pymssql(config)


def tao_ket_noi_pyodbc(config):
    """
    Tao ket noi bang pyodbc (ho tro Windows Auth)
    """
    server = config.get('server', '127.0.0.1')
    port = config.get('port', 1433)
    database = config.get('database', 'master')
    windows_auth = config.get('windows_auth', False)
    
    if windows_auth:
        # Windows Authentication
        conn_str = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={server},{port};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes"
        )
    else:
        # SQL Server Authentication
        user = config.get('user', 'sa')
        password = config.get('password', '')
        conn_str = (
            f"DRIVER={{SQL Server}};"
            f"SERVER={server},{port};"
            f"DATABASE={database};"
            f"UID={user};"
            f"PWD={password}"
        )
    
    return pyodbc.connect(conn_str, timeout=10)


def tao_ket_noi_pymssql(config):
    """
    Tao ket noi bang pymssql (chi SQL Server Auth)
    """
    return pymssql.connect(
        server=config.get('server', '127.0.0.1'),
        port=config.get('port', 1433),
        user=config.get('user', 'sa'),
        password=config.get('password', 'YourStrong!Pass123'),
        database=config.get('database', 'master'),
        charset='utf8'
    )


def thuc_thi_query(query, database_name=None, params=None):
    """
    Thuc thi query va tra ve ket qua
    """
    try:
        conn = tao_ket_noi(database_name)
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Lay ket qua
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description] if cursor.description else []
            conn.close()
            return results, columns
        else:
            conn.commit()
            conn.close()
            return None, None
            
    except Exception as e:
        print(f"Loi thuc thi query: {e}")
        raise


def lay_danh_sach_database():
    """
    Lay danh sach tat ca databases
    """
    try:
        query = """
        SELECT name 
        FROM sys.databases 
        WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
        ORDER BY name
        """
        results, _ = thuc_thi_query(query, 'master')
        return [db[0] for db in results]
    except Exception as e:
        print(f"Loi lay danh sach database: {e}")
        return []


def lay_danh_sach_bang(database_name=None):
    """
    Lay danh sach tat ca bang trong database
    Tra ve format: 'Schema.Table' (vi du: 'dbo.Users', 'Spend.GIAODICH_FINAL')
    """
    try:
        query = """
        SELECT TABLE_SCHEMA, TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_SCHEMA, TABLE_NAME
        """
        results, _ = thuc_thi_query(query, database_name)
        # Tra ve format Schema.Table
        return [f"{schema}.{table}" for schema, table in results]
    except Exception as e:
        print(f"Loi lay danh sach bang: {e}")
        return []


def lay_schema_bang(ten_bang, database_name=None):
    """
    Lay schema cua bang
    Ho tro ca format: 'Table' hoac 'Schema.Table'
    """
    try:
        # Tach schema va table name neu co
        if '.' in ten_bang:
            parts = ten_bang.split('.', 1)
            schema_name = parts[0]
            table_name = parts[1]
        else:
            schema_name = 'dbo'  # Default schema
            table_name = ten_bang
        
        # Su dung parameterized query de tranh SQL injection
        query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            IS_NULLABLE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = ? AND TABLE_NAME = ?
        ORDER BY ORDINAL_POSITION
        """
        
        results, _ = thuc_thi_query(query, database_name, (schema_name, table_name))
        
        columns = []
        for ten_cot, data_type, max_length, is_nullable in results:
            # Chuyen doi SQL Server data type sang Tableau data type
            if data_type in ['int', 'bigint', 'smallint', 'tinyint']:
                tableau_type = 'int'
            elif data_type in ['decimal', 'numeric', 'float', 'real', 'money']:
                tableau_type = 'float'
            elif data_type in ['datetime', 'datetime2', 'date', 'time', 'smalldatetime']:
                tableau_type = 'datetime'
            elif data_type in ['bit']:
                tableau_type = 'bool'
            else:
                tableau_type = 'string'
            
            columns.append({
                'column_name': ten_cot,
                'sql_type': data_type,
                'tableau_type': tableau_type,
                'max_length': max_length,
                'nullable': is_nullable == 'YES'
            })
        
        return columns
        
    except Exception as e:
        print(f"Loi lay schema bang: {e}")
        return []


def lay_du_lieu_bang(ten_bang, database_name=None, limit=1000):
    """
    Lay du lieu tu bang
    Ho tro ca format: 'Table' hoac 'Schema.Table'
    """
    try:
        # Tach schema va table name neu co
        if '.' in ten_bang:
            parts = ten_bang.split('.', 1)
            schema_name = parts[0]
            table_name = parts[1]
            full_table_name = f"[{schema_name}].[{table_name}]"
        else:
            full_table_name = f"[dbo].[{ten_bang}]"
        
        # Su dung TOP thay vi LIMIT cho SQL Server
        query = f"SELECT TOP {limit} * FROM {full_table_name}"
        results, columns = thuc_thi_query(query, database_name)
        
        # Chuyen doi thanh list of dict
        data = []
        for row in results:
            row_dict = {}
            for i, col_name in enumerate(columns):
                value = row[i]
                # Chuyen doi datetime thanh string
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                row_dict[col_name] = value
            data.append(row_dict)
        
        return data, columns
        
    except Exception as e:
        print(f"Loi lay du lieu bang: {e}")
        return [], []
