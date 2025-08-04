#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script kiểm thử dự án tốt nghiệp
Test 3 chức năng chính: SQL Server + API + Tableau
"""

def test_chuc_nang_chinh():
    """
    Kiểm thử 3 chức năng chính của dự án
    """
    print("🧪 KIỂM THỬ DỰ ÁN TỐT NGHIỆP")
    print("=" * 50)
    print("📋 Test 3 chức năng chính:")
    print("  1️⃣ Kết nối SQL Server")
    print("  2️⃣ API lấy dữ liệu") 
    print("  3️⃣ Kết nối Tableau")
    print("")
    
    # Test 1: SQL Server
    print("1️⃣ TEST KẾT NỐI SQL SERVER:")
    try:
        import pymssql
        
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database='CryptoData'
        )
        
        con_tro = ket_noi.cursor()
        con_tro.execute("SELECT COUNT(*) FROM bang_du_lieu_crypto")
        so_dong = con_tro.fetchone()[0]
        ket_noi.close()
        
        print(f"   ✅ Kết nối SQL Server thành công")
        print(f"   📊 Database có {so_dong} dòng dữ liệu")
        
    except Exception as e:
        print(f"   ❌ Lỗi kết nối SQL Server: {e}")
        return False
    
    # Test 2: API
    print("\n2️⃣ TEST API LẤY DỮ LIỆU:")
    try:
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
        from tableau_web_data_connector import app
        
        with app.test_client() as client:
            response = client.get('/api/crypto-data?coins=bitcoin,ethereum&currency=usd')
            
            if response.status_code == 200:
                data = response.get_json()
                print(f"   ✅ API hoạt động thành công")
                print(f"   📊 Trả về {data.get('count', 0)} loại tiền")
                print(f"   💾 Nguồn: {data.get('data_source', 'Unknown')}")
            else:
                print(f"   ❌ API lỗi: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Lỗi test API: {e}")
        return False
    
    # Test 3: Tableau interface
    print("\n3️⃣ TEST GIAO DIỆN TABLEAU:")
    try:
        with app.test_client() as client:
            response = client.get('/')
            
            if response.status_code == 200:
                print("   ✅ Giao diện Tableau hoạt động")
                print("   🌐 URL: http://127.0.0.1:5002")
            else:
                print(f"   ❌ Giao diện lỗi: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"   ❌ Lỗi test giao diện: {e}")
        return False
    
    return True

def main():
    """
    Hàm chính
    """
    if test_chuc_nang_chinh():
        print("\n" + "=" * 50)
        print("🎉 TẤT CẢ 3 CHỨC NĂNG HOẠT ĐỘNG HOÀN HẢO!")
        print("✅ Dự án sẵn sàng demo và nộp")
        print("")
        print("🚀 Để chạy dự án:")
        print("   cd src && python tableau_web_data_connector.py")
        print("")
        print("📊 Để kết nối Tableau:")
        print("   URL: http://127.0.0.1:5002")
    else:
        print("\n❌ CÓ LỖI XẢY RA!")
        print("🔧 Vui lòng kiểm tra lại:")
        print("  - Docker SQL Server có chạy không?")
        print("  - Database đã tạo chưa?")
        print("  - Thư viện pymssql đã cài chưa?")

if __name__ == "__main__":
    main()
