#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script cấu hình kết nối database linh hoạt
Dự án tốt nghiệp - Tableau Universal Database Connector

Mục đích: Kết nối Tableau với bất kỳ SQL Server database nào
"""

import json
import os

def tao_config_ket_noi():
    """
    Tạo file cấu hình kết nối database linh hoạt
    """
    print("🔧 CẤU HÌNH KẾT NỐI DATABASE")
    print("=" * 50)
    
    config = {}
    
    # Thông tin server
    print("\n📡 THÔNG TIN SERVER:")
    config['server'] = input("Server (mặc định: 127.0.0.1): ").strip() or "127.0.0.1"
    config['port'] = int(input("Port (mặc định: 1433): ").strip() or "1433")
    config['user'] = input("Username (mặc định: sa): ").strip() or "sa"
    config['password'] = input("Password: ").strip() or "YourStrong!Pass123"
    
    # Danh sách databases có sẵn
    print("\n📊 CHỌN DATABASE:")
    print("1. Nhập tên database có sẵn")
    print("2. Liệt kê tất cả databases trên server")
    
    lua_chon = input("Chọn cách (1-2): ").strip()
    
    if lua_chon == "2":
        # Kết nối để liệt kê databases
        try:
            import pymssql
            ket_noi = pymssql.connect(
                server=config['server'],
                port=config['port'],
                user=config['user'],
                password=config['password']
            )
            
            con_tro = ket_noi.cursor()
            con_tro.execute("SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')")
            databases = con_tro.fetchall()
            
            print("\n📋 Databases có sẵn:")
            for i, db in enumerate(databases, 1):
                print(f"{i}. {db[0]}")
            
            if databases:
                chon_db = int(input(f"Chọn database (1-{len(databases)}): ")) - 1
                config['database'] = databases[chon_db][0]
            else:
                print("❌ Không tìm thấy database nào")
                config['database'] = input("Nhập tên database: ").strip()
            
            ket_noi.close()
            
        except Exception as e:
            print(f"⚠️ Không thể kết nối: {e}")
            config['database'] = input("Nhập tên database: ").strip()
    else:
        config['database'] = input("Tên database: ").strip()
    
    # Lưu config
    config_path = "config/database_config.json"
    os.makedirs("config", exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Đã lưu cấu hình vào: {config_path}")
    return config

def kiem_tra_bang_trong_database(config):
    """
    Liệt kê tất cả bảng trong database
    """
    print(f"\n📊 LIỆT KÊ BẢNG TRONG DATABASE: {config['database']}")
    print("-" * 50)
    
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
        
        # Lấy danh sách bảng
        con_tro.execute("""
        SELECT TABLE_NAME, TABLE_TYPE 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """)
        
        bang_list = con_tro.fetchall()
        
        print(f"📋 Tìm thấy {len(bang_list)} bảng:")
        for i, (ten_bang, loai_bang) in enumerate(bang_list, 1):
            # Đếm số dòng trong bảng
            try:
                con_tro.execute(f"SELECT COUNT(*) FROM [{ten_bang}]")
                so_dong = con_tro.fetchone()[0]
                print(f"{i:2d}. {ten_bang} ({so_dong:,} dòng)")
            except:
                print(f"{i:2d}. {ten_bang} (không đếm được)")
        
        ket_noi.close()
        return [bang[0] for bang in bang_list]
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return []

def phan_tich_cau_truc_bang(config, ten_bang):
    """
    Phân tích cấu trúc của bảng để tự động tạo schema
    """
    print(f"\n🔍 PHÂN TÍCH BẢNG: {ten_bang}")
    print("-" * 50)
    
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
        
        # Lấy thông tin cột
        con_tro.execute(f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            CHARACTER_MAXIMUM_LENGTH,
            NUMERIC_PRECISION,
            NUMERIC_SCALE
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{ten_bang}'
        ORDER BY ORDINAL_POSITION
        """)
        
        cot_list = con_tro.fetchall()
        
        print("📋 Cấu trúc bảng:")
        schema_info = []
        
        for cot in cot_list:
            ten_cot, data_type, nullable, max_len, precision, scale = cot
            
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
            
            schema_info.append({
                'column_name': ten_cot,
                'sql_type': data_type,
                'tableau_type': tableau_type,
                'nullable': nullable == 'YES'
            })
            
            nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
            print(f"  - {ten_cot:<20} {data_type:<15} {nullable_str:<10} → {tableau_type}")
        
        # Lấy dữ liệu mẫu
        print(f"\n📊 Dữ liệu mẫu (5 dòng đầu):")
        con_tro.execute(f"SELECT TOP 5 * FROM [{ten_bang}]")
        du_lieu_mau = con_tro.fetchall()
        
        if du_lieu_mau:
            # In header
            ten_cot_list = [info['column_name'] for info in schema_info]
            print(" | ".join(f"{ten:<15}" for ten in ten_cot_list[:5]))  # Chỉ hiển thị 5 cột đầu
            print("-" * 80)
            
            # In dữ liệu
            for dong in du_lieu_mau:
                dong_str = []
                for i, gia_tri in enumerate(dong[:5]):  # Chỉ hiển thị 5 cột đầu
                    if gia_tri is None:
                        dong_str.append("NULL".ljust(15))
                    else:
                        dong_str.append(str(gia_tri)[:15].ljust(15))
                print(" | ".join(dong_str))
        
        ket_noi.close()
        
        # Lưu schema info
        schema_path = f"config/schema_{ten_bang}.json"
        with open(schema_path, 'w', encoding='utf-8') as f:
            json.dump({
                'table_name': ten_bang,
                'columns': schema_info,
                'database': config['database']
            }, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Đã lưu schema vào: {schema_path}")
        return schema_info
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return []

def main():
    """
    Hàm chính
    """
    print("🚀 TABLEAU UNIVERSAL DATABASE CONNECTOR")
    print("🎯 Kết nối Tableau với bất kỳ SQL Server database nào")
    print("=" * 60)
    
    # Bước 1: Cấu hình kết nối
    config = tao_config_ket_noi()
    
    # Bước 2: Liệt kê bảng
    bang_list = kiem_tra_bang_trong_database(config)
    
    if not bang_list:
        print("❌ Không tìm thấy bảng nào trong database")
        return
    
    # Bước 3: Chọn bảng để phân tích
    print(f"\n📊 Chọn bảng để phân tích:")
    for i, ten_bang in enumerate(bang_list, 1):
        print(f"{i}. {ten_bang}")
    
    try:
        chon_bang = int(input(f"Chọn bảng (1-{len(bang_list)}): ")) - 1
        ten_bang_chon = bang_list[chon_bang]
        
        # Bước 4: Phân tích bảng
        schema_info = phan_tich_cau_truc_bang(config, ten_bang_chon)
        
        if schema_info:
            print("\n" + "=" * 60)
            print("✅ HOÀN THÀNH CẤU HÌNH!")
            print(f"📊 Database: {config['database']}")
            print(f"📋 Bảng: {ten_bang_chon}")
            print(f"🔧 Cấu hình: config/database_config.json")
            print(f"📈 Schema: config/schema_{ten_bang_chon}.json")
            print("")
            print("🌐 Bước tiếp theo:")
            print("   1. Cập nhật API để sử dụng cấu hình mới")
            print("   2. Chạy: python tableau_web_data_connector.py")
            print("   3. Kết nối Tableau tại: http://127.0.0.1:5002")
        
    except (ValueError, IndexError):
        print("❌ Lựa chọn không hợp lệ")

if __name__ == "__main__":
    main()
