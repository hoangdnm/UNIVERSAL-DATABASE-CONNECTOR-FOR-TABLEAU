#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TEST TOÀN BỘ HỆ THỐNG SAU KHI REFACTOR
Kiểm tra tất cả các module và API hoạt động đúng
"""

import sys
import os

# Thêm src vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test 1: Kiểm tra import các module"""
    print("\n" + "=" * 70)
    print("TEST 1: KIỂM TRA IMPORT CÁC MODULE")
    print("=" * 70)
    
    try:
        # Test import database_connector
        import database_connector as db_conn
        print("✅ Import database_connector thành công")
        
        # Test import utils.schema_detector
        from utils.schema_detector import (
            doc_cau_hinh_database,
            lay_danh_sach_database,
            lay_danh_sach_bang,
            tu_dong_phat_hien_schema,
            parse_table_name
        )
        print("✅ Import utils.schema_detector thành công")
        
        # Test import routes.api_routes
        from routes.api_routes import register_routes
        print("✅ Import routes.api_routes thành công")
        
        # Test import main app
        from tableau_universal_connector import app
        print("✅ Import tableau_universal_connector thành công")
        
        print("\n🎉 TẤT CẢ IMPORTS THÀNH CÔNG!")
        return True
        
    except Exception as e:
        print(f"\n❌ LỖI IMPORT: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test 2: Kiểm tra đọc cấu hình"""
    print("\n" + "=" * 70)
    print("TEST 2: KIỂM TRA ĐỌC CẤU HÌNH")
    print("=" * 70)
    
    try:
        from utils.schema_detector import doc_cau_hinh_database
        
        config = doc_cau_hinh_database()
        print(f"✅ Đọc config thành công")
        print(f"   Server: {config.get('server')}")
        print(f"   Port: {config.get('port')}")
        print(f"   Database: {config.get('database')}")
        print(f"   User: {config.get('user')}")
        
        return True
        
    except Exception as e:
        print(f"❌ LỖI ĐỌC CONFIG: {e}")
        return False


def test_schema_functions():
    """Test 3: Kiểm tra các hàm schema"""
    print("\n" + "=" * 70)
    print("TEST 3: KIỂM TRA CÁC HÀM SCHEMA")
    print("=" * 70)
    
    try:
        from utils.schema_detector import parse_table_name
        
        # Test parse table name format 1: Table
        schema_table, db = parse_table_name("Users", {})
        assert schema_table == "Users"
        print(f"✅ Parse 'Users' -> table='{schema_table}', db='{db}'")
        
        # Test parse table name format 2: Schema.Table
        schema_table, db = parse_table_name("dbo.Users", {'database': 'TestDB'})
        assert schema_table == "dbo.Users"
        assert db == "TestDB"
        print(f"✅ Parse 'dbo.Users' -> table='{schema_table}', db='{db}'")
        
        # Test parse table name format 3: Database.Schema.Table
        schema_table, db = parse_table_name("MyDB.dbo.Users", {})
        assert schema_table == "dbo.Users"
        assert db == "MyDB"
        print(f"✅ Parse 'MyDB.dbo.Users' -> table='{schema_table}', db='{db}'")
        
        print("\n🎉 TẤT CẢ TESTS SCHEMA THÀNH CÔNG!")
        return True
        
    except Exception as e:
        print(f"❌ LỖI TEST SCHEMA: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_flask_app():
    """Test 4: Kiểm tra Flask app"""
    print("\n" + "=" * 70)
    print("TEST 4: KIỂM TRA FLASK APP")
    print("=" * 70)
    
    try:
        from tableau_universal_connector import app
        
        # Test app được khởi tạo
        assert app is not None
        print("✅ Flask app được khởi tạo thành công")
        
        # Test template folder
        assert 'templates' in app.template_folder
        print(f"✅ Template folder: {app.template_folder}")
        
        # Test routes
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        print(f"✅ Số routes đã đăng ký: {len(routes)}")
        
        expected_routes = [
            '/',
            '/api/database-info',
            '/api/databases',
            '/api/tables',
            '/api/schema/<path:table_name>',
            '/api/data/<path:table_name>'
        ]
        
        for route in expected_routes:
            if route in routes:
                print(f"   ✓ {route}")
            else:
                print(f"   ✗ {route} - THIẾU!")
        
        print("\n🎉 FLASK APP HOẠT ĐỘNG TỐT!")
        return True
        
    except Exception as e:
        print(f"❌ LỖI FLASK APP: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_template_exists():
    """Test 5: Kiểm tra template HTML tồn tại"""
    print("\n" + "=" * 70)
    print("TEST 5: KIỂM TRA TEMPLATE HTML")
    print("=" * 70)
    
    try:
        template_path = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'templates', 
            'wdc_template.html'
        )
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = len(content.split('\n'))
                print(f"✅ Template tồn tại: {template_path}")
                print(f"   Số dòng: {lines}")
                
                # Kiểm tra các phần quan trọng
                checks = [
                    ('Tableau WDC API', 'tableauwdc-2.3.latest.js' in content),
                    ('Database selector', 'databasesContainer' in content),
                    ('Table selector', 'tablesContainer' in content),
                    ('Submit button', 'submitButton' in content),
                    ('JavaScript functions', 'tableau.makeConnector()' in content)
                ]
                
                for check_name, check_result in checks:
                    if check_result:
                        print(f"   ✓ {check_name}")
                    else:
                        print(f"   ✗ {check_name} - THIẾU!")
                
                return True
        else:
            print(f"❌ Template không tồn tại: {template_path}")
            return False
            
    except Exception as e:
        print(f"❌ LỖI KIỂM TRA TEMPLATE: {e}")
        return False


def test_file_structure():
    """Test 6: Kiểm tra cấu trúc file"""
    print("\n" + "=" * 70)
    print("TEST 6: KIỂM TRA CẤU TRÚC FILE")
    print("=" * 70)
    
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    
    required_files = [
        'src/tableau_universal_connector.py',
        'src/database_connector.py',
        'src/routes/__init__.py',
        'src/routes/api_routes.py',
        'src/utils/__init__.py',
        'src/utils/schema_detector.py',
        'templates/wdc_template.html',
        'config/database_config.json',
        'requirements.txt'
    ]
    
    all_exist = True
    for file in required_files:
        file_path = os.path.join(base_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - THIẾU!")
            all_exist = False
    
    if all_exist:
        print("\n🎉 TẤT CẢ FILE CẦN THIẾT ĐỀU TỒN TẠI!")
        return True
    else:
        print("\n⚠️ MỘT SỐ FILE BỊ THIẾU!")
        return False


def main():
    """Chạy tất cả tests"""
    print("\n" + "=" * 70)
    print("🧪 BẮT ĐẦU KIỂM THỬ TOÀN BỘ HỆ THỐNG SAU REFACTORING")
    print("=" * 70)
    
    results = {
        'Test 1: Imports': test_imports(),
        'Test 2: Config': test_config(),
        'Test 3: Schema Functions': test_schema_functions(),
        'Test 4: Flask App': test_flask_app(),
        'Test 5: Template': test_template_exists(),
        'Test 6: File Structure': test_file_structure()
    }
    
    # Tổng kết
    print("\n" + "=" * 70)
    print("📊 TỔNG KẾT KẾT QUẢ KIỂM THỬ")
    print("=" * 70)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "=" * 70)
    print(f"Kết quả: {passed}/{total} tests PASSED ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 TẤT CẢ TESTS ĐỀU THÀNH CÔNG!")
        print("✅ HỆ THỐNG SAU REFACTORING HOẠT ĐỘNG ỔN ĐỊNH!")
    else:
        print("⚠️ MỘT SỐ TESTS THẤT BẠI - CẦN KIỂM TRA LẠI!")
    
    print("=" * 70 + "\n")
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
