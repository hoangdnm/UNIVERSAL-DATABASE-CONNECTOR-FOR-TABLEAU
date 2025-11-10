#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schema Detector Module
Phát hiện và xử lý schema của bảng database
"""

import json
import os
import sys

# Import database connector
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database_connector as db_conn


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
    
    Args:
        ten_bang (str): Tên bảng cần lấy schema
        database_name (str, optional): Tên database. Mặc định lấy từ config
    
    Returns:
        dict: Dictionary chứa thông tin schema bảng
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


def parse_table_name(table_name, request_args):
    """
    Phân tích tên bảng để tách database, schema, table
    
    Args:
        table_name (str): Tên bảng (có thể là "Table", "Schema.Table", "Database.Schema.Table")
        request_args (dict): Request arguments chứa database parameter
    
    Returns:
        tuple: (schema_table, database_name)
    """
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
        database_name = request_args.get('database', None)
        print(f"🔍 Parse format Schema.Table: table='{schema_table}', database='{database_name}'")
    else:
        # Format: Table
        schema_table = table_name
        database_name = request_args.get('database', None)
        print(f"🔍 Parse format Table: table='{schema_table}', database='{database_name}'")
    
    return schema_table, database_name
