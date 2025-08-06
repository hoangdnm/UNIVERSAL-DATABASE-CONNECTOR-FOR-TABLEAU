#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tạo tất cả bảng và dữ liệu trong database ECommerce_Test
"""
import pymssql
import random
import json
from datetime import datetime, timedelta

# Cài đặt faker
try:
    from faker import Faker
    fake = Faker('vi_VN')
except ImportError:
    import subprocess
    print("📦 Đang cài đặt faker...")
    subprocess.run(['pip', 'install', 'faker'], check=True)
    from faker import Faker
    fake = Faker('vi_VN')

def ket_noi_database():
    """Kết nối tới database ECommerce_Test"""
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
        print(f"❌ Lỗi kết nối database: {e}")
        return None

def tao_tat_ca_bang():
    """Tạo tất cả bảng và dữ liệu"""
    print("🚀 BẮT ĐẦU TẠO TẤT CẢ BẢNG VÀ DỮ LIỆU")
    print("=" * 50)
    
    ket_noi = ket_noi_database()
    if not ket_noi:
        return False
    
    try:
        con_tro = ket_noi.cursor()
        
        # 1. Tạo bảng khách hàng
        print("📊 Đang tạo bảng khach_hang...")
        con_tro.execute('''
        CREATE TABLE khach_hang (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ten_khach_hang NVARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            so_dien_thoai VARCHAR(20),
            dia_chi NVARCHAR(200),
            thanh_pho NVARCHAR(50),
            ngay_sinh DATE,
            gioi_tinh NVARCHAR(10),
            ngay_dang_ky DATETIME DEFAULT GETDATE(),
            trang_thai NVARCHAR(20) DEFAULT N'Hoạt động',
            diem_thuong INT DEFAULT 0
        )
        ''')
        
        # Thêm dữ liệu khách hàng
        thanh_pho_list = ['Hà Nội', 'TP. Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ']
        khach_hang_data = []
        for i in range(500):
            ten = fake.name()
            email = f"khach{i+1}@email.com"
            sdt = fake.phone_number()
            dia_chi = fake.address()
            thanh_pho = random.choice(thanh_pho_list)
            ngay_sinh = fake.date_of_birth(minimum_age=18, maximum_age=65)
            gioi_tinh = random.choice(['Nam', 'Nữ'])
            ngay_dk = fake.date_time_between(start_date='-2y', end_date='now')
            trang_thai = random.choice(['Hoạt động', 'VIP', 'Tạm khóa'])
            diem = random.randint(0, 5000)
            
            khach_hang_data.append((ten, email, sdt, dia_chi, thanh_pho, ngay_sinh, 
                                  gioi_tinh, ngay_dk, trang_thai, diem))
        
        con_tro.executemany('''
        INSERT INTO khach_hang (ten_khach_hang, email, so_dien_thoai, dia_chi, thanh_pho, 
                               ngay_sinh, gioi_tinh, ngay_dang_ky, trang_thai, diem_thuong)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', khach_hang_data)
        print("✅ Đã tạo bảng khach_hang với 500 records")
        
        # 2. Tạo bảng danh mục
        print("📊 Đang tạo bảng danh_muc...")
        con_tro.execute('''
        CREATE TABLE danh_muc (
            id INT IDENTITY(1,1) PRIMARY KEY,
            ten_danh_muc NVARCHAR(100) NOT NULL,
            mo_ta NVARCHAR(300),
            trang_thai NVARCHAR(20) DEFAULT N'Hoạt động',
            ngay_tao DATETIME DEFAULT GETDATE()
        )
        ''')
        
        danh_muc_data = [
            ('Điện thoại', 'Điện thoại thông minh các loại', 'Hoạt động'),
            ('Laptop', 'Máy tính xách tay', 'Hoạt động'),
            ('Tablet', 'Máy tính bảng', 'Hoạt động'),
            ('Phụ kiện', 'Phụ kiện điện tử', 'Hoạt động'),
            ('Thời trang Nam', 'Quần áo nam', 'Hoạt động'),
            ('Thời trang Nữ', 'Quần áo nữ', 'Hoạt động'),
            ('Giày dép', 'Giày dép các loại', 'Hoạt động'),
            ('Gia dụng', 'Đồ gia dụng', 'Hoạt động'),
            ('Sách', 'Sách và văn phòng phẩm', 'Hoạt động'),
            ('Thể thao', 'Đồ thể thao', 'Hoạt động')
        ]
        
        con_tro.executemany('''
        INSERT INTO danh_muc (ten_danh_muc, mo_ta, trang_thai)
        VALUES (%s, %s, %s)
        ''', danh_muc_data)
        print("✅ Đã tạo bảng danh_muc với 10 records")
        
        # 3. Tạo bảng sản phẩm
        print("📊 Đang tạo bảng san_pham...")
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
            thuong_hieu NVARCHAR(100),
            mau_sac NVARCHAR(50),
            diem_danh_gia DECIMAL(3,2) DEFAULT 0,
            luot_xem INT DEFAULT 0,
            trang_thai NVARCHAR(20) DEFAULT N'Còn hàng',
            ngay_tao DATETIME DEFAULT GETDATE()
        )
        ''')
        
        # Thêm dữ liệu sản phẩm
        san_pham_data = []
        thuong_hieu_list = ['Samsung', 'Apple', 'Xiaomi', 'HP', 'Dell', 'ASUS', 'Nike', 'Adidas']
        mau_sac_list = ['Đen', 'Trắng', 'Xám', 'Vàng', 'Xanh', 'Đỏ']
        
        for i in range(1000):
            ten_sp = f"Sản phẩm {fake.word().title()} {i+1}"
            ma_sp = f"SP{i+1:04d}"
            danh_muc_id = random.randint(1, 10)
            mo_ta = f"Mô tả chi tiết cho {ten_sp}"
            gia_ban = random.randint(100000, 20000000)
            gia_nhap = int(gia_ban * random.uniform(0.6, 0.8))
            so_luong = random.randint(0, 100)
            thuong_hieu = random.choice(thuong_hieu_list)
            mau_sac = random.choice(mau_sac_list)
            diem = round(random.uniform(3.0, 5.0), 1)
            luot_xem = random.randint(0, 5000)
            trang_thai = random.choice(['Còn hàng', 'Hết hàng', 'Ngưng bán'])
            ngay_tao = fake.date_time_between(start_date='-1y', end_date='now')
            
            san_pham_data.append((ten_sp, ma_sp, danh_muc_id, mo_ta, gia_ban, gia_nhap,
                                so_luong, thuong_hieu, mau_sac, diem, luot_xem, trang_thai, ngay_tao))
        
        con_tro.executemany('''
        INSERT INTO san_pham (ten_san_pham, ma_san_pham, danh_muc_id, mo_ta, gia_ban, gia_nhap,
                             so_luong_ton, thuong_hieu, mau_sac, diem_danh_gia, luot_xem, trang_thai, ngay_tao)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', san_pham_data)
        print("✅ Đã tạo bảng san_pham với 1000 records")
        
        # 4. Tạo bảng đơn hàng
        print("📊 Đang tạo bảng don_hang...")
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
            ghi_chu NVARCHAR(200)
        )
        ''')
        
        # Thêm dữ liệu đơn hàng
        don_hang_data = []
        phuong_thuc_tt = ['Tiền mặt', 'Chuyển khoản', 'Thẻ tín dụng', 'COD']
        trang_thai_tt = ['Chưa thanh toán', 'Đã thanh toán', 'Thanh toán một phần']
        trang_thai_dh = ['Chờ xử lý', 'Đã xác nhận', 'Đang giao', 'Đã giao', 'Đã hủy']
        
        for i in range(1500):
            ma_dh = f"DH{i+1:06d}"
            khach_hang_id = random.randint(1, 500)
            ngay_dat = fake.date_time_between(start_date='-6m', end_date='now')
            tong_tien = random.randint(500000, 10000000)
            phi_vc = random.choice([0, 25000, 50000])
            giam_gia = random.randint(0, int(tong_tien * 0.1))
            tong_tt = tong_tien + phi_vc - giam_gia
            phuong_thuc = random.choice(phuong_thuc_tt)
            tt_thanh_toan = random.choice(trang_thai_tt)
            tt_don_hang = random.choice(trang_thai_dh)
            dia_chi = fake.address()
            ghi_chu = random.choice(['', 'Giao hàng nhanh', 'Kiểm tra kỹ'])
            
            don_hang_data.append((ma_dh, khach_hang_id, ngay_dat, tong_tien, phi_vc, giam_gia,
                                tong_tt, phuong_thuc, tt_thanh_toan, tt_don_hang, dia_chi, ghi_chu))
        
        con_tro.executemany('''
        INSERT INTO don_hang (ma_don_hang, khach_hang_id, ngay_dat_hang, tong_tien, 
                             phi_van_chuyen, giam_gia, tong_thanh_toan, phuong_thuc_thanh_toan,
                             trang_thai_thanh_toan, trang_thai_don_hang, dia_chi_giao_hang, ghi_chu)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', don_hang_data)
        print("✅ Đã tạo bảng don_hang với 1500 records")
        
        # 5. Tạo bảng chi tiết đơn hàng
        print("📊 Đang tạo bảng chi_tiet_don_hang...")
        con_tro.execute('''
        CREATE TABLE chi_tiet_don_hang (
            id INT IDENTITY(1,1) PRIMARY KEY,
            don_hang_id INT NOT NULL,
            san_pham_id INT NOT NULL,
            so_luong INT NOT NULL,
            gia_ban DECIMAL(18,2) NOT NULL,
            thanh_tien DECIMAL(18,2) NOT NULL
        )
        ''')
        
        # Thêm chi tiết đơn hàng
        chi_tiet_data = []
        for don_hang_id in range(1, 1501):
            so_san_pham = random.randint(1, 4)
            for _ in range(so_san_pham):
                san_pham_id = random.randint(1, 1000)
                so_luong = random.randint(1, 3)
                gia_ban = random.randint(100000, 3000000)
                thanh_tien = so_luong * gia_ban
                chi_tiet_data.append((don_hang_id, san_pham_id, so_luong, gia_ban, thanh_tien))
        
        con_tro.executemany('''
        INSERT INTO chi_tiet_don_hang (don_hang_id, san_pham_id, so_luong, gia_ban, thanh_tien)
        VALUES (%s, %s, %s, %s, %s)
        ''', chi_tiet_data)
        print(f"✅ Đã tạo bảng chi_tiet_don_hang với {len(chi_tiet_data)} records")
        
        # 6. Tạo bảng đánh giá
        print("📊 Đang tạo bảng danh_gia_san_pham...")
        con_tro.execute('''
        CREATE TABLE danh_gia_san_pham (
            id INT IDENTITY(1,1) PRIMARY KEY,
            san_pham_id INT NOT NULL,
            khach_hang_id INT NOT NULL,
            diem_danh_gia INT CHECK (diem_danh_gia >= 1 AND diem_danh_gia <= 5),
            tieu_de NVARCHAR(200),
            noi_dung NVARCHAR(1000),
            ngay_danh_gia DATETIME DEFAULT GETDATE(),
            trang_thai NVARCHAR(20) DEFAULT N'Hiển thị'
        )
        ''')
        
        # Thêm đánh giá
        danh_gia_data = []
        tieu_de_list = ['Sản phẩm tốt', 'Chất lượng cao', 'Giá hợp lý', 'Hài lòng', 'Bình thường']
        noi_dung_list = ['Sản phẩm đúng mô tả', 'Giao hàng nhanh', 'Chất lượng OK', 'Sẽ mua lại']
        
        for i in range(2000):
            san_pham_id = random.randint(1, 1000)
            khach_hang_id = random.randint(1, 500)
            diem = random.randint(3, 5)
            tieu_de = random.choice(tieu_de_list)
            noi_dung = random.choice(noi_dung_list)
            ngay_dg = fake.date_time_between(start_date='-6m', end_date='now')
            trang_thai = 'Hiển thị'
            
            danh_gia_data.append((san_pham_id, khach_hang_id, diem, tieu_de, noi_dung, ngay_dg, trang_thai))
        
        con_tro.executemany('''
        INSERT INTO danh_gia_san_pham (san_pham_id, khach_hang_id, diem_danh_gia, tieu_de, 
                                      noi_dung, ngay_danh_gia, trang_thai)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', danh_gia_data)
        print("✅ Đã tạo bảng danh_gia_san_pham với 2000 records")
        
        # 7. Tạo bảng nhân viên
        print("📊 Đang tạo bảng nhan_vien...")
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
            trang_thai NVARCHAR(20) DEFAULT N'Đang làm việc'
        )
        ''')
        
        # Thêm nhân viên
        nhan_vien_data = []
        chuc_vu_list = ['Nhân viên', 'Trưởng nhóm', 'Quản lý', 'Thực tập sinh']
        phong_ban_list = ['Kinh doanh', 'Kỹ thuật', 'Marketing', 'Nhân sự', 'Kế toán']
        
        for i in range(50):
            ma_nv = f"NV{i+1:03d}"
            ten_nv = fake.name()
            email = f"nhanvien{i+1}@company.com"
            sdt = fake.phone_number()
            chuc_vu = random.choice(chuc_vu_list)
            phong_ban = random.choice(phong_ban_list)
            luong = random.randint(8000000, 30000000)
            ngay_vao = fake.date_between(start_date='-2y', end_date='now')
            trang_thai = 'Đang làm việc'
            
            nhan_vien_data.append((ma_nv, ten_nv, email, sdt, chuc_vu, phong_ban, luong, ngay_vao, trang_thai))
        
        con_tro.executemany('''
        INSERT INTO nhan_vien (ma_nhan_vien, ten_nhan_vien, email, so_dien_thoai, 
                              chuc_vu, phong_ban, luong_co_ban, ngay_vao_lam, trang_thai)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', nhan_vien_data)
        print("✅ Đã tạo bảng nhan_vien với 50 records")
        
        # Commit tất cả thay đổi
        ket_noi.commit()
        ket_noi.close()
        
        print("\n" + "=" * 50)
        print("🎉 HOÀN THÀNH TẠO TẤT CẢ BẢNG!")
        print("📊 Database ECommerce_Test đã có đầy đủ dữ liệu:")
        print("   • khach_hang: 500 records")
        print("   • danh_muc: 10 records")
        print("   • san_pham: 1000 records")
        print("   • don_hang: 1500 records")
        print("   • chi_tiet_don_hang: ~4000 records")
        print("   • danh_gia_san_pham: 2000 records")
        print("   • nhan_vien: 50 records")
        print("\n🚀 Giờ có thể test Universal Connector!")
        
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        ket_noi.rollback()
        ket_noi.close()
        return False

if __name__ == '__main__':
    tao_tat_ca_bang()
