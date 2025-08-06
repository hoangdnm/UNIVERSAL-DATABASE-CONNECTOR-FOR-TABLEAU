#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo database test với nhiều bảng và dữ liệu phong phú
Database: ECommerce_Test - Hệ thống bán hàng điện tử
"""

import pymssql
import random
import json
from datetime import datetime, timedelta
from faker import Faker

# Khởi tạo Faker với tiếng Việt
fake = Faker('vi_VN')

def ket_noi_database():
    """
    Kết nối tới SQL Server
    """
    try:
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa', 
            password='YourStrong!Pass123',
            database='master'
        )
        return ket_noi
    except Exception as e:
        print(f"❌ Lỗi kết nối database: {e}")
        return None

def tao_database():
    """
    Tạo database ECommerce_Test
    """
    ket_noi = ket_noi_database()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        # Xóa database cũ nếu tồn tại
        con_tro.execute("DROP DATABASE IF EXISTS ECommerce_Test")
        
        # Tạo database mới
        con_tro.execute("CREATE DATABASE ECommerce_Test")
        print("✅ Đã tạo database ECommerce_Test")
        
        ket_noi.commit()
        ket_noi.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo database: {e}")
        ket_noi.close()
        return False

def ket_noi_ecommerce_db():
    """
    Kết nối tới database ECommerce_Test
    """
    try:
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123', 
            database='ECommerce_Test'
        )
        return ket_noi
    except Exception as e:
        print(f"❌ Lỗi kết nối ECommerce_Test: {e}")
        return None

def tao_bang_khach_hang():
    """
    Tạo bảng khách hàng
    """
    ket_noi = ket_noi_ecommerce_db()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        # Tạo bảng
        con_tro.execute('''
        CREATE TABLE khach_hang (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ten_khach_hang NVARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            so_dien_thoai VARCHAR(20),
            dia_chi NVARCHAR(200),
            thanh_pho NVARCHAR(50),
            quoc_gia NVARCHAR(50) DEFAULT N'Việt Nam',
            ngay_sinh DATE,
            gioi_tinh NVARCHAR(10),
            ngay_dang_ky DATETIME DEFAULT GETDATE(),
            trang_thai NVARCHAR(20) DEFAULT N'Hoạt động',
            diem_thuong INT DEFAULT 0
        )
        ''')
        
        # Thêm dữ liệu mẫu
        khach_hang_data = []
        thanh_pho_list = [
            'Hà Nội', 'TP. Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ',
            'Nha Trang', 'Huế', 'Vũng Tàu', 'Đà Lạt', 'Quy Nhon'
        ]
        
        for i in range(500):
            ten = fake.name()
            email = fake.email()
            sdt = fake.phone_number()
            dia_chi = fake.address()
            thanh_pho = random.choice(thanh_pho_list)
            ngay_sinh = fake.date_of_birth(minimum_age=18, maximum_age=65)
            gioi_tinh = random.choice(['Nam', 'Nữ', 'Khác'])
            ngay_dk = fake.date_time_between(start_date='-2y', end_date='now')
            trang_thai = random.choice(['Hoạt động', 'Tạm khóa', 'VIP'])
            diem = random.randint(0, 10000)
            
            khach_hang_data.append((
                ten, email, sdt, dia_chi, thanh_pho, 'Việt Nam',
                ngay_sinh, gioi_tinh, ngay_dk, trang_thai, diem
            ))
        
        con_tro.executemany('''
        INSERT INTO khach_hang (ten_khach_hang, email, so_dien_thoai, dia_chi, 
                               thanh_pho, quoc_gia, ngay_sinh, gioi_tinh, 
                               ngay_dang_ky, trang_thai, diem_thuong)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', khach_hang_data)
        
        ket_noi.commit()
        ket_noi.close()
        print("✅ Đã tạo bảng khach_hang với 500 records")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng khach_hang: {e}")
        ket_noi.close()
        return False

def tao_bang_danh_muc():
    """
    Tạo bảng danh mục sản phẩm
    """
    ket_noi = ket_noi_ecommerce_db()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        con_tro.execute('''
        CREATE TABLE danh_muc (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ten_danh_muc NVARCHAR(100) NOT NULL,
            mo_ta NVARCHAR(300),
            danh_muc_cha_id INT NULL,
            trang_thai NVARCHAR(20) DEFAULT N'Hoạt động',
            thu_tu_hien_thi INT DEFAULT 0,
            ngay_tao DATETIME DEFAULT GETDATE()
        )
        ''')
        
        # Dữ liệu danh mục
        danh_muc_data = [
            ('Điện thoại & Tablet', 'Các sản phẩm công nghệ di động', None, 'Hoạt động', 1),
            ('Laptop & Máy tính', 'Máy tính và phụ kiện', None, 'Hoạt động', 2),
            ('Thời trang', 'Quần áo, giày dép, phụ kiện', None, 'Hoạt động', 3),
            ('Gia dụng & Nhà cửa', 'Đồ gia dụng, nội thất', None, 'Hoạt động', 4),
            ('Sách & Văn phòng phẩm', 'Sách, dụng cụ học tập', None, 'Hoạt động', 5),
            ('Thể thao & Du lịch', 'Đồ thể thao, phụ kiện du lịch', None, 'Hoạt động', 6),
            ('Điện thoại iPhone', 'Các dòng iPhone', 1, 'Hoạt động', 11),
            ('Điện thoại Samsung', 'Các dòng Samsung', 1, 'Hoạt động', 12),
            ('Laptop Gaming', 'Laptop cho game thủ', 2, 'Hoạt động', 21),
            ('Laptop Văn phòng', 'Laptop cho công việc', 2, 'Hoạt động', 22),
            ('Thời trang Nam', 'Quần áo nam', 3, 'Hoạt động', 31),
            ('Thời trang Nữ', 'Quần áo nữ', 3, 'Hoạt động', 32),
        ]
        
        con_tro.executemany('''
        INSERT INTO danh_muc (ten_danh_muc, mo_ta, danh_muc_cha_id, trang_thai, thu_tu_hien_thi)
        VALUES (%s, %s, %s, %s, %s)
        ''', danh_muc_data)
        
        ket_noi.commit()
        ket_noi.close()
        print("✅ Đã tạo bảng danh_muc với 12 records")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng danh_muc: {e}")
        ket_noi.close()
        return False

def tao_bang_san_pham():
    """
    Tạo bảng sản phẩm
    """
    ket_noi = ket_noi_ecommerce_db()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        con_tro.execute('''
        CREATE TABLE san_pham (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ten_san_pham NVARCHAR(200) NOT NULL,
            ma_san_pham VARCHAR(50) UNIQUE NOT NULL,
            danh_muc_id INT NOT NULL,
            mo_ta NVARCHAR(500),
            gia_ban DECIMAL(18,2) NOT NULL,
            gia_nhap DECIMAL(18,2),
            so_luong_ton INT DEFAULT 0,
            trong_luong DECIMAL(10,2),
            kich_thuoc NVARCHAR(100),
            mau_sac NVARCHAR(50),
            thuong_hieu NVARCHAR(100),
            xuat_xu NVARCHAR(50),
            bao_hanh_thang INT DEFAULT 12,
            diem_danh_gia DECIMAL(3,2) DEFAULT 0,
            luot_xem INT DEFAULT 0,
            trang_thai NVARCHAR(20) DEFAULT N'Còn hàng',
            ngay_tao DATETIME DEFAULT GETDATE(),
            ngay_cap_nhat DATETIME DEFAULT GETDATE()
        )
        ''')
        
        # Tạo dữ liệu sản phẩm
        san_pham_data = []
        thuong_hieu_list = {
            7: ['Apple'],  # iPhone
            8: ['Samsung', 'Xiaomi', 'Oppo', 'Vivo'],  # Android
            9: ['ASUS', 'MSI', 'Acer', 'HP', 'Dell'],  # Gaming
            10: ['HP', 'Dell', 'Lenovo', 'Acer'],  # Văn phòng
            11: ['Adidas', 'Nike', 'Zara', 'H&M'],  # Nam
            12: ['Zara', 'H&M', 'Uniqlo', 'Mango']  # Nữ
        }
        
        mau_sac_list = ['Đen', 'Trắng', 'Xám', 'Vàng', 'Xanh', 'Đỏ', 'Hồng', 'Tím']
        trang_thai_list = ['Còn hàng', 'Hết hàng', 'Ngưng bán', 'Sắp về']
        
        for i in range(1000):
            danh_muc_id = random.choice([7, 8, 9, 10, 11, 12])
            thuong_hieu = random.choice(thuong_hieu_list.get(danh_muc_id, ['Generic']))
            
            if danh_muc_id in [7, 8]:  # Điện thoại
                ten_sp = f"{thuong_hieu} {fake.word().title()} {random.randint(10,15)}"
                gia_ban = random.randint(5000000, 30000000)
                trong_luong = random.uniform(150, 250)
                kich_thuoc = f"{random.uniform(6.0, 6.8):.1f} inch"
                bao_hanh = 24
            elif danh_muc_id in [9, 10]:  # Laptop
                ten_sp = f"{thuong_hieu} {fake.word().title()} {random.choice(['i5', 'i7', 'Ryzen'])}"
                gia_ban = random.randint(15000000, 50000000)
                trong_luong = random.uniform(1.5, 2.5)
                kich_thuoc = f"{random.choice([13, 14, 15, 16])} inch"
                bao_hanh = 24
            else:  # Thời trang
                ten_sp = f"{thuong_hieu} {fake.word().title()} {random.choice(['Áo', 'Quần', 'Giày'])}"
                gia_ban = random.randint(200000, 2000000)
                trong_luong = random.uniform(0.2, 1.0)
                kich_thuoc = random.choice(['S', 'M', 'L', 'XL', '38', '39', '40', '41', '42'])
                bao_hanh = 6
            
            ma_sp = f"SP{i+1:04d}"
            mo_ta = f"Sản phẩm {ten_sp} chính hãng, chất lượng cao"
            gia_nhap = gia_ban * random.uniform(0.6, 0.8)
            so_luong = random.randint(0, 100)
            mau_sac = random.choice(mau_sac_list)
            xuat_xu = random.choice(['Việt Nam', 'Trung Quốc', 'Hàn Quốc', 'Nhật Bản', 'Mỹ'])
            diem = round(random.uniform(3.0, 5.0), 1)
            luot_xem = random.randint(0, 10000)
            trang_thai = random.choice(trang_thai_list)
            ngay_tao = fake.date_time_between(start_date='-1y', end_date='now')
            
            san_pham_data.append((
                ten_sp, ma_sp, danh_muc_id, mo_ta, gia_ban, gia_nhap,
                so_luong, trong_luong, kich_thuoc, mau_sac, thuong_hieu,
                xuat_xu, bao_hanh, diem, luot_xem, trang_thai, ngay_tao, ngay_tao
            ))
        
        con_tro.executemany('''
        INSERT INTO san_pham (ten_san_pham, ma_san_pham, danh_muc_id, mo_ta, gia_ban, gia_nhap,
                             so_luong_ton, trong_luong, kich_thuoc, mau_sac, thuong_hieu,
                             xuat_xu, bao_hanh_thang, diem_danh_gia, luot_xem, trang_thai, 
                             ngay_tao, ngay_cap_nhat)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', san_pham_data)
        
        ket_noi.commit()
        ket_noi.close()
        print("✅ Đã tạo bảng san_pham với 1000 records")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng san_pham: {e}")
        ket_noi.close()
        return False

def tao_bang_don_hang():
    """
    Tạo bảng đơn hàng
    """
    ket_noi = ket_noi_ecommerce_db()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        con_tro.execute('''
        CREATE TABLE don_hang (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ma_don_hang VARCHAR(50) UNIQUE NOT NULL,
            khach_hang_id INT NOT NULL,
            ngay_dat_hang DATETIME DEFAULT GETDATE(),
            tong_tien DECIMAL(18,2) NOT NULL,
            phi_van_chuyen DECIMAL(18,2) DEFAULT 0,
            giam_gia DECIMAL(18,2) DEFAULT 0,
            tong_thanh_toan DECIMAL(18,2) NOT NULL,
            phuong_thuc_thanh_toan NVARCHAR(50),
            trang_thai_thanh_toan NVARCHAR(30),
            trang_thai_don_hang NVARCHAR(30),
            dia_chi_giao_hang NVARCHAR(300),
            ghi_chu NVARCHAR(200),
            ngay_cap_nhat DATETIME DEFAULT GETDATE()
        )
        ''')
        
        # Tạo dữ liệu đơn hàng
        don_hang_data = []
        phuong_thuc_tt = ['Tiền mặt', 'Chuyển khoản', 'Thẻ tín dụng', 'Ví điện tử', 'COD']
        trang_thai_tt = ['Chưa thanh toán', 'Đã thanh toán', 'Thanh toán một phần', 'Hoàn tiền']
        trang_thai_dh = ['Chờ xử lý', 'Đã xác nhận', 'Đang giao', 'Đã giao', 'Đã hủy', 'Trả hàng']
        
        for i in range(2000):
            ma_dh = f"DH{i+1:06d}"
            khach_hang_id = random.randint(1, 500)
            ngay_dat = fake.date_time_between(start_date='-6m', end_date='now')
            tong_tien = random.randint(100000, 20000000)
            phi_vc = random.choice([0, 25000, 50000, 100000])
            giam_gia = random.randint(0, int(tong_tien * 0.2))
            tong_tt = tong_tien + phi_vc - giam_gia
            phuong_thuc = random.choice(phuong_thuc_tt)
            tt_thanh_toan = random.choice(trang_thai_tt)
            tt_don_hang = random.choice(trang_thai_dh)
            dia_chi = fake.address()
            ghi_chu = random.choice(['', 'Giao hàng nhanh', 'Kiểm tra kỹ hàng', 'Gọi trước khi giao'])
            
            don_hang_data.append((
                ma_dh, khach_hang_id, ngay_dat, tong_tien, phi_vc, giam_gia,
                tong_tt, phuong_thuc, tt_thanh_toan, tt_don_hang, dia_chi, ghi_chu, ngay_dat
            ))
        
        con_tro.executemany('''
        INSERT INTO don_hang (ma_don_hang, khach_hang_id, ngay_dat_hang, tong_tien, 
                             phi_van_chuyen, giam_gia, tong_thanh_toan, phuong_thuc_thanh_toan,
                             trang_thai_thanh_toan, trang_thai_don_hang, dia_chi_giao_hang, 
                             ghi_chu, ngay_cap_nhat)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', don_hang_data)
        
        ket_noi.commit()
        ket_noi.close()
        print("✅ Đã tạo bảng don_hang với 2000 records")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng don_hang: {e}")
        ket_noi.close()
        return False

def tao_bang_chi_tiet_don_hang():
    """
    Tạo bảng chi tiết đơn hàng
    """
    ket_noi = ket_noi_ecommerce_db()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        con_tro.execute('''
        CREATE TABLE chi_tiet_don_hang (
            id INT IDENTITY(1,1) PRIMARY KEY,
            don_hang_id INT NOT NULL,
            san_pham_id INT NOT NULL,
            so_luong INT NOT NULL,
            gia_ban DECIMAL(18,2) NOT NULL,
            thanh_tien DECIMAL(18,2) NOT NULL,
            ghi_chu NVARCHAR(100)
        )
        ''')
        
        # Tạo chi tiết cho mỗi đơn hàng
        chi_tiet_data = []
        
        for don_hang_id in range(1, 2001):  # 2000 đơn hàng
            so_san_pham = random.randint(1, 5)  # Mỗi đơn có 1-5 sản phẩm
            
            for _ in range(so_san_pham):
                san_pham_id = random.randint(1, 1000)
                so_luong = random.randint(1, 3)
                gia_ban = random.randint(100000, 5000000)
                thanh_tien = so_luong * gia_ban
                ghi_chu = random.choice(['', 'Màu đặc biệt', 'Size đặc biệt', 'Yêu cầu gói quà'])
                
                chi_tiet_data.append((
                    don_hang_id, san_pham_id, so_luong, gia_ban, thanh_tien, ghi_chu
                ))
        
        # Chia nhỏ để insert (tránh quá tải)
        batch_size = 1000
        for i in range(0, len(chi_tiet_data), batch_size):
            batch = chi_tiet_data[i:i+batch_size]
            con_tro.executemany('''
            INSERT INTO chi_tiet_don_hang (don_hang_id, san_pham_id, so_luong, gia_ban, thanh_tien, ghi_chu)
            VALUES (%s, %s, %s, %s, %s, %s)
            ''', batch)
            ket_noi.commit()
        
        print(f"✅ Đã tạo bảng chi_tiet_don_hang với {len(chi_tiet_data)} records")
        ket_noi.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng chi_tiet_don_hang: {e}")
        ket_noi.close()
        return False

def tao_bang_danh_gia():
    """
    Tạo bảng đánh giá sản phẩm
    """
    ket_noi = ket_noi_ecommerce_db()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        con_tro.execute('''
        CREATE TABLE danh_gia_san_pham (
            id INT IDENTITY(1,1) PRIMARY KEY,
            san_pham_id INT NOT NULL,
            khach_hang_id INT NOT NULL,
            don_hang_id INT,
            diem_danh_gia INT CHECK (diem_danh_gia >= 1 AND diem_danh_gia <= 5),
            tieu_de NVARCHAR(200),
            noi_dung NVARCHAR(1000),
            ngay_danh_gia DATETIME DEFAULT GETDATE(),
            trang_thai NVARCHAR(20) DEFAULT N'Hiển thị'
        )
        ''')
        
        # Tạo đánh giá
        danh_gia_data = []
        tieu_de_list = [
            'Sản phẩm tốt', 'Chất lượng cao', 'Giá hợp lý', 'Giao hàng nhanh',
            'Đúng mô tả', 'Sẽ mua lại', 'Khuyên mọi người mua', 'Hài lòng',
            'Bình thường', 'Không như mong đợi', 'Cần cải thiện'
        ]
        
        noi_dung_list = [
            'Sản phẩm đúng như mô tả, chất lượng tốt',
            'Giao hàng nhanh, đóng gói cẩn thận',
            'Giá cả hợp lý so với chất lượng',
            'Sẽ ủng hộ shop lần sau',
            'Sản phẩm OK, phù hợp với nhu cầu',
            'Chất lượng không như kỳ vọng',
            'Cần cải thiện về dịch vụ',
            'Tạm ổn, có thể chấp nhận được'
        ]
        
        for i in range(3000):
            san_pham_id = random.randint(1, 1000)
            khach_hang_id = random.randint(1, 500)
            don_hang_id = random.randint(1, 2000) if random.random() > 0.3 else None
            diem = random.randint(3, 5)  # Chủ yếu đánh giá tích cực
            tieu_de = random.choice(tieu_de_list)
            noi_dung = random.choice(noi_dung_list)
            ngay_dg = fake.date_time_between(start_date='-6m', end_date='now')
            trang_thai = random.choice(['Hiển thị', 'Ẩn'])
            
            danh_gia_data.append((
                san_pham_id, khach_hang_id, don_hang_id, diem,
                tieu_de, noi_dung, ngay_dg, trang_thai
            ))
        
        con_tro.executemany('''
        INSERT INTO danh_gia_san_pham (san_pham_id, khach_hang_id, don_hang_id, diem_danh_gia,
                                      tieu_de, noi_dung, ngay_danh_gia, trang_thai)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', danh_gia_data)
        
        ket_noi.commit()
        ket_noi.close()
        print("✅ Đã tạo bảng danh_gia_san_pham với 3000 records")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng danh_gia_san_pham: {e}")
        ket_noi.close()
        return False

def tao_bang_nhan_vien():
    """
    Tạo bảng nhân viên
    """
    ket_noi = ket_noi_ecommerce_db()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        con_tro.execute('''
        CREATE TABLE nhan_vien (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ma_nhan_vien VARCHAR(20) UNIQUE NOT NULL,
            ten_nhan_vien NVARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            so_dien_thoai VARCHAR(20),
            chuc_vu NVARCHAR(50),
            phong_ban NVARCHAR(50),
            luong_co_ban DECIMAL(18,2),
            ngay_vao_lam DATE,
            trang_thai NVARCHAR(20) DEFAULT N'Đang làm việc',
            dia_chi NVARCHAR(200),
            ngay_sinh DATE,
            gioi_tinh NVARCHAR(10)
        )
        ''')
        
        # Tạo dữ liệu nhân viên
        nhan_vien_data = []
        chuc_vu_list = ['Nhân viên', 'Trưởng nhóm', 'Quản lý', 'Giám đốc', 'Thực tập sinh']
        phong_ban_list = ['Kinh doanh', 'Kỹ thuật', 'Marketing', 'Nhân sự', 'Kế toán', 'Kho vận']
        trang_thai_list = ['Đang làm việc', 'Nghỉ phép', 'Thôi việc']
        
        for i in range(50):
            ma_nv = f"NV{i+1:03d}"
            ten_nv = fake.name()
            email = fake.email()
            sdt = fake.phone_number()
            chuc_vu = random.choice(chuc_vu_list)
            phong_ban = random.choice(phong_ban_list)
            
            # Lương theo chức vụ
            luong_map = {
                'Thực tập sinh': random.randint(3000000, 5000000),
                'Nhân viên': random.randint(8000000, 15000000),
                'Trưởng nhóm': random.randint(15000000, 25000000),
                'Quản lý': random.randint(25000000, 40000000),
                'Giám đốc': random.randint(40000000, 80000000)
            }
            luong = luong_map[chuc_vu]
            
            ngay_vao = fake.date_between(start_date='-3y', end_date='now')
            trang_thai = random.choice(trang_thai_list)
            dia_chi = fake.address()
            ngay_sinh = fake.date_of_birth(minimum_age=22, maximum_age=60)
            gioi_tinh = random.choice(['Nam', 'Nữ'])
            
            nhan_vien_data.append((
                ma_nv, ten_nv, email, sdt, chuc_vu, phong_ban,
                luong, ngay_vao, trang_thai, dia_chi, ngay_sinh, gioi_tinh
            ))
        
        con_tro.executemany('''
        INSERT INTO nhan_vien (ma_nhan_vien, ten_nhan_vien, email, so_dien_thoai, 
                              chuc_vu, phong_ban, luong_co_ban, ngay_vao_lam,
                              trang_thai, dia_chi, ngay_sinh, gioi_tinh)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', nhan_vien_data)
        
        ket_noi.commit()
        ket_noi.close()
        print("✅ Đã tạo bảng nhan_vien với 50 records")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi tạo bảng nhan_vien: {e}")
        ket_noi.close()
        return False

def cap_nhat_database_config():
    """
    Cập nhật config để sử dụng database ECommerce_Test
    """
    try:
        config_data = {
            'server': '127.0.0.1',
            'port': 1235,
            'user': 'sa',
            'password': 'YourStrong!Pass123',
            'database': 'ECommerce_Test'
        }
        
        with open('config/database_config.json', 'w', encoding='utf-8') as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        
        print("✅ Đã cập nhật database_config.json")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi cập nhật config: {e}")
        return False

def main():
    """
    Chạy toàn bộ quá trình tạo database test
    """
    print("🚀 BẮT ĐẦU TẠO DATABASE TEST - ECOMMERCE")
    print("=" * 60)
    
    # Bước 1: Tạo database
    print("\n📝 Bước 1: Tạo database ECommerce_Test...")
    if not tao_database():
        return False
    
    # Bước 2: Tạo các bảng
    print("\n📊 Bước 2: Tạo các bảng...")
    
    if not tao_bang_khach_hang():
        return False
    
    if not tao_bang_danh_muc():
        return False
    
    if not tao_bang_san_pham():
        return False
    
    if not tao_bang_don_hang():
        return False
    
    if not tao_bang_chi_tiet_don_hang():
        return False
    
    if not tao_bang_danh_gia():
        return False
    
    if not tao_bang_nhan_vien():
        return False
    
    # Bước 3: Cập nhật config
    print("\n⚙️ Bước 3: Cập nhật database config...")
    if not cap_nhat_database_config():
        return False
    
    print("\n" + "=" * 60)
    print("🎉 HOÀN THÀNH TẠO DATABASE TEST!")
    print("\n📊 Database: ECommerce_Test")
    print("📋 Các bảng đã tạo:")
    print("   • khach_hang (500 records)")
    print("   • danh_muc (12 records)")
    print("   • san_pham (1000 records)")
    print("   • don_hang (2000 records)")
    print("   • chi_tiet_don_hang (~5000 records)")
    print("   • danh_gia_san_pham (3000 records)")
    print("   • nhan_vien (50 records)")
    print("\n🎯 Giờ bạn có thể test Universal Connector với database phong phú!")
    print("🚀 Chạy: python src/tableau_universal_connector.py")
    
    return True

if __name__ == '__main__':
    try:
        # Cài đặt faker nếu chưa có
        import subprocess
        subprocess.run(['pip', 'install', 'faker'], check=False, capture_output=True)
        
        main()
    except ImportError:
        print("❌ Thiếu thư viện faker. Đang cài đặt...")
        import subprocess
        subprocess.run(['pip', 'install', 'faker'])
        print("✅ Đã cài đặt faker. Chạy lại script này.")
    except Exception as e:
        print(f"❌ Lỗi chung: {e}")
