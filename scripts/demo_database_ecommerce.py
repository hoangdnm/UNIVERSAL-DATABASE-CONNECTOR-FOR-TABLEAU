#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script demo đơn giản để test database ECommerce_Test
"""

import pymssql
import json

def ket_noi_ecommerce():
    """
    Kết nối database ECommerce_Test
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
        print(f"❌ Lỗi kết nối: {e}")
        return None

def hien_thi_thong_tin_database():
    """
    Hiển thị thông tin tổng quan về database
    """
    ket_noi = ket_noi_ecommerce()
    if not ket_noi:
        return
    
    try:
        con_tro = ket_noi.cursor()
        
        print("📊 THÔNG TIN DATABASE ECOMMERCE_TEST")
        print("=" * 50)
        
        # Danh sách bảng và số records
        bang_list = [
            'khach_hang', 'danh_muc', 'san_pham', 'don_hang', 
            'chi_tiet_don_hang', 'danh_gia_san_pham', 'nhan_vien'
        ]
        
        for bang in bang_list:
            con_tro.execute(f"SELECT COUNT(*) FROM {bang}")
            so_luong = con_tro.fetchone()[0]
            print(f"📋 {bang:20}: {so_luong:,} records")
        
        print("\n🎯 TOP 5 SẢN PHẨM BÁN CHẠY:")
        con_tro.execute('''
        SELECT TOP 5 
            sp.ten_san_pham,
            sp.thuong_hieu,
            SUM(ct.so_luong) as tong_ban,
            sp.gia_ban
        FROM san_pham sp
        JOIN chi_tiet_don_hang ct ON sp.id = ct.san_pham_id
        GROUP BY sp.id, sp.ten_san_pham, sp.thuong_hieu, sp.gia_ban
        ORDER BY tong_ban DESC
        ''')
        
        for row in con_tro.fetchall():
            print(f"   • {row[0]} ({row[1]}) - Bán: {row[2]} - Giá: {row[3]:,.0f}đ")
        
        print("\n💰 THỐNG KÊ DOANH THU THEO THÁNG:")
        con_tro.execute('''
        SELECT TOP 6
            FORMAT(ngay_dat_hang, 'yyyy-MM') as thang,
            COUNT(*) as so_don,
            SUM(tong_thanh_toan) as doanh_thu
        FROM don_hang
        WHERE trang_thai_don_hang = N'Đã giao'
        GROUP BY FORMAT(ngay_dat_hang, 'yyyy-MM')
        ORDER BY thang DESC
        ''')
        
        for row in con_tro.fetchall():
            print(f"   • {row[0]}: {row[1]} đơn - {row[2]:,.0f}đ")
        
        print("\n🏆 TOP 5 KHÁCH HÀNG VIP:")
        con_tro.execute('''
        SELECT TOP 5
            kh.ten_khach_hang,
            kh.thanh_pho,
            COUNT(dh.id) as so_don,
            SUM(dh.tong_thanh_toan) as tong_chi_tieu
        FROM khach_hang kh
        JOIN don_hang dh ON kh.id = dh.khach_hang_id
        GROUP BY kh.id, kh.ten_khach_hang, kh.thanh_pho
        ORDER BY tong_chi_tieu DESC
        ''')
        
        for row in con_tro.fetchall():
            print(f"   • {row[0]} ({row[1]}) - {row[2]} đơn - {row[3]:,.0f}đ")
        
        ket_noi.close()
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        ket_noi.close()

def test_ket_noi_universal_connector():
    """
    Test kết nối với Universal Connector
    """
    print("\n🔗 TEST KẾT NỐI UNIVERSAL CONNECTOR")
    print("=" * 50)
    
    # Kiểm tra config file
    try:
        with open('config/database_config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        print("✅ Database config:")
        print(f"   • Server: {config['server']}:{config['port']}")
        print(f"   • Database: {config['database']}")
        print(f"   • User: {config['user']}")
        
    except Exception as e:
        print(f"❌ Lỗi đọc config: {e}")
        return
    
    # Test kết nối
    ket_noi = ket_noi_ecommerce()
    if ket_noi:
        print("✅ Kết nối database thành công!")
        
        con_tro = ket_noi.cursor()
        con_tro.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        so_bang = con_tro.fetchone()[0]
        print(f"✅ Tìm thấy {so_bang} bảng trong database")
        
        ket_noi.close()
    else:
        print("❌ Không thể kết nối database!")

def huong_dan_su_dung():
    """
    Hướng dẫn sử dụng database test
    """
    print("\n📖 HƯỚNG DẪN SỬ DỤNG DATABASE TEST")
    print("=" * 50)
    
    print("🚀 1. Chạy Universal Connector:")
    print("   python src/tableau_universal_connector.py")
    
    print("\n🌐 2. Mở trình duyệt:")
    print("   http://127.0.0.1:5002")
    
    print("\n📊 3. Test các bảng khác nhau:")
    print("   • khach_hang - Thông tin khách hàng")
    print("   • san_pham - Catalog sản phẩm") 
    print("   • don_hang - Dữ liệu đơn hàng")
    print("   • chi_tiet_don_hang - Chi tiết từng đơn")
    print("   • danh_gia_san_pham - Review của khách")
    print("   • nhan_vien - Thông tin nhân viên")
    
    print("\n🎯 4. Test tính năng mới:")
    print("   • Export CSV/Excel/JSON")
    print("   • Dashboard Gallery")
    print("   • Mobile responsive")
    print("   • Multi-table selection")
    
    print("\n💡 5. SQL queries hay để test:")
    print("   • SELECT * FROM san_pham WHERE gia_ban > 10000000")
    print("   • SELECT * FROM don_hang WHERE ngay_dat_hang >= '2024-01-01'")
    print("   • SELECT * FROM khach_hang WHERE thanh_pho = N'Hà Nội'")

def main():
    """
    Demo database ECommerce_Test
    """
    print("🎉 DEMO DATABASE ECOMMERCE_TEST")
    print("Hệ thống bán hàng điện tử với dữ liệu phong phú")
    
    hien_thi_thong_tin_database()
    test_ket_noi_universal_connector()
    huong_dan_su_dung()
    
    print("\n" + "=" * 50)
    print("✅ Demo hoàn thành! Sẵn sàng test Universal Connector")

if __name__ == '__main__':
    main()
