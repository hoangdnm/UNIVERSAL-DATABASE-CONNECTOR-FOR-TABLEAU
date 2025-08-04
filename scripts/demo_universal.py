#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script demo tính năng Universal Database Connector
Dự án tốt nghiệp - Kết nối với nhiều loại database
"""

def demo_ket_noi_nhieu_database():
    """
    Demo kết nối với nhiều database khác nhau
    """
    print("🎯 DEMO UNIVERSAL DATABASE CONNECTOR")
    print("=" * 60)
    
    print("📋 Các bước thực hiện:")
    print("1. Cấu hình kết nối database")
    print("2. Phân tích cấu trúc bảng") 
    print("3. Chạy Universal API")
    print("4. Kết nối Tableau")
    print("")
    
    print("🚀 Ưu điểm của dự án:")
    print("✅ Không cần code lại khi đổi database")
    print("✅ Tự động phát hiện schema của bất kỳ bảng nào")
    print("✅ Linh hoạt với Tableau cho mọi loại dữ liệu")
    print("✅ Hỗ trợ SQL WHERE clause tùy chỉnh")
    print("✅ Có thể kết nối với:")
    print("   - Database doanh nghiệp")
    print("   - Database học tập") 
    print("   - Database thử nghiệm")
    print("   - Bất kỳ SQL Server nào")
    print("")
    
    # Demo các database mẫu
    databases_mau = [
        {
            "name": "Northwind (Database mẫu)",
            "description": "Database quản lý bán hàng cổ điển",
            "tables": ["Customers", "Orders", "Products", "Categories"]
        },
        {
            "name": "AdventureWorks (Microsoft Sample)",
            "description": "Database mẫu của Microsoft",
            "tables": ["Person.Person", "Sales.SalesOrderHeader", "Production.Product"]
        },
        {
            "name": "Company HR Database",
            "description": "Database nhân sự công ty",
            "tables": ["Employees", "Departments", "Salaries", "Projects"]
        },
        {
            "name": "E-commerce Database",
            "description": "Database thương mại điện tử",
            "tables": ["Users", "Products", "Orders", "Reviews"]
        }
    ]
    
    print("📊 VÍ DỤ CÁC DATABASE CÓ THỂ KẾT NỐI:")
    for i, db in enumerate(databases_mau, 1):
        print(f"\n{i}. {db['name']}")
        print(f"   📝 {db['description']}")
        print(f"   📋 Bảng: {', '.join(db['tables'])}")
    
    print("\n" + "=" * 60)
    print("🔧 HƯỚNG DẪN SỬ DỤNG:")
    print("")
    print("Bước 1: Cấu hình database")
    print("   python scripts/cau_hinh_database.py")
    print("")
    print("Bước 2: Chạy Universal Connector")
    print("   python src/tableau_universal_connector.py")
    print("")
    print("Bước 3: Mở Tableau Desktop")
    print("   - Chọn Web Data Connector")
    print("   - URL: http://127.0.0.1:5002")
    print("   - Chọn bảng từ dropdown")
    print("   - Chọn số lượng dòng")
    print("   - Có thể thêm WHERE clause")
    print("   - Kết nối!")
    print("")
    print("🎉 Kết quả: Tableau sẽ hiển thị dữ liệu từ bất kỳ bảng nào!")

def test_cac_loai_du_lieu():
    """
    Test với các loại dữ liệu khác nhau
    """
    print("\n🧪 TEST VỚI CÁC LOẠI DỮ LIỆU:")
    print("-" * 40)
    
    test_cases = [
        {
            "loai": "Dữ liệu bán hàng",
            "sql_where": "total_amount > 1000000",
            "mo_ta": "Lọc đơn hàng lớn hơn 1 triệu"
        },
        {
            "loai": "Dữ liệu nhân sự", 
            "sql_where": "salary >= 20000000 AND department = 'IT'",
            "mo_ta": "Nhân viên IT có lương >= 20 triệu"
        },
        {
            "loai": "Dữ liệu khách hàng",
            "sql_where": "age BETWEEN 25 AND 40",
            "mo_ta": "Khách hàng từ 25-40 tuổi"
        },
        {
            "loai": "Dữ liệu sản phẩm",
            "sql_where": "price < 500000 AND category = 'Electronics'",
            "mo_ta": "Sản phẩm điện tử dưới 500K"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"{i}. {test['loai']}:")
        print(f"   WHERE: {test['sql_where']}")
        print(f"   📝 {test['mo_ta']}")
        print()

def main():
    """
    Hàm chính
    """
    demo_ket_noi_nhieu_database()
    test_cac_loai_du_lieu()
    
    print("🎓 ĐÁNH GIA DỰ ÁN:")
    print("✅ Tính linh hoạt cao: Kết nối với bất kỳ database nào")
    print("✅ Tự động hóa: Không cần config thủ công")
    print("✅ Thân thiện: Giao diện dễ sử dụng")
    print("✅ Mở rộng: Có thể áp dụng cho doanh nghiệp")
    print("✅ Tableau ready: Hoàn toàn tương thích")
    print("")
    print("🚀 DỰ ÁN ĐÃ NÂNG CẤP THÀNH CÔNG!")
    print("   Từ: Connector cố định cho 1 loại dữ liệu")
    print("   Thành: Universal Connector cho mọi database!")

if __name__ == "__main__":
    main()
