#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Routes Module
Chứa tất cả các API endpoints
"""

from flask import jsonify, request
from datetime import datetime
import sys
import os

# Import schema detector
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.schema_detector import (
    doc_cau_hinh_database,
    lay_danh_sach_database,
    lay_danh_sach_bang,
    tu_dong_phat_hien_schema,
    parse_table_name
)
import database_connector as db_conn


def register_routes(app):
    """
    Đăng ký tất cả API routes cho Flask app
    
    Args:
        app: Flask application instance
    """
    
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
            schema_table, database_name = parse_table_name(table_name, request.args)
            
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
            schema_table, database_name = parse_table_name(table_name, request.args)
            
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
            
            # Lay du lieu bang module database_connector
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
