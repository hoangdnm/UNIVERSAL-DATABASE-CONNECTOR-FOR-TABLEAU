#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo database test đơn giản
"""

import pymssql
import random
from datetime import datetime, timedelta

def test_ket_noi():
    """Test kết nối SQL Server"""
    try:
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database='master'
        )
        print("✅ Kết nối SQL Server thành công!")
        ket_noi.close()
        return True
    except Exception as e:
        print(f"❌ Lỗi kết nối SQL Server: {e}")
        return False

def tao_database_don_gian():
    """Tạo database test đơn giản"""
    if not test_ket_noi():
        return False
    
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
        
        # Xóa database cũ
        print("🗑️ Xóa database cũ (nếu có)...")
        con_tro.execute("DROP DATABASE IF EXISTS TestData")
        
        # Tạo database mới
        print("📝 Tạo database TestData...")
        con_tro.execute("CREATE DATABASE TestData")
        ket_noi.commit()
        ket_noi.close()
        
        # Kết nối database mới
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database='TestData'
        )
        con_tro = ket_noi.cursor()
        
        # Tạo bảng customers
        print("📊 Tạo bảng customers...")
        con_tro.execute('''
        CREATE TABLE customers (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ten_khach_hang NVARCHAR(100),
            email VARCHAR(100),
            so_dien_thoai VARCHAR(20),
            thanh_pho NVARCHAR(50),
            tuoi INT,
            ngay_dang_ky DATE
        )
        ''')
        
        # Tạo bảng products
        print("📊 Tạo bảng products...")
        con_tro.execute('''
        CREATE TABLE products (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ten_san_pham NVARCHAR(100),
            gia DECIMAL(18,2),
            danh_muc NVARCHAR(50),
            so_luong INT,
            diem_danh_gia DECIMAL(3,1)
        )
        ''')
        
        # Tạo bảng orders
        print("📊 Tạo bảng orders...")
        con_tro.execute('''
        CREATE TABLE orders (
            id INT IDENTITY(1,1) PRIMARY KEY,
            customer_id INT,
            product_id INT,
            ngay_dat_hang DATE,
            so_luong INT,
            tong_tien DECIMAL(18,2),
            trang_thai NVARCHAR(30)
        )
        ''')
        
        # Thêm dữ liệu customers
        print("📝 Thêm dữ liệu customers...")
        customers_data = []
        ten_list = ['Nguyen Van A', 'Tran Thi B', 'Le Van C', 'Pham Thi D', 'Hoang Van E']
        thanh_pho_list = ['Ha Noi', 'Ho Chi Minh', 'Da Nang', 'Hai Phong', 'Can Tho']
        
        for i in range(100):
            ten = f"{random.choice(ten_list)} {i+1}"
            email = f"user{i+1}@email.com"
            sdt = f"09{random.randint(10000000, 99999999)}"
            thanh_pho = random.choice(thanh_pho_list)
            tuoi = random.randint(18, 65)
            ngay_dk = datetime.now() - timedelta(days=random.randint(0, 365))
            
            customers_data.append((ten, email, sdt, thanh_pho, tuoi, ngay_dk.date()))
        
        con_tro.executemany('''
        INSERT INTO customers (ten_khach_hang, email, so_dien_thoai, thanh_pho, tuoi, ngay_dang_ky)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', customers_data)
        
        # Thêm dữ liệu products
        print("📝 Thêm dữ liệu products...")
        products_data = []
        danh_muc_list = ['Dien thoai', 'Laptop', 'Thoi trang', 'Gia dung', 'Sach']
        
        for i in range(50):
            ten_sp = f"San pham {i+1}"
            gia = random.randint(100000, 10000000)
            danh_muc = random.choice(danh_muc_list)
            so_luong = random.randint(0, 100)
            diem = round(random.uniform(3.0, 5.0), 1)
            
            products_data.append((ten_sp, gia, danh_muc, so_luong, diem))
        
        con_tro.executemany('''
        INSERT INTO products (ten_san_pham, gia, danh_muc, so_luong, diem_danh_gia)
        VALUES (%s, %s, %s, %s, %s)
        ''', products_data)
        
        # Thêm dữ liệu orders
        print("📝 Thêm dữ liệu orders...")
        orders_data = []
        trang_thai_list = ['Da giao', 'Dang giao', 'Cho xu ly', 'Da huy']
        
        for i in range(200):
            customer_id = random.randint(1, 100)
            product_id = random.randint(1, 50)
            ngay_dat = datetime.now() - timedelta(days=random.randint(0, 180))
            so_luong = random.randint(1, 5)
            tong_tien = random.randint(100000, 5000000)
            trang_thai = random.choice(trang_thai_list)
            
            orders_data.append((customer_id, product_id, ngay_dat.date(), so_luong, tong_tien, trang_thai))
        
        con_tro.executemany('''
        INSERT INTO orders (customer_id, product_id, ngay_dat_hang, so_luong, tong_tien, trang_thai)
        VALUES (%s, %s, %s, %s, %s, %s)
        ''', orders_data)
        
        ket_noi.commit()
        ket_noi.close()
        
        print("\n✅ Tạo database TestData thành công!")
        print("📊 Các bảng đã tạo:")
        print("   • customers (100 records)")
        print("   • products (50 records)")
        print("   • orders (200 records)")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo database: {e}")
        return False

def cap_nhat_config():
    """Cập nhật config file"""
    try:
        import json
        config_data = {
            'server': '127.0.0.1',
            'port': 1235,
            'user': 'sa',
            'password': 'YourStrong!Pass123',
            'database': 'TestData'
        }
        
        with open('config/database_config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        
        print("✅ Đã cập nhật config/database_config.json")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi cập nhật config: {e}")
        return False

def main():
    print("🚀 TẠO DATABASE TEST ĐỞN GIẢN")
    print("=" * 40)
    
    if tao_database_don_gian():
        cap_nhat_config()
        print("\n🎉 HOÀN THÀNH!")
        print("🚀 Chạy: python src/tableau_universal_connector.py")
        print("🌐 Mở: http://127.0.0.1:5002")
    else:
        print("❌ Có lỗi xảy ra!")

if __name__ == '__main__':
    main()
