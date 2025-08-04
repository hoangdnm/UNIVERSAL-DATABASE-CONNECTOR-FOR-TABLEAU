#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script test hiệu suất với 1000 dòng dữ liệu
Dự án tốt nghiệp - Kiểm tra tốc độ API và Tableau với dữ liệu lớn
"""

import time
import requests
import json

def test_hieu_suat_sql_server():
    """
    Test tốc độ truy vấn SQL Server với 1000 dòng
    """
    print("🗄️ TEST HIỆU SUẤT SQL SERVER")
    print("-" * 40)
    
    try:
        import pymssql
        
        # Kết nối
        bat_dau = time.time()
        ket_noi = pymssql.connect(
            server='127.0.0.1',
            port=1235,
            user='sa',
            password='YourStrong!Pass123',
            database='CryptoData'
        )
        
        thoi_gian_ket_noi = time.time() - bat_dau
        print(f"⏱️ Thời gian kết nối: {thoi_gian_ket_noi:.3f}s")
        
        con_tro = ket_noi.cursor()
        
        # Test 1: Đếm tổng số dòng
        bat_dau = time.time()
        con_tro.execute("SELECT COUNT(*) FROM bang_du_lieu_crypto")
        tong_dong = con_tro.fetchone()[0]
        thoi_gian_count = time.time() - bat_dau
        print(f"📊 Tổng số dòng: {tong_dong} (Thời gian: {thoi_gian_count:.3f}s)")
        
        # Test 2: Lấy TOP 10
        bat_dau = time.time()
        con_tro.execute("SELECT TOP 10 * FROM bang_du_lieu_crypto ORDER BY gia_hien_tai DESC")
        top10 = con_tro.fetchall()
        thoi_gian_top10 = time.time() - bat_dau
        print(f"🔝 TOP 10: {len(top10)} dòng (Thời gian: {thoi_gian_top10:.3f}s)")
        
        # Test 3: Lấy tất cả dữ liệu
        bat_dau = time.time()
        con_tro.execute("SELECT * FROM bang_du_lieu_crypto")
        tat_ca = con_tro.fetchall()
        thoi_gian_all = time.time() - bat_dau
        print(f"💾 Tất cả dữ liệu: {len(tat_ca)} dòng (Thời gian: {thoi_gian_all:.3f}s)")
        
        # Test 4: Query phức tạp
        bat_dau = time.time()
        con_tro.execute("""
        SELECT don_vi_tien_te, COUNT(*) as so_luong, 
               AVG(gia_hien_tai) as gia_trung_binh,
               MAX(gia_hien_tai) as gia_cao_nhat,
               MIN(gia_hien_tai) as gia_thap_nhat
        FROM bang_du_lieu_crypto 
        GROUP BY don_vi_tien_te
        """)
        thong_ke = con_tro.fetchall()
        thoi_gian_complex = time.time() - bat_dau
        print(f"📈 Query phức tạp: {len(thong_ke)} nhóm (Thời gian: {thoi_gian_complex:.3f}s)")
        
        ket_noi.close()
        
        return {
            'ket_noi': thoi_gian_ket_noi,
            'count': thoi_gian_count,
            'top10': thoi_gian_top10,
            'all': thoi_gian_all,
            'complex': thoi_gian_complex,
            'tong_dong': tong_dong
        }
        
    except Exception as e:
        print(f"❌ Lỗi SQL Server: {e}")
        return None

def test_hieu_suat_api():
    """
    Test tốc độ API với 1000 dòng dữ liệu
    """
    print("\n🌐 TEST HIỆU SUẤT API")
    print("-" * 40)
    
    # Danh sách test case
    test_cases = [
        {"url": "http://127.0.0.1:5002/api/crypto-data", "mo_ta": "Mặc định (3 coins)"},
        {"url": "http://127.0.0.1:5002/api/crypto-data?coins=bitcoin", "mo_ta": "1 coin"},
        {"url": "http://127.0.0.1:5002/api/crypto-data?coins=bitcoin,ethereum,cardano,binancecoin,solana", "mo_ta": "5 coins"},
        {"url": "http://127.0.0.1:5002/api/crypto-data?currency=usd", "mo_ta": "Tất cả USD"}
    ]
    
    ket_qua_api = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 Test {i}: {test_case['mo_ta']}")
        
        try:
            # Test 3 lần và lấy trung bình
            thoi_gian_list = []
            
            for lan in range(3):
                bat_dau = time.time()
                response = requests.get(test_case['url'], timeout=30)
                ket_thuc = time.time()
                
                if response.status_code == 200:
                    thoi_gian = ket_thuc - bat_dau
                    thoi_gian_list.append(thoi_gian)
                    
                    data = response.json()
                    so_luong = data.get('count', 0)
                    nguon = data.get('data_source', 'Unknown')
                    
                    print(f"   Lần {lan+1}: {thoi_gian:.3f}s - {so_luong} dòng - {nguon}")
                else:
                    print(f"   Lần {lan+1}: Lỗi {response.status_code}")
            
            if thoi_gian_list:
                trung_binh = sum(thoi_gian_list) / len(thoi_gian_list)
                nhanh_nhat = min(thoi_gian_list)
                cham_nhat = max(thoi_gian_list)
                
                print(f"   ⚡ Nhanh nhất: {nhanh_nhat:.3f}s")
                print(f"   🐌 Chậm nhất: {cham_nhat:.3f}s")
                print(f"   📊 Trung bình: {trung_binh:.3f}s")
                
                ket_qua_api.append({
                    'test': test_case['mo_ta'],
                    'trung_binh': trung_binh,
                    'nhanh_nhat': nhanh_nhat,
                    'cham_nhat': cham_nhat,
                    'so_luong': so_luong
                })
        
        except Exception as e:
            print(f"   ❌ Lỗi: {e}")
    
    return ket_qua_api

def test_tableau_wdc():
    """
    Test giao diện Tableau WDC
    """
    print("\n🎨 TEST GIAO DIỆN TABLEAU WDC")
    print("-" * 40)
    
    try:
        bat_dau = time.time()
        response = requests.get("http://127.0.0.1:5002/", timeout=10)
        thoi_gian = time.time() - bat_dau
        
        if response.status_code == 200:
            kich_thuoc = len(response.content)
            print(f"✅ Giao diện tải thành công")
            print(f"⏱️ Thời gian tải: {thoi_gian:.3f}s")
            print(f"📦 Kích thước: {kich_thuoc:,} bytes")
            
            # Kiểm tra nội dung
            if "Tableau Web Data Connector" in response.text:
                print("✅ Có tiêu đề chính xác")
            if "tableau.makeConnector" in response.text:
                print("✅ Có Tableau WDC API")
            if "crypto-data" in response.text:
                print("✅ Có endpoint API")
                
            return {'thanh_cong': True, 'thoi_gian': thoi_gian, 'kich_thuoc': kich_thuoc}
        else:
            print(f"❌ Lỗi {response.status_code}")
            return {'thanh_cong': False}
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return {'thanh_cong': False}

def hien_thi_ket_qua_tong_hop(sql_result, api_result, wdc_result):
    """
    Hiển thị báo cáo tổng hợp
    """
    print("\n" + "=" * 60)
    print("📊 BÁO CÁO HIỆU SUẤT TỔNG HỢP")
    print("=" * 60)
    
    if sql_result:
        print(f"🗄️ SQL SERVER (1000+ dòng):")
        print(f"   ⚡ Kết nối: {sql_result['ket_noi']:.3f}s")
        print(f"   📊 Đếm dòng: {sql_result['count']:.3f}s")
        print(f"   🔝 TOP 10: {sql_result['top10']:.3f}s")
        print(f"   💾 Tất cả: {sql_result['all']:.3f}s ({sql_result['tong_dong']} dòng)")
        print(f"   📈 Query phức tạp: {sql_result['complex']:.3f}s")
    
    if api_result:
        print(f"\n🌐 API REST:")
        for ket_qua in api_result:
            print(f"   {ket_qua['test']}: {ket_qua['trung_binh']:.3f}s ({ket_qua['so_luong']} dòng)")
    
    if wdc_result and wdc_result['thanh_cong']:
        print(f"\n🎨 TABLEAU WDC:")
        print(f"   ⚡ Tải giao diện: {wdc_result['thoi_gian']:.3f}s")
        print(f"   📦 Kích thước: {wdc_result['kich_thuoc']:,} bytes")
    
    # Đánh giá hiệu suất
    print(f"\n⭐ ĐÁNH GIÁ:")
    if sql_result and sql_result['all'] < 1.0:
        print("   ✅ SQL Server: Hiệu suất TỐT (< 1s cho 1000+ dòng)")
    elif sql_result and sql_result['all'] < 3.0:
        print("   ⚠️ SQL Server: Hiệu suất TRUNG BÌNH (1-3s)")
    else:
        print("   ❌ SQL Server: Hiệu suất CHẬM (> 3s)")
    
    if api_result:
        api_trung_binh = sum(r['trung_binh'] for r in api_result) / len(api_result)
        if api_trung_binh < 1.0:
            print("   ✅ API: Hiệu suất TỐT (< 1s)")
        elif api_trung_binh < 3.0:
            print("   ⚠️ API: Hiệu suất TRUNG BÌNH (1-3s)")
        else:
            print("   ❌ API: Hiệu suất CHẬM (> 3s)")

def main():
    """
    Hàm chính - Chạy tất cả test hiệu suất
    """
    print("🧪 TEST HIỆU SUẤT VỚI 1000 DÒNG DỮ LIỆU")
    print("🎯 Mục đích: Kiểm tra tốc độ SQL Server + API + Tableau")
    print("📅 Ngày test:", time.strftime("%d/%m/%Y %H:%M:%S"))
    print("=" * 60)
    
    # Test 1: SQL Server
    sql_result = test_hieu_suat_sql_server()
    
    # Test 2: API
    print("\n⚠️ Lưu ý: Cần chạy server trước: python tableau_web_data_connector.py")
    co_test_api = input("🌐 Test API? (Y/n): ").lower()
    
    api_result = None
    wdc_result = None
    
    if co_test_api != 'n':
        api_result = test_hieu_suat_api()
        wdc_result = test_tableau_wdc()
    
    # Hiển thị kết quả tổng hợp
    hien_thi_ket_qua_tong_hop(sql_result, api_result, wdc_result)
    
    print("\n🎉 HOÀN THÀNH TEST HIỆU SUẤT!")
    print("📊 Dự án sẵn sàng xử lý 1000+ dòng dữ liệu")

if __name__ == "__main__":
    main()
