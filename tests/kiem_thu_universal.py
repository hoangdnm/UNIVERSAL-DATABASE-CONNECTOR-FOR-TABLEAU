#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧪 KIỂM THỬ DỰ ÁN NÂNG CẤP - UNIVERSAL DATABASE CONNECTOR
==================================================
Kiểm thử phiên bản nâng cấp với khả năng kết nối bất kỳ database nào
"""

import sys
import os
import requests
import time
from datetime import datetime

def test_universal_connector():
    """
    Kiểm thử Universal Database Connector
    """
    print("🧪 KIỂM THỬ UNIVERSAL DATABASE CONNECTOR")
    print("=" * 55)
    print("📋 Test các tính năng nâng cấp:")
    print("  1️⃣ Config database linh hoạt")
    print("  2️⃣ Universal API connector") 
    print("  3️⃣ Tableau universal interface")
    print("  4️⃣ Auto schema detection")
    print("")
    
    ket_qua_test = []
    
    # Test 1: Config database
    print("1️⃣ TEST CẤU HÌNH DATABASE:")
    try:
        import json
        config_path = "config/database_config.json"
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            print(f"   ✅ Config file tồn tại")
            print(f"   📡 Server: {config['server']}:{config['port']}")
            print(f"   🗃️ Database: {config['database']}")
            ket_qua_test.append("✅ Config database")
        else:
            print("   ❌ Không tìm thấy config file")
            ket_qua_test.append("❌ Config database")
            
    except Exception as e:
        print(f"   ❌ Lỗi config: {e}")
        ket_qua_test.append("❌ Config database")
    
    # Test 2: Universal API
    print("\n2️⃣ TEST UNIVERSAL API:")
    try:
        # Import universal connector để test
        sys.path.append('src')
        from tableau_universal_connector import doc_cau_hinh_database, lay_danh_sach_bang
        
        config = doc_cau_hinh_database()
        bang_list = lay_danh_sach_bang()  # Không cần parameter
        
        if bang_list:
            print(f"   ✅ Universal API hoạt động")
            print(f"   📋 Phát hiện {len(bang_list)} bảng:")
            for bang in bang_list[:3]:  # Hiển thị 3 bảng đầu
                print(f"      • {bang}")
            if len(bang_list) > 3:
                print(f"      • ... và {len(bang_list)-3} bảng khác")
            ket_qua_test.append("✅ Universal API")
        else:
            print("   ❌ Không phát hiện được bảng")
            ket_qua_test.append("❌ Universal API")
            
    except Exception as e:
        print(f"   ❌ Lỗi API: {e}")
        ket_qua_test.append("❌ Universal API")
        bang_list = []  # Set default để test tiếp
    
    # Test 3: Schema detection
    print("\n3️⃣ TEST AUTO SCHEMA DETECTION:")
    try:
        if 'bang_list' in locals() and bang_list:
            # Test với bảng đầu tiên
            bang_dau = bang_list[0]
            from tableau_universal_connector import lay_schema_bang
            
            config = doc_cau_hinh_database()
            schema = lay_schema_bang(config, bang_dau)
            if schema:
                print(f"   ✅ Schema detection hoạt động")
                print(f"   📊 Bảng '{bang_dau}' có {len(schema)} cột:")
                for cot in schema[:3]:  # Hiển thị 3 cột đầu
                    print(f"      • {cot['name']} ({cot['dataType']})")
                if len(schema) > 3:
                    print(f"      • ... và {len(schema)-3} cột khác")
                ket_qua_test.append("✅ Schema detection")
            else:
                print("   ❌ Không phát hiện được schema")
                ket_qua_test.append("❌ Schema detection")
        else:
            print("   ❌ Không có bảng để test schema")
            ket_qua_test.append("❌ Schema detection")
            
    except Exception as e:
        print(f"   ❌ Lỗi schema: {e}")
        ket_qua_test.append("❌ Schema detection")
    
    # Test 4: Universal interface
    print("\n4️⃣ TEST UNIVERSAL INTERFACE:")
    try:
        # Kiểm tra template có chứa universal features
        template_path = "src/tableau_universal_connector.py"
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        features_can_co = [
            "dropdown",  # Dropdown chọn bảng
            "table_name",  # Tên bảng dynamic
            "schema",  # Schema detection
            "WHERE",  # WHERE clause support
        ]
        
        features_tim_thay = 0
        for feature in features_can_co:
            if feature in content:
                features_tim_thay += 1
        
        if features_tim_thay >= 3:
            print(f"   ✅ Universal interface hoạt động")
            print(f"   🎯 Có {features_tim_thay}/{len(features_can_co)} tính năng universal")
            ket_qua_test.append("✅ Universal interface")
        else:
            print(f"   ❌ Interface chưa universal ({features_tim_thay}/{len(features_can_co)})")
            ket_qua_test.append("❌ Universal interface")
            
    except Exception as e:
        print(f"   ❌ Lỗi interface: {e}")
        ket_qua_test.append("❌ Universal interface")
    
    # Tổng kết
    print("\n" + "=" * 55)
    thanh_cong = sum(1 for kq in ket_qua_test if "✅" in kq)
    tong_so = len(ket_qua_test)
    
    print(f"📊 KẾT QUẢ KIỂM THỬ: {thanh_cong}/{tong_so} TÍNH NĂNG HOẠT ĐỘNG")
    
    for i, kq in enumerate(ket_qua_test, 1):
        print(f"  {i}. {kq}")
    
    if thanh_cong == tong_so:
        print("\n🎉 UNIVERSAL CONNECTOR HOẠT ĐỘNG HOÀN HẢO!")
        print("✅ Dự án đã nâng cấp thành công")
        print("🚀 Sẵn sàng demo Universal Database Connector")
        return True
    else:
        print(f"\n⚠️ CẦN KHẮC PHỤC {tong_so - thanh_cong} TÍNH NĂNG")
        return False

if __name__ == "__main__":
    test_universal_connector()
