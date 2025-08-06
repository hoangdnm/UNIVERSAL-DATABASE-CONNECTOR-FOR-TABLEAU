#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm thử tính năng Focus Nhiều Bảng
Dự án tốt nghiệp - Nâng cấp từ 1 bảng lên nhiều bảng cùng lúc
"""

import requests
import json
import sys
import os

def kiem_thu_focus_nhieu_bang():
    """
    Kiểm thử tính năng focus nhiều bảng cùng lúc
    """
    print("🎯 KIỂM THỬ TÍNH NĂNG FOCUS NHIỀU BẢNG")
    print("=" * 60)
    print("📋 Nâng cấp từ phiên bản cũ:")
    print("  🔄 Trước: Chỉ chọn được 1 bảng")
    print("  🆕 Sau: Có thể chọn nhiều bảng cùng lúc")
    print("")
    
    base_url = "http://127.0.0.1:5002"
    ket_qua_test = []
    
    # Test 1: Kiểm tra giao diện có checkbox
    print("1️⃣ TEST GIAO DIỆN CHECKBOX:")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            content = response.text
            
            # Kiểm tra các phần tử giao diện mới
            checkbox_features = [
                "tablesContainer",  # Container cho checkbox
                "selectedTablesCount",  # Đếm số bảng đã chọn
                "table-checkbox",  # CSS class cho checkbox
                "selectedTables",  # Name attribute cho checkbox
                "Chọn các bảng dữ liệu (có thể chọn nhiều)",  # Label mới
            ]
            
            features_tim_thay = 0
            for feature in checkbox_features:
                if feature in content:
                    features_tim_thay += 1
                    print(f"   ✅ Tìm thấy: {feature}")
                else:
                    print(f"   ❌ Thiếu: {feature}")
            
            if features_tim_thay >= 4:
                print(f"   ✅ Giao diện checkbox hoạt động ({features_tim_thay}/{len(checkbox_features)})")
                ket_qua_test.append("✅ Giao diện checkbox")
            else:
                print(f"   ❌ Giao diện chưa đầy đủ ({features_tim_thay}/{len(checkbox_features)})")
                ket_qua_test.append("❌ Giao diện checkbox")
                
        else:
            print(f"   ❌ Lỗi truy cập giao diện: HTTP {response.status_code}")
            ket_qua_test.append("❌ Giao diện checkbox")
            
    except Exception as e:
        print(f"   ❌ Lỗi kiểm tra giao diện: {e}")
        ket_qua_test.append("❌ Giao diện checkbox")
    
    # Test 2: Kiểm tra API mới cho nhiều bảng
    print("\n2️⃣ TEST API NHIỀU BẢNG:")
    try:
        # Lấy danh sách database
        db_response = requests.get(f"{base_url}/api/databases")
        if db_response.status_code == 200:
            db_data = db_response.json()
            if db_data['success'] and db_data['databases']:
                database = db_data['databases'][0]
                print(f"   📊 Test với database: {database}")
                
                # Lấy danh sách bảng
                tables_response = requests.get(f"{base_url}/api/tables?database={database}")
                if tables_response.status_code == 200:
                    tables_data = tables_response.json()
                    if tables_data['success'] and tables_data['tables']:
                        bang_list = tables_data['tables']
                        print(f"   📋 Tìm thấy {len(bang_list)} bảng: {bang_list[:3]}...")
                        
                        # Test API nhiều bảng
                        test_tables = bang_list[:2]  # Test với 2 bảng đầu
                        test_data = {
                            "database": database,
                            "tables": test_tables,
                            "limit": "10",
                            "order": "auto",
                            "where": ""
                        }
                        
                        multi_response = requests.post(
                            f"{base_url}/api/multi-tables-data",
                            json=test_data,
                            headers={"Content-Type": "application/json"}
                        )
                        
                        if multi_response.status_code == 200:
                            multi_data = multi_response.json()
                            if multi_data['success']:
                                print(f"   ✅ API nhiều bảng hoạt động")
                                print(f"   📊 Kết hợp {len(multi_data['tables'])} bảng")
                                print(f"   📈 Lấy được {multi_data['count']} dòng dữ liệu")
                                ket_qua_test.append("✅ API nhiều bảng")
                            else:
                                print(f"   ❌ API trả về lỗi: {multi_data.get('error', 'Unknown')}")
                                ket_qua_test.append("❌ API nhiều bảng")
                        else:
                            print(f"   ❌ Lỗi HTTP API: {multi_response.status_code}")
                            ket_qua_test.append("❌ API nhiều bảng")
                    else:
                        print("   ❌ Không tìm thấy bảng để test")
                        ket_qua_test.append("❌ API nhiều bảng")
                else:
                    print(f"   ❌ Lỗi lấy danh sách bảng: {tables_response.status_code}")
                    ket_qua_test.append("❌ API nhiều bảng")
            else:
                print("   ❌ Không tìm thấy database để test")
                ket_qua_test.append("❌ API nhiều bảng")
        else:
            print(f"   ❌ Lỗi lấy database: {db_response.status_code}")
            ket_qua_test.append("❌ API nhiều bảng")
            
    except Exception as e:
        print(f"   ❌ Lỗi test API: {e}")
        ket_qua_test.append("❌ API nhiều bảng")
    
    # Test 3: Kiểm tra JavaScript functions
    print("\n3️⃣ TEST JAVASCRIPT FUNCTIONS:")
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            content = response.text
            
            js_functions = [
                "toggleAllTables()",
                "updateSelectedTablesCount()",
                "getSelectedTables()",
                "multi-tables-data",  # API endpoint trong JS
                "selectedTables",  # Variable trong JS
            ]
            
            functions_tim_thay = 0
            for func in js_functions:
                if func in content:
                    functions_tim_thay += 1
                    print(f"   ✅ Tìm thấy: {func}")
                else:
                    print(f"   ❌ Thiếu: {func}")
            
            if functions_tim_thay >= 4:
                print(f"   ✅ JavaScript functions hoạt động ({functions_tim_thay}/{len(js_functions)})")
                ket_qua_test.append("✅ JavaScript functions")
            else:
                print(f"   ❌ JavaScript chưa đầy đủ ({functions_tim_thay}/{len(js_functions)})")
                ket_qua_test.append("❌ JavaScript functions")
                
        else:
            print(f"   ❌ Lỗi kiểm tra JavaScript: HTTP {response.status_code}")
            ket_qua_test.append("❌ JavaScript functions")
            
    except Exception as e:
        print(f"   ❌ Lỗi test JavaScript: {e}")
        ket_qua_test.append("❌ JavaScript functions")
    
    # Tổng kết
    print("\n" + "=" * 60)
    print("🏆 KẾT QUẢ KIỂM THỬ FOCUS NHIỀU BẢNG:")
    print("=" * 60)
    
    thanh_cong = sum(1 for result in ket_qua_test if result.startswith("✅"))
    tong_so = len(ket_qua_test)
    
    for result in ket_qua_test:
        print(f"  {result}")
    
    print(f"\n📊 Tỷ lệ thành công: {thanh_cong}/{tong_so} ({thanh_cong/tong_so*100:.1f}%)")
    
    if thanh_cong == tong_so:
        print("🎉 TÍNH NĂNG FOCUS NHIỀU BẢNG HOẠT ĐỘNG HOÀN HẢO!")
        print("💡 Đã nâng cấp thành công từ 1 bảng → nhiều bảng!")
        return True
    else:
        print("⚠️  Còn một số vấn đề cần khắc phục")
        return False

def main():
    """
    Hàm chính
    """
    print("🚀 TABLEAU UNIVERSAL DATABASE CONNECTOR")
    print("🎯 Kiểm thử nâng cấp: Focus nhiều bảng cùng lúc")
    print("📅 Ngày kiểm thử:", __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("")
    
    kiem_thu_focus_nhieu_bang()

if __name__ == "__main__":
    main()
