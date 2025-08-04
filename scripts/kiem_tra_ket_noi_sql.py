#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm tra kết nối SQL Server
Dự án tốt nghiệp - Tableau Universal Database Connector
"""

import pymssql
import json
import os

def kiem_tra_cau_hinh():
    """
    Kiểm tra và hiển thị cấu hình database
    """
    print("🔧 KIỂM TRA CẤU HÌNH DATABASE")
    print("=" * 50)
    
    config_path = "config/database_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print(f"📄 File cấu hình: {config_path}")
        print(f"🖥️  Server: {config['server']}")
        print(f"🔌 Port: {config['port']}")
        print(f"👤 User: {config['user']}")
        print(f"🗄️  Database: {config['database']}")
        print(f"🔑 Password: {'*' * len(config['password'])}")
        
        return config
    else:
        print(f"❌ Không tìm thấy file cấu hình: {config_path}")
        return None

def kiem_tra_ket_noi_co_ban(config):
    """
    Kiểm tra kết nối cơ bản đến SQL Server
    """
    print(f"\n🔗 KIỂM TRA KẾT NỐI CƠ BẢN")
    print("=" * 50)
    
    try:
        print(f"⏳ Đang kết nối đến {config['server']}:{config['port']}...")
        
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='master'  # Kết nối master trước
        )
        
        print("✅ Kết nối master database thành công!")
        
        con_tro = ket_noi.cursor()
        con_tro.execute("SELECT @@VERSION")
        phien_ban = con_tro.fetchone()[0]
        print(f"📊 Phiên bản SQL Server: {phien_ban[:50]}...")
        
        ket_noi.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return False

def kiem_tra_danh_sach_database(config):
    """
    Kiểm tra danh sách các database có sẵn
    """
    print(f"\n📂 KIỂM TRA DANH SÁCH DATABASE")
    print("=" * 50)
    
    try:
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='master'
        )
        
        con_tro = ket_noi.cursor()
        con_tro.execute("SELECT name FROM sys.databases WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb') ORDER BY name")
        
        databases = con_tro.fetchall()
        
        if databases:
            print(f"✅ Tìm thấy {len(databases)} database:")
            for i, db in enumerate(databases, 1):
                print(f"   {i}. {db[0]}")
        else:
            print("⚠️ Không tìm thấy database nào (ngoài system databases)")
            print("💡 Gợi ý: Hãy tạo database mới hoặc kiểm tra quyền truy cập")
        
        ket_noi.close()
        return [db[0] for db in databases]
        
    except Exception as e:
        print(f"❌ Lỗi lấy danh sách database: {e}")
        return []

def kiem_tra_database_cu_the(config, ten_database):
    """
    Kiểm tra kết nối đến database cụ thể
    """
    print(f"\n🗄️ KIỂM TRA DATABASE CỤ THỂ: {ten_database}")
    print("=" * 50)
    
    try:
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=ten_database
        )
        
        print(f"✅ Kết nối database '{ten_database}' thành công!")
        
        con_tro = ket_noi.cursor()
        
        # Kiểm tra số lượng bảng
        con_tro.execute("""
        SELECT COUNT(*) 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        """)
        so_bang = con_tro.fetchone()[0]
        print(f"📋 Số lượng bảng: {so_bang}")
        
        # Lấy danh sách bảng
        con_tro.execute("""
        SELECT TABLE_NAME 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_TYPE = 'BASE TABLE'
        ORDER BY TABLE_NAME
        """)
        
        bang_list = con_tro.fetchall()
        if bang_list:
            print(f"📊 Danh sách bảng:")
            for i, bang in enumerate(bang_list[:5], 1):  # Chỉ hiển thị 5 bảng đầu
                print(f"   {i}. {bang[0]}")
            if len(bang_list) > 5:
                print(f"   ... và {len(bang_list) - 5} bảng khác")
        
        ket_noi.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi kết nối database '{ten_database}': {e}")
        return False

def kiem_tra_thu_vien():
    """
    Kiểm tra các thư viện cần thiết
    """
    print(f"\n📦 KIỂM TRA THƯ VIỆN")
    print("=" * 50)
    
    try:
        import pymssql
        print(f"✅ pymssql: phiên bản {pymssql.__version__}")
    except Exception as e:
        print(f"❌ pymssql: {e}")
        return False
    
    try:
        import flask
        print(f"✅ flask: phiên bản {flask.__version__}")
    except Exception as e:
        print(f"❌ flask: {e}")
        return False
    
    return True

def main():
    """
    Hàm chính - thực hiện tất cả kiểm tra
    """
    print("🔍 KIỂM TRA TOÀN DIỆN HỆ THỐNG")
    print("=" * 60)
    print("📋 Sẽ kiểm tra:")
    print("  1️⃣ Thư viện cần thiết")
    print("  2️⃣ Cấu hình database")
    print("  3️⃣ Kết nối SQL Server")
    print("  4️⃣ Danh sách database")
    print("  5️⃣ Database cụ thể")
    print("")
    
    # 1. Kiểm tra thư viện
    if not kiem_tra_thu_vien():
        print("\n❌ KIỂM TRA THẤT BẠI: Thiếu thư viện cần thiết")
        return
    
    # 2. Kiểm tra cấu hình
    config = kiem_tra_cau_hinh()
    if not config:
        print("\n❌ KIỂM TRA THẤT BẠI: Không có file cấu hình")
        return
    
    # 3. Kiểm tra kết nối cơ bản
    if not kiem_tra_ket_noi_co_ban(config):
        print("\n❌ KIỂM TRA THẤT BẠI: Không thể kết nối SQL Server")
        print("\n🔧 HƯỚNG DẪN KHẮC PHỤC:")
        print("  1. Kiểm tra Docker đang chạy: docker ps")
        print("  2. Khởi động SQL Server: docker-compose up -d")
        print("  3. Kiểm tra port 1235 có bị chiếm: netstat -an | findstr 1235")
        return
    
    # 4. Kiểm tra danh sách database
    databases = kiem_tra_danh_sach_database(config)
    
    # 5. Kiểm tra database cụ thể (nếu có)
    if config['database'] != 'master':
        kiem_tra_database_cu_the(config, config['database'])
    elif databases:
        # Kiểm tra database đầu tiên trong danh sách
        kiem_tra_database_cu_the(config, databases[0])
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("🎉 KIỂM TRA HOÀN TẤT!")
    print("=" * 60)
    
    if databases:
        print("✅ HỆ THỐNG HOẠT ĐỘNG BÌNH THƯỜNG")
        print(f"📊 Tìm thấy {len(databases)} database")
        print(f"🔗 Server: {config['server']}:{config['port']}")
        print("")
        print("💡 HƯỚNG DẪN TIẾP THEO:")
        print("  1. Chạy Universal Connector: python src/tableau_universal_connector.py")
        print("  2. Mở trình duyệt: http://127.0.0.1:5002")
        print("  3. Chọn database và bảng cần kết nối")
    else:
        print("⚠️ HỆ THỐNG HOẠT ĐỘNG NHƯNG CHƯA CÓ DATABASE")
        print("")
        print("💡 HƯỚNG DẪN TẠO DATABASE:")
        print("  1. Chạy script tạo database: python scripts/khoi_tao_database.py")
        print("  2. Hoặc tạo database bằng SQL Management Studio")
        print("  3. Sau đó chạy lại kiểm tra này")

if __name__ == "__main__":
    main()
