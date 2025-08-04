#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo 1000 dòng dữ liệu test cho SQL Server
Dự án tốt nghiệp - Test hiệu suất với dữ liệu lớn

Mục đích: Tạo 1000 dòng dữ liệu tiền điện tử để test hiệu suất
"""

import random
from datetime import datetime, timedelta
import time

def tao_du_lieu_1000_dong():
    """
    Tạo 1000 dòng dữ liệu tiền điện tử ngẫu nhiên
    """
    print("📊 TẠO 1000 DÒNG DỮ LIỆU TEST")
    print("=" * 50)
    
    try:
        import pymssql
        print("✅ pymssql đã sẵn sàng")
    except ImportError:
        print("❌ Cần cài đặt pymssql trước")
        return False
    
    # Thông tin kết nối
    thong_tin_ket_noi = {
        'server': '127.0.0.1',
        'port': 1235,
        'user': 'sa', 
        'password': 'YourStrong!Pass123',
        'database': 'CryptoData'
    }
    
    try:
        # Kết nối SQL Server
        print("🔗 Đang kết nối SQL Server...")
        ket_noi = pymssql.connect(
            server=thong_tin_ket_noi['server'],
            port=thong_tin_ket_noi['port'],
            user=thong_tin_ket_noi['user'],
            password=thong_tin_ket_noi['password'],
            database=thong_tin_ket_noi['database']
        )
        
        con_tro = ket_noi.cursor()
        print("✅ Kết nối thành công!")
        
        # Kiểm tra số dòng hiện tại
        con_tro.execute("SELECT COUNT(*) FROM bang_du_lieu_crypto")
        so_dong_hien_tai = con_tro.fetchone()[0]
        print(f"📋 Số dòng hiện tại: {so_dong_hien_tai}")
        
        # Xóa dữ liệu cũ nếu muốn
        lua_chon = input("🗑️ Xóa dữ liệu cũ? (y/N): ").lower()
        if lua_chon == 'y':
            print("🧹 Đang xóa dữ liệu cũ...")
            con_tro.execute("DELETE FROM bang_du_lieu_crypto")
            ket_noi.commit()
            print("✅ Đã xóa dữ liệu cũ")
        
        # Danh sách tên coin mẫu
        danh_sach_coin = [
            ("bitcoin", "Bitcoin", "BTC", 1),
            ("ethereum", "Ethereum", "ETH", 2), 
            ("cardano", "Cardano", "ADA", 8),
            ("binancecoin", "BNB", "BNB", 4),
            ("solana", "Solana", "SOL", 5),
            ("ripple", "XRP", "XRP", 6),
            ("polkadot", "Polkadot", "DOT", 7),
            ("dogecoin", "Dogecoin", "DOGE", 9),
            ("avalanche", "Avalanche", "AVAX", 10),
            ("chainlink", "Chainlink", "LINK", 11),
            ("polygon", "Polygon", "MATIC", 12),
            ("litecoin", "Litecoin", "LTC", 13),
            ("shiba-inu", "Shiba Inu", "SHIB", 14),
            ("uniswap", "Uniswap", "UNI", 15),
            ("cosmos", "Cosmos", "ATOM", 16),
            ("algorand", "Algorand", "ALGO", 17),
            ("vechain", "VeChain", "VET", 18),
            ("filecoin", "Filecoin", "FIL", 19),
            ("tron", "TRON", "TRX", 20),
            ("stellar", "Stellar", "XLM", 21)
        ]
        
        # Tạo 1000 dòng dữ liệu
        print("📝 Đang tạo 1000 dòng dữ liệu...")
        bat_dau = time.time()
        
        du_lieu_1k = []
        for i in range(1000):
            # Chọn coin ngẫu nhiên
            coin_info = random.choice(danh_sach_coin)
            
            # Tạo ID unique
            id_coin = f"{coin_info[0]}_{i+1}"
            ten_coin = f"{coin_info[1]} #{i+1}"
            ky_hieu = coin_info[2]
            
            # Tạo dữ liệu ngẫu nhiên
            gia_co_ban = random.uniform(0.001, 50000)
            gia_hien_tai = gia_co_ban * random.uniform(0.8, 1.2)
            von_hoa = int(gia_hien_tai * random.uniform(1000000, 1000000000))
            xep_hang = i + 1
            khoi_luong = int(von_hoa * random.uniform(0.01, 0.1))
            thay_doi = random.uniform(-10, 10)
            
            # Thời gian ngẫu nhiên trong 30 ngày qua
            ngay_ngau_nhien = datetime.now() - timedelta(days=random.randint(0, 30))
            
            # Thêm vào danh sách
            du_lieu_1k.append((
                id_coin,
                ten_coin,
                ky_hieu,
                round(gia_hien_tai, 8),
                von_hoa,
                xep_hang,
                khoi_luong,
                round(thay_doi, 4),
                ngay_ngau_nhien,
                'usd'
            ))
            
            # Hiển thị tiến độ
            if (i + 1) % 100 == 0:
                print(f"   📊 Đã tạo {i+1}/1000 dòng...")
        
        # Chèn dữ liệu vào database
        print("💾 Đang chèn dữ liệu vào SQL Server...")
        
        cau_lenh_chen = """
        INSERT INTO bang_du_lieu_crypto 
        (id, ten_coin, ky_hieu, gia_hien_tai, von_hoa_thi_truong, xep_hang, 
         khoi_luong_24h, phan_tram_thay_doi_24h, cap_nhat_lan_cuoi, don_vi_tien_te)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # Chèn từng batch 100 dòng
        for i in range(0, len(du_lieu_1k), 100):
            batch = du_lieu_1k[i:i+100]
            for dong in batch:
                con_tro.execute(cau_lenh_chen, dong)
            
            ket_noi.commit()
            print(f"   💾 Đã chèn {min(i+100, len(du_lieu_1k))}/1000 dòng...")
        
        ket_thuc = time.time()
        thoi_gian = ket_thuc - bat_dau
        
        # Kiểm tra kết quả
        con_tro.execute("SELECT COUNT(*) FROM bang_du_lieu_crypto")
        tong_dong = con_tro.fetchone()[0]
        
        print(f"✅ Hoàn thành trong {thoi_gian:.2f} giây")
        print(f"📊 Tổng số dòng trong database: {tong_dong}")
        
        # Test query nhanh
        print("\n🧪 Test query mẫu:")
        con_tro.execute("SELECT TOP 5 ten_coin, ky_hieu, gia_hien_tai FROM bang_du_lieu_crypto ORDER BY gia_hien_tai DESC")
        top5 = con_tro.fetchall()
        
        for dong in top5:
            print(f"   💰 {dong[0]} ({dong[1]}): ${dong[2]:,.8f}")
        
        ket_noi.close()
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return False

def main():
    """
    Hàm chính
    """
    print("🚀 SCRIPT TẠO 1000 DÒNG DỮ LIỆU TEST")
    print("🎯 Mục đích: Test hiệu suất với dữ liệu lớn")
    print("")
    
    if tao_du_lieu_1000_dong():
        print("\n" + "=" * 50)
        print("🎉 TẠO DỮ LIỆU THÀNH CÔNG!")
        print("📊 Database đã có 1000+ dòng dữ liệu")
        print("")
        print("🧪 Bây giờ có thể test:")
        print("   python kiem_thu_du_an.py")
        print("   python tableau_web_data_connector.py")
        print("")
        print("🌐 Test API với 1000 dòng:")
        print("   http://127.0.0.1:5002/test")
    else:
        print("\n❌ TẠO DỮ LIỆU THẤT BẠI!")
        print("🔧 Kiểm tra:")
        print("  - Docker SQL Server có chạy?")
        print("  - Database CryptoData đã tạo?")

if __name__ == "__main__":
    main()
