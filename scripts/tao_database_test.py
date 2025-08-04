#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo database test nhanh
"""

import pymssql
import json

def tao_database_test():
    """
    Tạo database test đơn giản
    """
    try:
        # Kết nối master
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database='master'
        )
        
        con_tro = ket_noi.cursor()
        
        # Tạo database mới
        database_name = "TestTableauDB"
        
        # Xóa database cũ nếu có
        con_tro.execute(f"IF EXISTS (SELECT * FROM sys.databases WHERE name = '{database_name}') DROP DATABASE [{database_name}]")
        
        # Tạo database mới
        con_tro.execute(f"CREATE DATABASE [{database_name}]")
        ket_noi.commit()
        ket_noi.close()
        
        print(f"✅ Đã tạo database: {database_name}")
        
        # Kết nối database mới và tạo bảng
        ket_noi_moi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database=database_name
        )
        
        con_tro_moi = ket_noi_moi.cursor()
        
        # Tạo bảng test
        con_tro_moi.execute("""
        CREATE TABLE test_data (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name NVARCHAR(100),
            value DECIMAL(10,2),
            created_date DATETIME DEFAULT GETDATE()
        )
        """)
        
        # Thêm dữ liệu test
        test_data = [
            ('Sản phẩm A', 100.50),
            ('Sản phẩm B', 200.75),
            ('Sản phẩm C', 300.25),
            ('Sản phẩm D', 150.00),
            ('Sản phẩm E', 250.80)
        ]
        
        for name, value in test_data:
            con_tro_moi.execute("INSERT INTO test_data (name, value) VALUES (%s, %s)", (name, value))
        
        ket_noi_moi.commit()
        ket_noi_moi.close()
        
        print("✅ Đã tạo bảng test_data với 5 dòng dữ liệu")
        
        # Cập nhật config
        config = {
            "server": "127.0.0.1",
            "port": 1235,
            "user": "sa",
            "password": "YourStrong!Pass123",
            "database": database_name
        }
        
        with open("config/database_config.json", "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("✅ Đã cập nhật config/database_config.json")
        print(f"🎯 Database hiện tại: {database_name}")
        print("🚀 Bây giờ có thể chạy Universal Connector!")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

if __name__ == "__main__":
    print("🗄️ TẠO DATABASE TEST CHO TABLEAU CONNECTOR")
    print("=" * 50)
    tao_database_test()
