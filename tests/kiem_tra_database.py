#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script kiểm tra database có sẵn trong SQL Server"""

import pymssql

try:
    # Kết nối SQL Server
    conn = pymssql.connect(
        server='127.0.0.1',
        port=1235,
        user='sa',
        password='YourStrong!Pass123',
        database='master'
    )
    
    cur = conn.cursor()
    
    # Lấy danh sách database
    cur.execute("""
        SELECT name, create_date 
        FROM sys.databases 
        WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
        ORDER BY name
    """)
    
    databases = cur.fetchall()
    
    print("=" * 60)
    print("📊 DANH SÁCH DATABASE HIỆN CÓ")
    print("=" * 60)
    
    if databases:
        print(f"\n✅ Tìm thấy {len(databases)} database:\n")
        for db_name, create_date in databases:
            # Lấy số bảng trong database
            cur.execute(f"""
                SELECT COUNT(*) 
                FROM [{db_name}].INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)
            so_bang = cur.fetchone()[0]
            
            # Tổng số dòng
            cur.execute(f"""
                SELECT SUM(p.rows) 
                FROM [{db_name}].sys.tables t
                INNER JOIN [{db_name}].sys.partitions p ON t.object_id = p.object_id
                WHERE p.index_id IN (0,1)
            """)
            tong_dong = cur.fetchone()[0] or 0
            
            print(f"   📁 {db_name}")
            print(f"      • Số bảng: {so_bang}")
            print(f"      • Tổng dòng: {tong_dong:,}")
            print(f"      • Ngày tạo: {create_date.strftime('%d/%m/%Y %H:%M')}")
            print()
    else:
        print("\n❌ Chưa có database nào (ngoài system databases)")
        print("\n💡 Chạy script tạo database:")
        print("   python scripts/tao_3_database_500_dong.py")
    
    conn.close()
    
except Exception as e:
    print(f"❌ Lỗi kết nối SQL Server: {e}")
    print("\n💡 Kiểm tra:")
    print("   1. Docker SQL Server đang chạy: docker ps | grep mssql")
    print("   2. Start container: cd config && docker compose up -d")
