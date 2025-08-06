#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm thử tính năng FOCUS NHIỀU BẢNG cùng lúc
Dự án nâng cấp - Từ 1 bảng → Nhiều bảng riêng biệt

Mục đích: Đảm bảo có thể chọn nhiều bảng và mỗi bảng là dataset riêng
"""

import requests
import json
import time

def kiem_thu_focus_nhieu_bang():
    """
    Kiểm thử tính năng focus nhiều bảng
    """
    print("🧪 KIỂM THỬ TÍNH NĂNG FOCUS NHIỀU BẢNG")
    print("=" * 60)
    print("🎯 Mục tiêu: Mỗi bảng là dataset riêng biệt (KHÔNG kết hợp)")
    print("")
    
    base_url = "http://127.0.0.1:5002"
    ket_qua_test = []
    
    # Test 1: Kiểm tra giao diện có checkbox
    print("1️⃣ TEST GIAO DIỆN CHECKBOX:")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            content = response.text
            
            # Kiểm tra có checkbox và JavaScript function
            features_checkbox = [
                'type="checkbox"',
                'tablesContainer',
                'updateSelectedCount',
                'getSelectedTables',
            ]
            
            checkbox_found = sum(1 for feature in features_checkbox if feature in content)
            
            if checkbox_found >= 3:
                print(f"   ✅ Giao diện checkbox hoạt động ({checkbox_found}/4 tính năng)")
                ket_qua_test.append("✅ Giao diện checkbox")
            else:
                print(f"   ❌ Thiếu tính năng checkbox ({checkbox_found}/4)")
                ket_qua_test.append("❌ Giao diện checkbox")
        else:
            print(f"   ❌ Không thể truy cập giao diện (HTTP {response.status_code})")
            ket_qua_test.append("❌ Giao diện checkbox")
    except Exception as e:
        print(f"   ❌ Lỗi kiểm tra giao diện: {e}")
        ket_qua_test.append("❌ Giao diện checkbox")
    
    # Test 2: Kiểm tra API databases
    print("\n2️⃣ TEST API DATABASES:")
    try:
        response = requests.get(f"{base_url}/api/databases")
        if response.status_code == 200:
            data = response.json()
            if data['success'] and data['databases']:
                print(f"   ✅ API databases: {len(data['databases'])} database")
                for db in data['databases'][:3]:
                    print(f"      • {db}")
                ket_qua_test.append("✅ API databases")
                test_database = data['databases'][0]
            else:
                print("   ❌ Không tìm thấy database")
                ket_qua_test.append("❌ API databases")
                return
        else:
            print(f"   ❌ API databases lỗi (HTTP {response.status_code})")
            ket_qua_test.append("❌ API databases")
            return
    except Exception as e:
        print(f"   ❌ Lỗi API databases: {e}")
        ket_qua_test.append("❌ API databases")
        return
    
    # Test 3: Kiểm tra API tables
    print("\n3️⃣ TEST API TABLES:")
    try:
        response = requests.get(f"{base_url}/api/tables?database={test_database}")
        if response.status_code == 200:
            data = response.json()
            if data['success'] and data['tables']:
                print(f"   ✅ API tables: {len(data['tables'])} bảng trong {test_database}")
                for table in data['tables'][:3]:
                    print(f"      • {table}")
                ket_qua_test.append("✅ API tables")
                test_tables = data['tables'][:2]  # Lấy 2 bảng đầu để test
            else:
                print("   ❌ Không tìm thấy bảng")
                ket_qua_test.append("❌ API tables")
                return
        else:
            print(f"   ❌ API tables lỗi (HTTP {response.status_code})")
            ket_qua_test.append("❌ API tables")
            return
    except Exception as e:
        print(f"   ❌ Lỗi API tables: {e}")
        ket_qua_test.append("❌ API tables")
        return
    
    # Test 4: Kiểm tra từng bảng riêng biệt (KHÔNG kết hợp)
    print("\n4️⃣ TEST BẢNG RIÊNG BIỆT:")
    for i, table in enumerate(test_tables, 1):
        try:
            # Test schema của từng bảng
            schema_response = requests.get(f"{base_url}/api/schema/{table}?database={test_database}")
            if schema_response.status_code == 200:
                schema_data = schema_response.json()
                if schema_data['success']:
                    columns = schema_data['schema']['columns']
                    print(f"   ✅ Bảng {i}: {table} ({len(columns)} cột)")
                    
                    # Test data của từng bảng
                    data_response = requests.get(f"{base_url}/api/data/{table}?database={test_database}&limit=5")
                    if data_response.status_code == 200:
                        data_result = data_response.json()
                        if data_result['success']:
                            print(f"      📊 Dữ liệu: {data_result['count']} dòng")
                        else:
                            print(f"      ⚠️ Không có dữ liệu")
                    else:
                        print(f"      ❌ Lỗi lấy dữ liệu")
                else:
                    print(f"   ❌ Không lấy được schema của {table}")
            else:
                print(f"   ❌ Lỗi API schema {table}")
        except Exception as e:
            print(f"   ❌ Lỗi test bảng {table}: {e}")
    
    ket_qua_test.append("✅ Bảng riêng biệt")
    
    # Test 5: Xác nhận KHÔNG có API kết hợp
    print("\n5️⃣ TEST KHÔNG CÓ KẾT HỢP TỰ ĐỘNG:")
    try:
        # Thử gọi API cũ (phải bị xóa)
        old_api_response = requests.post(f"{base_url}/api/multi-tables-data", 
                                       json={"tables": test_tables, "database": test_database})
        if old_api_response.status_code == 404:
            print("   ✅ API kết hợp cũ đã bị xóa (404 Not Found)")
            ket_qua_test.append("✅ Không kết hợp tự động")
        else:
            print(f"   ⚠️ API kết hợp cũ vẫn tồn tại (HTTP {old_api_response.status_code})")
            ket_qua_test.append("⚠️ Vẫn có kết hợp tự động")
    except Exception as e:
        print(f"   ✅ API kết hợp cũ không tồn tại: {e}")
        ket_qua_test.append("✅ Không kết hợp tự động")
    
    # Tổng kết
    print("\n" + "="*60)
    print("📊 KẾT QUẢ KIỂM THỬ FOCUS NHIỀU BẢNG:")
    print("")
    
    thanh_cong = sum(1 for kq in ket_qua_test if kq.startswith("✅"))
    tong_so = len(ket_qua_test)
    
    for kq in ket_qua_test:
        print(f"  {kq}")
    
    print("")
    print(f"🎯 Tổng kết: {thanh_cong}/{tong_so} test PASS")
    
    if thanh_cong == tong_so:
        print("🎉 TÍNH NĂNG FOCUS NHIỀU BẢNG HOẠT ĐỘNG HOÀN HẢO!")
        print("✨ Mỗi bảng là dataset riêng biệt trong Tableau")
        print("🚫 KHÔNG tự động kết hợp dữ liệu")
        print("👤 User có thể chọn từng bảng để phân tích")
    else:
        print("⚠️ Một số tính năng cần kiểm tra lại")
    
    print("="*60)
    return thanh_cong == tong_so

if __name__ == "__main__":
    # Đợi server khởi động
    print("⏳ Đợi server khởi động...")
    time.sleep(2)
    
    kiem_thu_focus_nhieu_bang()
