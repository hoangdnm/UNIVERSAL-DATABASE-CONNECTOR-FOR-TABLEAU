#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script khởi tạo database cho dự án Web Data Connector
Dự án tốt nghiệp - Kết nối Tableau với SQL Server

Mục đích: Tạo database CryptoData và bảng dữ liệu tiền điện tử
Sử dụng: python khoi_tao_database.py
"""

def kiem_tra_va_cai_dat():
    """
    Kiểm tra và cài đặt thư viện cần thiết
    """
    try:
        import pymssql
        print("✅ pymssql đã được cài đặt")
        return True
    except ImportError:
        print("❌ pymssql chưa được cài đặt")
        print("📦 Đang cài đặt pymssql...")
        
        try:
            import subprocess
            import sys
            
            # Cài đặt pymssql
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "pymssql"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Cài đặt pymssql thành công!")
                return True
            else:
                print(f"❌ Lỗi cài đặt: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Lỗi cài đặt: {e}")
            return False

def tao_du_lieu_crypto():
    """
    Tạo dữ liệu mẫu cho tiền điện tử
    """
    from datetime import datetime
    return [
        ('bitcoin_1', 'Bitcoin', 'BTC', 43250.50, 847000000000, 1, 18500000000, 2.5, datetime.now(), 'usd', 'cryptocurrency', 'Tiền điện tử hàng đầu', 'active'),
        ('ethereum_1', 'Ethereum', 'ETH', 2580.75, 310000000000, 2, 12000000000, -1.2, datetime.now(), 'usd', 'cryptocurrency', 'Nền tảng hợp đồng thông minh', 'active'),
        ('cardano_1', 'Cardano', 'ADA', 0.485, 17000000000, 8, 450000000, 3.8, datetime.now(), 'usd', 'cryptocurrency', 'Blockchain thế hệ 3', 'active'),
        ('binancecoin_1', 'BNB', 'BNB', 315.20, 48000000000, 4, 1200000000, 1.5, datetime.now(), 'usd', 'cryptocurrency', 'Token của sàn Binance', 'active'),
        ('solana_1', 'Solana', 'SOL', 98.45, 43000000000, 5, 2100000000, -0.8, datetime.now(), 'usd', 'cryptocurrency', 'Blockchain hiệu suất cao', 'active')
    ]

def tao_du_lieu_chung_khoan():
    """
    Tạo dữ liệu mẫu cho chứng khoán
    """
    from datetime import datetime
    return [
        ('aapl_1', 'Apple Inc.', 'AAPL', 185.25, 2890000000000, 1, 85000000000, 1.2, datetime.now(), 'usd', 'stock', 'Công ty công nghệ hàng đầu', 'active'),
        ('msft_1', 'Microsoft Corp.', 'MSFT', 340.80, 2520000000000, 2, 45000000000, 0.8, datetime.now(), 'usd', 'stock', 'Phần mềm và cloud computing', 'active'),
        ('googl_1', 'Alphabet Inc.', 'GOOGL', 142.15, 1750000000000, 3, 28000000000, -0.5, datetime.now(), 'usd', 'stock', 'Công cụ tìm kiếm và quảng cáo', 'active'),
        ('amzn_1', 'Amazon.com Inc.', 'AMZN', 145.60, 1520000000000, 4, 32000000000, 2.1, datetime.now(), 'usd', 'stock', 'Thương mại điện tử và AWS', 'active'),
        ('tsla_1', 'Tesla Inc.', 'TSLA', 220.45, 700000000000, 5, 24000000000, -1.8, datetime.now(), 'usd', 'stock', 'Xe điện và năng lượng', 'active')
    ]

def tao_du_lieu_ban_hang():
    """
    Tạo dữ liệu mẫu cho bán hàng
    """
    from datetime import datetime
    return [
        ('product_1', 'Laptop Gaming', 'LTG001', 25000000, 150000000000, 1, 500, 5.2, datetime.now(), 'vnd', 'sales', 'Laptop chơi game cao cấp', 'available'),
        ('product_2', 'Smartphone 5G', 'SP5G002', 15000000, 300000000000, 2, 800, -2.1, datetime.now(), 'vnd', 'sales', 'Điện thoại thông minh 5G', 'available'),
        ('product_3', 'Tai nghe Bluetooth', 'BTH003', 2500000, 75000000000, 3, 1200, 8.5, datetime.now(), 'vnd', 'sales', 'Tai nghe không dây chất lượng cao', 'available'),
        ('product_4', 'Smart TV 4K', 'TV4K004', 18000000, 200000000000, 4, 350, 1.8, datetime.now(), 'vnd', 'sales', 'TV thông minh 4K 55 inch', 'available'),
        ('product_5', 'Máy tính bảng', 'TAB005', 12000000, 180000000000, 5, 600, -1.2, datetime.now(), 'vnd', 'sales', 'Máy tính bảng đa năng', 'available')
    ]

def tao_du_lieu_nhan_su():
    """
    Tạo dữ liệu mẫu cho nhân sự
    """
    from datetime import datetime
    return [
        ('emp_1', 'Nguyễn Văn An', 'NVA001', 25000000, 300000000, 1, 24, 10.5, datetime.now(), 'vnd', 'employee', 'Kỹ sư phần mềm Senior', 'active'),
        ('emp_2', 'Trần Thị Bình', 'TTB002', 22000000, 264000000, 2, 18, 8.2, datetime.now(), 'vnd', 'employee', 'Chuyên viên Marketing', 'active'),
        ('emp_3', 'Lê Hoàng Cường', 'LHC003', 18000000, 216000000, 3, 12, 5.5, datetime.now(), 'vnd', 'employee', 'Kế toán trưởng', 'active'),
        ('emp_4', 'Phạm Minh Đức', 'PMD004', 30000000, 360000000, 4, 36, 12.0, datetime.now(), 'vnd', 'employee', 'Quản lý dự án', 'active'),
        ('emp_5', 'Võ Thị Hoa', 'VTH005', 20000000, 240000000, 5, 15, 6.8, datetime.now(), 'vnd', 'employee', 'Chuyên viên nhân sự', 'active')
    ]

def tao_du_lieu_tuy_chinh():
    """
    Tạo dữ liệu tùy chỉnh theo input của người dùng
    """
    from datetime import datetime
    
    print("\n📝 TẠO DỮ LIỆU TÙY CHỈNH")
    print("-" * 40)
    
    loai_du_lieu = input("Nhập loại dữ liệu (VD: product, customer, etc.): ").strip()
    don_vi = input("Nhập đơn vị (VD: vnd, usd, etc.): ").strip()
    so_luong = int(input("Số lượng dòng dữ liệu (1-100): ") or "5")
    
    du_lieu_tuy_chinh = []
    
    for i in range(min(so_luong, 100)):
        print(f"\nNhập thông tin cho dòng {i+1}:")
        ten_muc = input(f"Tên mục {i+1}: ").strip() or f"Mục {i+1}"
        ky_hieu = input(f"Ký hiệu {i+1}: ").strip() or f"SYM{i+1:03d}"
        gia_tri = float(input(f"Giá trị số {i+1}: ") or str((i+1) * 1000))
        mo_ta = input(f"Mô tả {i+1}: ").strip() or f"Mô tả cho {ten_muc}"
        
        du_lieu_tuy_chinh.append((
            f"custom_{i+1}",
            ten_muc,
            ky_hieu,
            gia_tri,
            int(gia_tri * 1000000),  # gia_tri_lon
            i+1,  # thu_tu
            int(gia_tri * 100),  # gia_tri_phu
            round((i+1-3) * 2.5, 2),  # phan_tram_thay_doi
            datetime.now(),
            don_vi,
            loai_du_lieu,
            mo_ta,
            'active'
        ))
    
    return du_lieu_tuy_chinh

def tao_database_va_bang():
    """
    Tạo database và bảng dữ liệu
    """
    import pymssql
    from datetime import datetime
    
    # Thông tin kết nối
    thong_tin_ket_noi = {
        'server': '127.0.0.1',
        'port': 1235,
        'user': 'sa',
        'password': 'YourStrong!Pass123'
    }
    
    try:
        # Kết nối đến SQL Server (không chỉ định database)
        print("🔗 Đang kết nối SQL Server...")
        ket_noi = pymssql.connect(
            server=thong_tin_ket_noi['server'],
            port=thong_tin_ket_noi['port'],
            user=thong_tin_ket_noi['user'],
            password=thong_tin_ket_noi['password']
        )
        
        con_tro = ket_noi.cursor()
        print("✅ Kết nối thành công!")
        
        # Tạo database
        print("📄 Tạo database TableauDataHub...")
        try:
            # Tắt autocommit để tạo database
            ket_noi.autocommit(True)
            con_tro.execute("IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'TableauDataHub') CREATE DATABASE TableauDataHub")
            print("✅ Tạo database thành công!")
        except Exception as e:
            if "already exists" in str(e).lower() or "đã tồn tại" in str(e).lower():
                print("📄 Database đã tồn tại")
            else:
                print(f"⚠️ Lỗi tạo database: {e}")
                print("🔄 Thử tiếp với database master...")
        
        # Bật lại autocommit
        ket_noi.autocommit(False)
        
        # Đóng kết nối và mở lại với database
        ket_noi.close()
        
        # Kết nối lại với database TableauDataHub
        ket_noi = pymssql.connect(
            server=thong_tin_ket_noi['server'],
            port=thong_tin_ket_noi['port'],
            user=thong_tin_ket_noi['user'],
            password=thong_tin_ket_noi['password'],
            database='TableauDataHub'
        )
        con_tro = ket_noi.cursor()
        
        # Tạo bảng linh hoạt cho nhiều loại dữ liệu
        print("📊 Tạo bảng du_lieu_tong_hop...")
        cau_lenh_tao_bang = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='du_lieu_tong_hop' AND xtype='U')
        CREATE TABLE du_lieu_tong_hop (
            id NVARCHAR(50) PRIMARY KEY,
            ten_muc NVARCHAR(100) NOT NULL,
            ky_hieu NVARCHAR(20),
            gia_tri_so DECIMAL(18,8),
            gia_tri_lon BIGINT,
            thu_tu INT,
            gia_tri_phu BIGINT,
            phan_tram_thay_doi DECIMAL(10,4),
            cap_nhat_lan_cuoi DATETIME2,
            don_vi NVARCHAR(20),
            loai_du_lieu NVARCHAR(50),
            mo_ta NVARCHAR(200),
            trang_thai NVARCHAR(20),
            ngay_tao DATETIME2 DEFAULT GETDATE()
        )
        """
        
        con_tro.execute(cau_lenh_tao_bang)
        ket_noi.commit()
        print("✅ Tạo bảng thành công!")
        
        # Kiểm tra và chèn dữ liệu mẫu
        print("💾 Kiểm tra dữ liệu...")
        con_tro.execute("SELECT COUNT(*) FROM du_lieu_tong_hop")
        so_dong = con_tro.fetchone()[0]
        
        if so_dong == 0:
            print("📝 Chọn loại dữ liệu mẫu:")
            print("1. Tiền điện tử (Cryptocurrency)")
            print("2. Chứng khoán (Stock Market)")
            print("3. Bán hàng (Sales Data)")
            print("4. Nhân sự (HR Data)")
            print("5. Tùy chỉnh (Custom Data)")
            
            lua_chon = input("Chọn loại dữ liệu (1-5): ").strip()
            
            if lua_chon == "1":
                du_lieu_mau = tao_du_lieu_crypto()
            elif lua_chon == "2":
                du_lieu_mau = tao_du_lieu_chung_khoan()
            elif lua_chon == "3":
                du_lieu_mau = tao_du_lieu_ban_hang()
            elif lua_chon == "4":
                du_lieu_mau = tao_du_lieu_nhan_su()
            elif lua_chon == "5":
                du_lieu_mau = tao_du_lieu_tuy_chinh()
            else:
                print("⚠️ Chọn mặc định: Tiền điện tử")
                du_lieu_mau = tao_du_lieu_crypto()
            
            cau_lenh_chen = """
            INSERT INTO du_lieu_tong_hop 
            (id, ten_muc, ky_hieu, gia_tri_so, gia_tri_lon, thu_tu, 
             gia_tri_phu, phan_tram_thay_doi, cap_nhat_lan_cuoi, don_vi, loai_du_lieu, mo_ta, trang_thai)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            for dong in du_lieu_mau:
                con_tro.execute(cau_lenh_chen, dong)
            
            ket_noi.commit()
            print(f"✅ Chèn {len(du_lieu_mau)} dòng dữ liệu mẫu thành công!")
        else:
            print(f"📊 Bảng đã có {so_dong} dòng dữ liệu")
        
        # Kiểm tra dữ liệu
        print("🔍 Kiểm tra dữ liệu vừa tạo...")
        con_tro.execute("SELECT TOP 5 id, ten_muc, ky_hieu, gia_tri_so, loai_du_lieu FROM du_lieu_tong_hop ORDER BY thu_tu")
        ket_qua = con_tro.fetchall()
        
        for dong in ket_qua:
            print(f"  - {dong[1]} ({dong[2]}): {dong[3]:,.2f} - Loại: {dong[4]}")
        
        ket_noi.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    """
    Hàm chính
    """
    print("🚀 Khởi tạo Database SQL Server cho Web Data Connector")
    print("=" * 60)
    
    # Bước 1: Kiểm tra và cài đặt thư viện
    if not kiem_tra_va_cai_dat():
        print("❌ Không thể cài đặt thư viện cần thiết")
        return
    
    # Bước 2: Tạo database và bảng
    if tao_database_va_bang():
        print("\n" + "=" * 60)
        print("✅ Hoàn thành khởi tạo database!")
        print("🔗 Bây giờ bạn có thể chạy Web Data Connector")
        print("📊 Database: TableauDataHub")
        print("📋 Bảng: du_lieu_tong_hop") 
        print("🌐 Chạy server: python tableau_web_data_connector.py")
    else:
        print("\n❌ Khởi tạo database thất bại!")

if __name__ == "__main__":
    main()
