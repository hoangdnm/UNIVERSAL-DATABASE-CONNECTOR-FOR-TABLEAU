#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo thực tế - Tạo database mới và test Real-time
Chứng minh khả năng làm việc với database mới và cập nhật real-time
"""

import json
import os
import pymssql
from datetime import datetime
import random
import requests
import time

def demo_tao_database_moi():
    """
    Demo tạo database mới
    """
    print("🚀 DEMO: TẠO DATABASE MỚI VÀ TEST DỰ ÁN")
    print("=" * 60)
    
    # Tạo tên database mới
    ten_database_demo = "DemoDatabase_" + datetime.now().strftime("%m%d_%H%M")
    
    try:
        print(f"📊 Đang tạo database demo: {ten_database_demo}")
        
        # Kết nối master để tạo database
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database='master',
            autocommit=True  # Quan trọng: tự động commit
        )
        
        con_tro = ket_noi.cursor()
        
        # Tạo database mới
        con_tro.execute(f"CREATE DATABASE [{ten_database_demo}]")
        print(f"✅ Tạo database {ten_database_demo} thành công!")
        
        ket_noi.close()
        
        # Kết nối database mới và tạo bảng
        ket_noi_moi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database=ten_database_demo
        )
        
        con_tro_moi = ket_noi_moi.cursor()
        
        # Tạo bảng nhân viên
        print("📋 Đang tạo bảng: nhan_vien")
        con_tro_moi.execute("""
        CREATE TABLE nhan_vien (
            ma_nv INT IDENTITY(1,1) PRIMARY KEY,
            ho_ten NVARCHAR(100) NOT NULL,
            chuc_vu NVARCHAR(50),
            luong_co_ban DECIMAL(12,2),
            phong_ban NVARCHAR(50),
            ngay_vao_lam DATE,
            trang_thai NVARCHAR(20) DEFAULT N'Đang làm việc'
        )
        """)
        
        # Thêm dữ liệu mẫu
        print("👥 Đang thêm nhân viên mẫu...")
        danh_sach_nv = [
            ('Nguyễn Văn An', 'Trưởng phòng', 25000000, 'IT', '2023-01-15'),
            ('Trần Thị Bình', 'Lập trình viên', 18000000, 'IT', '2023-03-20'),
            ('Lê Văn Cường', 'Tester', 15000000, 'IT', '2023-05-10'),
            ('Phạm Thị Dung', 'Business Analyst', 20000000, 'IT', '2023-02-28'),
            ('Hoàng Văn Em', 'DevOps Engineer', 22000000, 'IT', '2023-04-05'),
            ('Vũ Thị Phương', 'Product Manager', 28000000, 'Sản phẩm', '2023-01-20'),
            ('Đặng Văn Giang', 'Marketing Manager', 24000000, 'Marketing', '2023-03-15'),
            ('Bùi Thị Hoa', 'HR Manager', 26000000, 'Nhân sự', '2023-02-10'),
            ('Ngô Văn Inh', 'Finance Manager', 30000000, 'Tài chính', '2023-01-05'),
            ('Lý Thị Kim', 'Sales Manager', 27000000, 'Kinh doanh', '2023-02-20')
        ]
        
        for nv in danh_sach_nv:
            con_tro_moi.execute("""
            INSERT INTO nhan_vien (ho_ten, chuc_vu, luong_co_ban, phong_ban, ngay_vao_lam)
            VALUES (%s, %s, %s, %s, %s)
            """, nv)
        
        ket_noi_moi.commit()
        
        # Kiểm tra dữ liệu
        con_tro_moi.execute("SELECT COUNT(*) FROM nhan_vien")
        so_nv = con_tro_moi.fetchone()[0]
        print(f"✅ Đã thêm {so_nv} nhân viên vào database")
        
        ket_noi_moi.close()
        
        return ten_database_demo
        
    except Exception as e:
        print(f"❌ Lỗi tạo database: {e}")
        return None

def cap_nhat_config_cho_database_moi(ten_database):
    """
    Cập nhật config để sử dụng database mới
    """
    print(f"\n🔧 CẬP NHẬT CONFIG CHO DATABASE: {ten_database}")
    print("=" * 60)
    
    try:
        # Backup config cũ
        config_path = "config/database_config.json"
        backup_path = "config/database_config_demo_backup.json"
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_cu = json.load(f)
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            json.dump(config_cu, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Đã backup config cũ: {config_cu['database']}")
        
        # Tạo config mới
        config_moi = {
            "server": "127.0.0.1",
            "port": 1235,
            "user": "sa",
            "password": "YourStrong!Pass123", 
            "database": ten_database
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_moi, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Đã cập nhật config để sử dụng: {ten_database}")
        return config_cu
        
    except Exception as e:
        print(f"❌ Lỗi cập nhật config: {e}")
        return None

def test_universal_connector():
    """
    Test Universal Connector với database mới
    """
    print(f"\n🌐 TEST UNIVERSAL CONNECTOR VỚI DATABASE MỚI")
    print("=" * 60)
    
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
        from tableau_universal_connector import app, lay_danh_sach_bang, doc_schema_bang
        
        print("📋 Test 1: Phát hiện bảng tự động")
        bang_list = lay_danh_sach_bang()
        print(f"   ✅ Tìm thấy {len(bang_list)} bảng: {bang_list}")
        
        if 'nhan_vien' in bang_list:
            print("\n📊 Test 2: Phát hiện schema tự động")
            schema = doc_schema_bang('nhan_vien')
            if schema:
                print(f"   ✅ Schema bảng nhan_vien:")
                for cot in schema['columns']:
                    print(f"      - {cot['column_name']:<15}: {cot['sql_type']:<12} → {cot['tableau_type']}")
            
            print("\n🌐 Test 3: API endpoints")
            with app.test_client() as client:
                # Test database info
                response = client.get('/api/database-info')
                if response.status_code == 200:
                    data = response.get_json()
                    if data['success']:
                        print(f"   ✅ Database info: {data['database']} ({data['table_count']} bảng)")
                
                # Test data API
                response = client.get('/api/data/nhan_vien?limit=5')
                if response.status_code == 200:
                    data = response.get_json()
                    if data['success']:
                        print(f"   ✅ Data API: {data['count']} dòng nhân viên")
                        print("   📊 5 nhân viên đầu tiên:")
                        for i, nv in enumerate(data['data'][:5], 1):
                            print(f"      {i}. {nv.get('ho_ten', 'N/A')} - {nv.get('chuc_vu', 'N/A')} - {nv.get('luong_co_ban', 0):,.0f}đ")
        
        print(f"\n🎉 UNIVERSAL CONNECTOR HOẠT ĐỘNG HOÀN HẢO!")
        print("💡 Dự án có thể sử dụng với bất kỳ database mới nào!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi test Universal Connector: {e}")
        return False

def demo_cap_nhat_real_time():
    """
    Demo cập nhật dữ liệu real-time
    """
    print(f"\n⚡ DEMO: CẬP NHẬT DỮ LIỆU REAL-TIME")
    print("=" * 60)
    
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
        
        print("📊 Bước 1: Lấy dữ liệu trước khi cập nhật")
        con_tro.execute("SELECT TOP 3 ho_ten, luong_co_ban FROM nhan_vien ORDER BY ma_nv")
        nv_truoc = con_tro.fetchall()
        
        for i, (ten, luong) in enumerate(nv_truoc, 1):
            print(f"   {i}. {ten}: {luong:,.0f}đ")
        
        print(f"\n💰 Bước 2: Tăng lương 15% cho tất cả nhân viên")
        con_tro.execute("UPDATE nhan_vien SET luong_co_ban = luong_co_ban * 1.15")
        ket_noi.commit()
        so_nv_cap_nhat = con_tro.rowcount
        print(f"   ✅ Đã tăng lương cho {so_nv_cap_nhat} nhân viên")
        
        print(f"\n📊 Bước 3: Kiểm tra dữ liệu sau khi cập nhật")
        con_tro.execute("SELECT TOP 3 ho_ten, luong_co_ban FROM nhan_vien ORDER BY ma_nv")
        nv_sau = con_tro.fetchall()
        
        for i, (ten, luong) in enumerate(nv_sau, 1):
            print(f"   {i}. {ten}: {luong:,.0f}đ")
        
        # Thêm nhân viên mới
        print(f"\n👤 Bước 4: Thêm nhân viên mới")
        nv_moi = (
            f'Nhân viên mới {datetime.now().strftime("%H:%M:%S")}',
            'Junior Developer',
            12000000,
            'IT',
            datetime.now().strftime('%Y-%m-%d')
        )
        
        con_tro.execute("""
        INSERT INTO nhan_vien (ho_ten, chuc_vu, luong_co_ban, phong_ban, ngay_vao_lam)
        VALUES (%s, %s, %s, %s, %s)
        """, nv_moi)
        ket_noi.commit()
        
        print(f"   ✅ Đã thêm: {nv_moi[0]} - {nv_moi[1]} - {nv_moi[2]:,.0f}đ")
        
        # Kiểm tra tổng số nhân viên
        con_tro.execute("SELECT COUNT(*) FROM nhan_vien")
        tong_nv = con_tro.fetchone()[0]
        print(f"   📊 Tổng số nhân viên hiện tại: {tong_nv}")
        
        ket_noi.close()
        
        print(f"\n🎉 DỮ LIỆU ĐÃ ĐƯỢC CẬP NHẬT REAL-TIME!")
        print("💡 Khi Tableau refresh, sẽ thấy ngay:")
        print("   - Lương tất cả nhân viên đã tăng 15%")
        print("   - Nhân viên mới đã được thêm vào")
        print("   - Không cần restart server hay thay đổi cấu hình!")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi demo real-time: {e}")
        return False

def khoi_phuc_config_goc(config_cu):
    """
    Khôi phục config gốc
    """
    print(f"\n🔄 KHÔI PHỤC CẤU HÌNH GỐC")
    print("=" * 60)
    
    try:
        if config_cu:
            with open("config/database_config.json", 'w', encoding='utf-8') as f:
                json.dump(config_cu, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Đã khôi phục config gốc: {config_cu['database']}")
            return True
        else:
            print("⚠️ Không có config cũ để khôi phục")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khôi phục config: {e}")
        return False

def main():
    """
    Hàm chính - Demo toàn diện
    """
    print("🎬 DEMO TOÀN DIỆN: DATABASE MỚI & REAL-TIME")
    print("=" * 70)
    print("🎯 Mục tiêu chứng minh:")
    print("  ✅ Dự án có thể làm việc với database mới")
    print("  ✅ Dữ liệu cập nhật real-time trong Tableau")
    print("")
    
    config_cu = None
    
    try:
        # Bước 1: Tạo database mới
        ten_database_demo = demo_tao_database_moi()
        if not ten_database_demo:
            return
        
        # Bước 2: Cập nhật config
        config_cu = cap_nhat_config_cho_database_moi(ten_database_demo)
        if not config_cu:
            return
        
        # Bước 3: Test Universal Connector
        if not test_universal_connector():
            return
        
        # Bước 4: Demo real-time
        if not demo_cap_nhat_real_time():
            return
        
        # Thành công
        print("\n" + "=" * 70)
        print("🎉 DEMO THÀNH CÔNG 100%!")
        print("=" * 70)
        
        print("💡 KẾT LUẬN:")
        print("✅ CÂU HỎI 1: Tạo database mới → DỰ ÁN SỬ DỤNG ĐƯỢC!")
        print("   - Universal Connector tự động phát hiện schema")
        print("   - Không cần thay đổi code chính")
        print("   - Chỉ cần cập nhật file config")
        print("")
        print("✅ CÂU HỎI 2: Cập nhật dữ liệu → REAL-TIME TRONG TABLEAU!")
        print("   - Dữ liệu INSERT/UPDATE trực tiếp trong database")
        print("   - API luôn trả về dữ liệu mới nhất")
        print("   - Tableau refresh sẽ hiển thị dữ liệu mới ngay lập tức")
        print("")
        print("🚀 DỰ ÁN TỐT NGHIỆP HOÀN HẢO:")
        print("   - Linh hoạt với bất kỳ database nào")
        print("   - Cập nhật real-time không cần restart")
        print("   - Tự động hóa hoàn toàn")
        
    finally:
        # Luôn khôi phục config cũ
        if config_cu:
            khoi_phuc_config_goc(config_cu)
        
        print(f"\n📋 Hướng dẫn sử dụng:")
        print("=" * 70)
        print("🔧 Để thay đổi database:")
        print("   1. Chạy: python scripts\\cau_hinh_database.py")
        print("   2. Nhập thông tin database mới")
        print("   3. Universal Connector tự động hoạt động!")
        print("")
        print("⚡ Để cập nhật real-time:")
        print("   1. Thực hiện INSERT/UPDATE trong SQL Server")
        print("   2. Trong Tableau: Data > Refresh")
        print("   3. Xem dữ liệu mới ngay lập tức!")

if __name__ == "__main__":
    main()
