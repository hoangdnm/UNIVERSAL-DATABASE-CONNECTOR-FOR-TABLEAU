#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm thử khả năng làm việc với database mới và cập nhật real-time
Dự án tốt nghiệp - Tableau Universal Database Connector

Test 2 tình huống:
1. Tạo database mới và kết nối
2. Cập nhật dữ liệu và xem real-time trong Tableau
"""

import json
import os
import sys
import pymssql
from datetime import datetime, timedelta
import random
import time

def tao_database_test_moi():
    """
    Tạo một database mới để test
    """
    print("🗄️ KIỂM THỬ: TẠO DATABASE MỚI")
    print("=" * 50)
    
    ten_database_moi = "TestDatabase_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Kết nối master để tạo database mới
        ket_noi_master = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database='master'
        )
        
        con_tro = ket_noi_master.cursor()
        
        # Tạo database mới
        print(f"📊 Đang tạo database: {ten_database_moi}")
        con_tro.execute(f"CREATE DATABASE [{ten_database_moi}]")
        ket_noi_master.commit()
        ket_noi_master.close()
        
        print(f"✅ Tạo database {ten_database_moi} thành công!")
        
        # Kết nối database mới và tạo bảng test
        ket_noi_moi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database=ten_database_moi
        )
        
        con_tro_moi = ket_noi_moi.cursor()
        
        # Tạo bảng sản phẩm
        print("📋 Đang tạo bảng: bang_san_pham")
        con_tro_moi.execute("""
        CREATE TABLE bang_san_pham (
            id_san_pham INT IDENTITY(1,1) PRIMARY KEY,
            ten_san_pham NVARCHAR(100) NOT NULL,
            gia_ban DECIMAL(10,2) NOT NULL,
            so_luong_ton INT NOT NULL,
            ngay_nhap DATETIME DEFAULT GETDATE(),
            danh_muc NVARCHAR(50),
            ghi_chu NVARCHAR(255)
        )
        """)
        
        # Thêm dữ liệu mẫu
        print("📊 Đang thêm dữ liệu mẫu...")
        danh_sach_san_pham = [
            ('Laptop Dell XPS 13', 25000000, 15, 'Máy tính', 'Laptop cao cấp'),
            ('iPhone 15 Pro', 30000000, 20, 'Điện thoại', 'Điện thoại Apple mới nhất'),
            ('Samsung Galaxy S24', 22000000, 25, 'Điện thoại', 'Điện thoại Samsung flagship'),
            ('MacBook Air M2', 28000000, 10, 'Máy tính', 'Laptop Apple'),
            ('iPad Pro 12.9', 35000000, 12, 'Máy tính bảng', 'Máy tính bảng cao cấp'),
            ('AirPods Pro', 6000000, 50, 'Tai nghe', 'Tai nghe không dây Apple'),
            ('Sony WH-1000XM5', 8000000, 30, 'Tai nghe', 'Tai nghe chống ồn Sony'),
            ('Apple Watch Series 9', 12000000, 18, 'Đồng hồ thông minh', 'Đồng hồ thông minh Apple'),
            ('Gaming Chair', 5000000, 8, 'Ghế gaming', 'Ghế chơi game cao cấp'),
            ('Monitor 4K Dell', 15000000, 6, 'Màn hình', 'Màn hình 4K chuyên nghiệp')
        ]
        
        for san_pham in danh_sach_san_pham:
            con_tro_moi.execute("""
            INSERT INTO bang_san_pham (ten_san_pham, gia_ban, so_luong_ton, danh_muc, ghi_chu)
            VALUES (%s, %s, %s, %s, %s)
            """, san_pham)
        
        ket_noi_moi.commit()
        
        # Kiểm tra dữ liệu đã thêm
        con_tro_moi.execute("SELECT COUNT(*) FROM bang_san_pham")
        so_dong = con_tro_moi.fetchone()[0]
        print(f"✅ Đã thêm {so_dong} sản phẩm vào database")
        
        ket_noi_moi.close()
        
        return ten_database_moi
        
    except Exception as e:
        print(f"❌ Lỗi tạo database mới: {e}")
        return None

def cap_nhat_config_database(ten_database_moi):
    """
    Cập nhật file config để trỏ đến database mới
    """
    print(f"\n🔧 KIỂM THỬ: CẬP NHẬT CẤU HÌNH DATABASE")
    print("=" * 50)
    
    try:
        # Backup config cũ
        config_path = "config/database_config.json"
        backup_path = "config/database_config_backup.json"
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_cu = json.load(f)
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(config_cu, f, indent=2, ensure_ascii=False)
            print(f"💾 Đã backup config cũ vào: {backup_path}")
        
        # Tạo config mới
        config_moi = {
            "server": "127.0.0.1",
            "port": 1235,
            "user": "sa",
            "password": "YourStrong!Pass123",
            "database": ten_database_moi
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_moi, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Đã cập nhật config để sử dụng database: {ten_database_moi}")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi cập nhật config: {e}")
        return False

def test_universal_connector_voi_database_moi(ten_database_moi):
    """
    Test xem Universal Connector có hoạt động với database mới không
    """
    print(f"\n🌐 KIỂM THỬ: UNIVERSAL CONNECTOR VỚI DATABASE MỚI")
    print("=" * 50)
    
    try:
        # Import Universal Connector
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
        from tableau_universal_connector import app, lay_danh_sach_bang, doc_schema_bang
        
        # Test 1: Lấy danh sách bảng
        print("📋 Test 1: Lấy danh sách bảng")
        bang_list = lay_danh_sach_bang()
        print(f"   ✅ Tìm thấy {len(bang_list)} bảng: {bang_list}")
        
        # Test 2: Lấy schema của bảng
        print("\n📊 Test 2: Phát hiện schema tự động")
        if 'bang_san_pham' in bang_list:
            schema = doc_schema_bang('bang_san_pham')
            if schema:
                print(f"   ✅ Schema bảng bang_san_pham:")
                for cot in schema['columns']:
                    print(f"      - {cot['column_name']}: {cot['sql_type']} → {cot['tableau_type']}")
            else:
                print("   ❌ Không lấy được schema")
                return False
        
        # Test 3: Test API endpoints
        print("\n🌐 Test 3: API endpoints")
        with app.test_client() as client:
            # Test database info
            response = client.get('/api/database-info')
            if response.status_code == 200:
                data = response.get_json()
                if data['success']:
                    print(f"   ✅ Database info: {data['database']} ({data['table_count']} bảng)")
                else:
                    print(f"   ❌ API lỗi: {data.get('error')}")
                    return False
            
            # Test tables list
            response = client.get('/api/tables')
            if response.status_code == 200:
                data = response.get_json()
                if data['success']:
                    print(f"   ✅ Tables API: {len(data['tables'])} bảng")
                else:
                    print(f"   ❌ Tables API lỗi: {data.get('error')}")
                    return False
            
            # Test data API
            response = client.get('/api/data/bang_san_pham?limit=5')
            if response.status_code == 200:
                data = response.get_json()
                if data['success']:
                    print(f"   ✅ Data API: {data['count']} dòng dữ liệu")
                    print(f"      Query: {data.get('query', 'N/A')}")
                else:
                    print(f"   ❌ Data API lỗi: {data.get('error')}")
                    return False
        
        print(f"\n🎉 UNIVERSAL CONNECTOR HOẠT ĐỘNG HOÀN HẢO VỚI DATABASE MỚI!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test Universal Connector: {e}")
        return False

def test_cap_nhat_real_time():
    """
    Test khả năng cập nhật dữ liệu real-time
    """
    print(f"\n⚡ KIỂM THỬ: CẬP NHẬT DỮ LIỆU REAL-TIME")
    print("=" * 50)
    
    try:
        # Đọc config hiện tại
        with open("config/database_config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Kết nối database
        ket_noi = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        
        con_tro = ket_noi.cursor()
        
        # Lấy số lượng dòng ban đầu
        con_tro.execute("SELECT COUNT(*) FROM bang_san_pham")
        so_dong_ban_dau = con_tro.fetchone()[0]
        print(f"📊 Số dòng ban đầu: {so_dong_ban_dau}")
        
        # Thêm dữ liệu mới
        print("⏳ Đang thêm dữ liệu mới...")
        san_pham_moi = [
            (f'Sản phẩm mới {datetime.now().strftime("%H:%M:%S")}', 
             random.randint(1000000, 50000000), 
             random.randint(1, 100), 
             'Hàng mới', 
             'Được thêm trong test real-time'),
            (f'Gadget {datetime.now().strftime("%H:%M:%S")}', 
             random.randint(500000, 20000000), 
             random.randint(5, 50), 
             'Phụ kiện', 
             'Test cập nhật real-time')
        ]
        
        for sp in san_pham_moi:
            con_tro.execute("""
            INSERT INTO bang_san_pham (ten_san_pham, gia_ban, so_luong_ton, danh_muc, ghi_chu)
            VALUES (%s, %s, %s, %s, %s)
            """, sp)
        
        ket_noi.commit()
        
        # Kiểm tra dữ liệu mới
        con_tro.execute("SELECT COUNT(*) FROM bang_san_pham")
        so_dong_moi = con_tro.fetchone()[0]
        print(f"✅ Đã thêm {so_dong_moi - so_dong_ban_dau} dòng mới")
        print(f"📊 Tổng số dòng hiện tại: {so_dong_moi}")
        
        # Test API với dữ liệu mới
        print("\n🌐 Test API với dữ liệu mới:")
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
        from tableau_universal_connector import app
        
        with app.test_client() as client:
            response = client.get('/api/data/bang_san_pham?limit=0&order=auto')
            if response.status_code == 200:
                data = response.get_json()
                if data['success']:
                    print(f"   ✅ API trả về {data['count']} dòng (bao gồm dữ liệu mới)")
                    print(f"   ⏰ Timestamp: {data.get('timestamp')}")
                    
                    # Hiển thị 3 dòng cuối (dữ liệu mới nhất)
                    print("   📊 3 dòng dữ liệu mới nhất:")
                    for i, dong in enumerate(data['data'][-3:], 1):
                        print(f"      {i}. {dong.get('ten_san_pham', 'N/A')} - {dong.get('gia_ban', 0):,}đ")
                else:
                    print(f"   ❌ API lỗi: {data.get('error')}")
                    return False
        
        # Cập nhật giá sản phẩm để test real-time
        print("\n💰 Test cập nhật giá sản phẩm:")
        con_tro.execute("UPDATE bang_san_pham SET gia_ban = gia_ban * 1.1 WHERE id_san_pham <= 3")
        ket_noi.commit()
        print("   ✅ Đã tăng giá 10% cho 3 sản phẩm đầu tiên")
        
        # Kiểm tra cập nhật trong API
        with app.test_client() as client:
            response = client.get('/api/data/bang_san_pham?limit=3&order=auto')
            if response.status_code == 200:
                data = response.get_json()
                if data['success']:
                    print("   📊 Giá sản phẩm sau khi cập nhật:")
                    for dong in data['data']:
                        print(f"      - {dong.get('ten_san_pham', 'N/A')}: {dong.get('gia_ban', 0):,.0f}đ")
        
        ket_noi.close()
        
        print(f"\n🎉 DỮ LIỆU CẬP NHẬT REAL-TIME HOẠT ĐỘNG HOÀN HẢO!")
        print("💡 Trong Tableau Public:")
        print("   - Dữ liệu sẽ được cập nhật mỗi khi refresh connection")
        print("   - Tableau sẽ gọi API mới và lấy dữ liệu mới nhất từ database")
        print("   - Không cần restart server hay thay đổi cấu hình")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test real-time: {e}")
        return False

def khoi_phuc_config_cu():
    """
    Khôi phục config database cũ
    """
    print(f"\n🔄 KHÔI PHỤC CẤU HÌNH CŨ")
    print("=" * 50)
    
    try:
        backup_path = "config/database_config_backup.json"
        config_path = "config/database_config.json"
        
        if os.path.exists(backup_path):
            with open(backup_path, 'r', encoding='utf-8') as f:
                config_cu = json.load(f)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_cu, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Đã khôi phục config cũ: {config_cu['database']}")
            return True
        else:
            print("⚠️ Không tìm thấy file backup config")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khôi phục config: {e}")
        return False

def main():
    """
    Hàm chính - thực hiện toàn bộ test
    """
    print("🧪 KIỂM THỬ TOÀN DIỆN: DATABASE MỚI & REAL-TIME")
    print("=" * 60)
    print("📋 Sẽ kiểm thử:")
    print("  1️⃣ Tạo database mới và kết nối")
    print("  2️⃣ Universal Connector hoạt động với database mới")
    print("  3️⃣ Cập nhật dữ liệu real-time")
    print("  4️⃣ Khôi phục cấu hình cũ")
    print("")
    
    ket_qua_test = {
        'database_moi': False,
        'universal_connector': False,
        'real_time': False,
        'khoi_phuc': False
    }
    
    # Test 1: Tạo database mới
    ten_database_moi = tao_database_test_moi()
    if ten_database_moi:
        ket_qua_test['database_moi'] = True
        
        # Cập nhật config
        if cap_nhat_config_database(ten_database_moi):
            
            # Test 2: Universal Connector
            if test_universal_connector_voi_database_moi(ten_database_moi):
                ket_qua_test['universal_connector'] = True
                
                # Test 3: Real-time update
                if test_cap_nhat_real_time():
                    ket_qua_test['real_time'] = True
    
    # Test 4: Khôi phục config cũ
    if khoi_phuc_config_cu():
        ket_qua_test['khoi_phuc'] = True
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ KIỂM THỬ:")
    print("=" * 60)
    
    for test_name, ket_qua in ket_qua_test.items():
        status = "✅ THÀNH CÔNG" if ket_qua else "❌ THẤT BẠI"
        print(f"  {test_name.upper():<20}: {status}")
    
    if all(ket_qua_test.values()):
        print("\n🎉 TẤT CẢ KIỂM THỬ THÀNH CÔNG!")
        print("\n💡 KẾT LUẬN:")
        print("=" * 60)
        print("✅ CÂU HỎI 1: Có thể tạo database mới và dự án sử dụng được")
        print("   - Universal Connector tự động phát hiện schema")
        print("   - Không cần thay đổi code chính")
        print("   - Chỉ cần cập nhật file config/database_config.json")
        print("")
        print("✅ CÂU HỎI 2: Có thể cập nhật dữ liệu real-time trong Tableau")
        print("   - Dữ liệu được cập nhật trực tiếp trong database")
        print("   - API tự động lấy dữ liệu mới nhất")
        print("   - Tableau refresh sẽ hiển thị dữ liệu mới")
        print("   - Không cần restart server hay thay đổi cấu hình")
        
    else:
        print("\n❌ CÓ LỖI XẢY RA TRONG QUÁ TRÌNH KIỂM THỬ")
        print("🔧 Vui lòng kiểm tra:")
        print("  - SQL Server có đang chạy không?")
        print("  - Có quyền tạo database không?")
        print("  - Thư viện pymssql đã cài đặt chưa?")

if __name__ == "__main__":
    main()
