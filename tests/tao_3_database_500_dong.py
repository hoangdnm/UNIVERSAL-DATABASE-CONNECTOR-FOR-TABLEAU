#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
========================================
SCRIPT TẠO 3 DATABASE VỚI DỮ LIỆU MẪU
========================================

Mục đích: Tạo 3 database khác nhau, mỗi database có 4-5 bảng, 
          mỗi bảng chứa khoảng 500 dòng dữ liệu

Danh sách database:
1. SalesDB - Quản lý bán hàng (5 bảng)
2. InventoryDB - Quản lý kho (4 bảng)  
3. EmployeeDB - Quản lý nhân viên (5 bảng)
"""

import pymssql
import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

# ============================================
# PHẦN 1: CẤU HÌNH KẾT NỐI
# ============================================

CAU_HINH_KET_NOI = {
    'server': '127.0.0.1',
    'port': 1235,
    'user': 'sa',
    'password': 'YourStrong!Pass123'
}

# ============================================
# PHẦN 2: DANH SÁCH DỮ LIỆU MẪU
# ============================================

# Danh sách tên khách hàng
DANH_SACH_TEN = [
    "Nguyễn Văn", "Trần Thị", "Lê Văn", "Phạm Thị", "Hoàng Văn",
    "Huỳnh Thị", "Phan Văn", "Vũ Thị", "Đặng Văn", "Bùi Thị",
    "Đỗ Văn", "Hồ Thị", "Ngô Văn", "Dương Thị", "Lý Văn"
]

DANH_SACH_HO = [
    "An", "Bình", "Cường", "Dũng", "Em", "Phương", "Giang", "Hà",
    "Khoa", "Linh", "Minh", "Nam", "Phúc", "Quang", "Sơn", "Tâm",
    "Uyên", "Vân", "Xuân", "Yến"
]

# Danh sách sản phẩm
DANH_SACH_SAN_PHAM = [
    "Laptop Dell", "Laptop HP", "Laptop Asus", "Laptop Lenovo",
    "iPhone 15", "iPhone 14", "Samsung Galaxy S24", "Xiaomi Redmi",
    "Chuột Logitech", "Bàn phím Corsair", "Tai nghe Sony", "Webcam",
    "Màn hình LG", "Màn hình Samsung", "SSD Kingston", "RAM Corsair",
    "Case PC", "Nguồn Cooler Master", "Card đồ họa RTX", "Mainboard"
]

# Danh sách phòng ban
DANH_SACH_PHONG_BAN = [
    "Kinh doanh", "Marketing", "Kế toán", "Nhân sự", "IT",
    "Vận hành", "Dịch vụ khách hàng", "R&D", "QA", "Legal"
]

# Danh sách chức vụ
DANH_SACH_CHUC_VU = [
    "Nhân viên", "Trưởng nhóm", "Quản lý", "Giám đốc", 
    "Chuyên viên", "Kỹ sư", "Phó giám đốc"
]

# Danh sách địa chỉ
DANH_SACH_TINH_THANH = [
    "Hà Nội", "TP.HCM", "Đà Nẵng", "Hải Phòng", "Cần Thơ",
    "Biên Hòa", "Vũng Tàu", "Nha Trang", "Huế", "Vinh"
]

# ============================================
# PHẦN 3: HÀM TẠO DATABASE VÀ BẢNG
# ============================================

def ket_noi_sql_server(database: str = 'master') -> pymssql.Connection:
    """
    Kết nối tới SQL Server
    
    Tham số:
        database: Tên database cần kết nối
        
    Trả về:
        pymssql.Connection: Đối tượng kết nối
    """
    return pymssql.connect(
        server=CAU_HINH_KET_NOI['server'],
        port=CAU_HINH_KET_NOI['port'],
        user=CAU_HINH_KET_NOI['user'],
        password=CAU_HINH_KET_NOI['password'],
        database=database
    )

def tao_database(ten_database: str) -> bool:
    """
    Tạo database mới (xóa nếu đã tồn tại)
    
    Tham số:
        ten_database: Tên database cần tạo
        
    Trả về:
        bool: True nếu thành công
    """
    try:
        ket_noi = ket_noi_sql_server('master')
        ket_noi.autocommit(True)
        con_tro = ket_noi.cursor()
        
        # Xóa database nếu tồn tại
        print(f"   🗑️ Xóa database '{ten_database}' (nếu tồn tại)...")
        con_tro.execute(f"""
            IF EXISTS (SELECT name FROM sys.databases WHERE name = '{ten_database}')
            BEGIN
                ALTER DATABASE [{ten_database}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
                DROP DATABASE [{ten_database}];
            END
        """)
        
        # Tạo database mới
        print(f"   ➕ Tạo database '{ten_database}'...")
        con_tro.execute(f"CREATE DATABASE [{ten_database}]")
        
        ket_noi.close()
        print(f"   ✅ Database '{ten_database}' đã được tạo")
        return True
        
    except Exception as e:
        print(f"   ❌ Lỗi tạo database '{ten_database}': {e}")
        return False

def tao_bang(ket_noi: pymssql.Connection, cau_lenh_sql: str, ten_bang: str) -> bool:
    """
    Tạo bảng trong database
    
    Tham số:
        ket_noi: Kết nối database
        cau_lenh_sql: Câu lệnh SQL tạo bảng
        ten_bang: Tên bảng
        
    Trả về:
        bool: True nếu thành công
    """
    try:
        con_tro = ket_noi.cursor()
        con_tro.execute(cau_lenh_sql)
        ket_noi.commit()
        print(f"      ✅ Bảng '{ten_bang}' đã được tạo")
        return True
    except Exception as e:
        print(f"      ❌ Lỗi tạo bảng '{ten_bang}': {e}")
        return False

# ============================================
# PHẦN 4: TẠO DATABASE 1 - SALESDB (BÁN HÀNG)
# ============================================

def tao_salesdb():
    """
    Tạo database SalesDB với 5 bảng:
    1. Customers (Khách hàng) - 500 dòng
    2. Products (Sản phẩm) - 500 dòng
    3. Orders (Đơn hàng) - 500 dòng
    4. OrderDetails (Chi tiết đơn) - 500 dòng
    5. Payments (Thanh toán) - 500 dòng
    """
    print("\n" + "=" * 60)
    print("📊 DATABASE 1: SALESDB (QUẢN LÝ BÁN HÀNG)")
    print("=" * 60)
    
    # Tạo database
    if not tao_database('SalesDB'):
        return False
    
    # Kết nối tới database vừa tạo
    ket_noi = ket_noi_sql_server('SalesDB')
    
    # Bảng 1: Customers
    print("\n   📋 Tạo bảng Customers...")
    tao_bang(ket_noi, """
        CREATE TABLE Customers (
            CustomerID INT PRIMARY KEY IDENTITY(1,1),
            FullName NVARCHAR(100) NOT NULL,
            Email NVARCHAR(100),
            Phone NVARCHAR(20),
            Address NVARCHAR(200),
            City NVARCHAR(50),
            CreatedDate DATETIME DEFAULT GETDATE()
        )
    """, "Customers")
    
    # Bảng 2: Products
    print("   📋 Tạo bảng Products...")
    tao_bang(ket_noi, """
        CREATE TABLE Products (
            ProductID INT PRIMARY KEY IDENTITY(1,1),
            ProductName NVARCHAR(100) NOT NULL,
            Category NVARCHAR(50),
            Price DECIMAL(18,2) NOT NULL,
            Stock INT DEFAULT 0,
            Description NVARCHAR(500)
        )
    """, "Products")
    
    # Bảng 3: Orders
    print("   📋 Tạo bảng Orders...")
    tao_bang(ket_noi, """
        CREATE TABLE Orders (
            OrderID INT PRIMARY KEY IDENTITY(1,1),
            CustomerID INT,
            OrderDate DATETIME DEFAULT GETDATE(),
            TotalAmount DECIMAL(18,2),
            Status NVARCHAR(20),
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
        )
    """, "Orders")
    
    # Bảng 4: OrderDetails
    print("   📋 Tạo bảng OrderDetails...")
    tao_bang(ket_noi, """
        CREATE TABLE OrderDetails (
            DetailID INT PRIMARY KEY IDENTITY(1,1),
            OrderID INT,
            ProductID INT,
            Quantity INT NOT NULL,
            UnitPrice DECIMAL(18,2) NOT NULL,
            Subtotal DECIMAL(18,2),
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
            FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
        )
    """, "OrderDetails")
    
    # Bảng 5: Payments
    print("   📋 Tạo bảng Payments...")
    tao_bang(ket_noi, """
        CREATE TABLE Payments (
            PaymentID INT PRIMARY KEY IDENTITY(1,1),
            OrderID INT,
            PaymentDate DATETIME DEFAULT GETDATE(),
            Amount DECIMAL(18,2),
            PaymentMethod NVARCHAR(50),
            Status NVARCHAR(20),
            FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
        )
    """, "Payments")
    
    # Sinh dữ liệu
    print("\n   🔄 Sinh dữ liệu 500 dòng cho mỗi bảng...")
    sinh_du_lieu_salesdb(ket_noi)
    
    ket_noi.close()
    print("\n   ✅ Hoàn thành SalesDB!")
    return True

def sinh_du_lieu_salesdb(ket_noi: pymssql.Connection):
    """Sinh 500 dòng dữ liệu cho SalesDB"""
    con_tro = ket_noi.cursor()
    
    # 1. Customers (500 dòng)
    print("      📝 Customers (500 dòng)...")
    for i in range(500):
        ten = f"{random.choice(DANH_SACH_TEN)} {random.choice(DANH_SACH_HO)}"
        email = f"{ten.lower().replace(' ', '.')}@email.com"
        phone = f"09{random.randint(10000000, 99999999)}"
        dia_chi = f"{random.randint(1, 500)} Đường {random.randint(1, 50)}"
        thanh_pho = random.choice(DANH_SACH_TINH_THANH)
        
        con_tro.execute("""
            INSERT INTO Customers (FullName, Email, Phone, Address, City)
            VALUES (%s, %s, %s, %s, %s)
        """, (ten, email, phone, dia_chi, thanh_pho))
    ket_noi.commit()
    
    # 2. Products (500 dòng)
    print("      📝 Products (500 dòng)...")
    danh_muc = ["Laptop", "Điện thoại", "Phụ kiện", "Linh kiện", "Màn hình"]
    for i in range(500):
        ten_sp = f"{random.choice(DANH_SACH_SAN_PHAM)} #{i+1}"
        category = random.choice(danh_muc)
        gia = round(random.uniform(100000, 50000000), 2)
        ton_kho = random.randint(0, 1000)
        
        con_tro.execute("""
            INSERT INTO Products (ProductName, Category, Price, Stock, Description)
            VALUES (%s, %s, %s, %s, %s)
        """, (ten_sp, category, gia, ton_kho, f"Mô tả {ten_sp}"))
    ket_noi.commit()
    
    # 3. Orders (500 dòng)
    print("      📝 Orders (500 dòng)...")
    trang_thai = ["Chờ xử lý", "Đang giao", "Hoàn thành", "Đã hủy"]
    for i in range(500):
        customer_id = random.randint(1, 500)
        ngay_dat = datetime.now() - timedelta(days=random.randint(0, 365))
        tong_tien = round(random.uniform(100000, 10000000), 2)
        status = random.choice(trang_thai)
        
        con_tro.execute("""
            INSERT INTO Orders (CustomerID, OrderDate, TotalAmount, Status)
            VALUES (%s, %s, %s, %s)
        """, (customer_id, ngay_dat, tong_tien, status))
    ket_noi.commit()
    
    # 4. OrderDetails (500 dòng)
    print("      📝 OrderDetails (500 dòng)...")
    for i in range(500):
        order_id = random.randint(1, 500)
        product_id = random.randint(1, 500)
        so_luong = random.randint(1, 10)
        don_gia = round(random.uniform(100000, 5000000), 2)
        thanh_tien = round(so_luong * don_gia, 2)
        
        con_tro.execute("""
            INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice, Subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, product_id, so_luong, don_gia, thanh_tien))
    ket_noi.commit()
    
    # 5. Payments (500 dòng)
    print("      📝 Payments (500 dòng)...")
    phuong_thuc = ["Tiền mặt", "Chuyển khoản", "Thẻ tín dụng", "Ví điện tử"]
    for i in range(500):
        order_id = random.randint(1, 500)
        ngay_tt = datetime.now() - timedelta(days=random.randint(0, 365))
        so_tien = round(random.uniform(100000, 10000000), 2)
        pt_tt = random.choice(phuong_thuc)
        status = random.choice(["Thành công", "Thất bại", "Chờ xác nhận"])
        
        con_tro.execute("""
            INSERT INTO Payments (OrderID, PaymentDate, Amount, PaymentMethod, Status)
            VALUES (%s, %s, %s, %s, %s)
        """, (order_id, ngay_tt, so_tien, pt_tt, status))
    ket_noi.commit()

# ============================================
# PHẦN 5: TẠO DATABASE 2 - INVENTORYDB (KHO)
# ============================================

def tao_inventorydb():
    """
    Tạo database InventoryDB với 4 bảng:
    1. Warehouses (Kho) - 500 dòng
    2. Items (Mặt hàng) - 500 dòng
    3. StockMovements (Xuất nhập kho) - 500 dòng
    4. Suppliers (Nhà cung cấp) - 500 dòng
    """
    print("\n" + "=" * 60)
    print("📦 DATABASE 2: INVENTORYDB (QUẢN LÝ KHO)")
    print("=" * 60)
    
    if not tao_database('InventoryDB'):
        return False
    
    ket_noi = ket_noi_sql_server('InventoryDB')
    
    # Bảng 1: Warehouses
    print("\n   📋 Tạo bảng Warehouses...")
    tao_bang(ket_noi, """
        CREATE TABLE Warehouses (
            WarehouseID INT PRIMARY KEY IDENTITY(1,1),
            WarehouseName NVARCHAR(100) NOT NULL,
            Location NVARCHAR(200),
            City NVARCHAR(50),
            Capacity INT,
            ManagerName NVARCHAR(100)
        )
    """, "Warehouses")
    
    # Bảng 2: Items
    print("   📋 Tạo bảng Items...")
    tao_bang(ket_noi, """
        CREATE TABLE Items (
            ItemID INT PRIMARY KEY IDENTITY(1,1),
            ItemCode NVARCHAR(50) NOT NULL,
            ItemName NVARCHAR(100) NOT NULL,
            Category NVARCHAR(50),
            Unit NVARCHAR(20),
            MinStock INT DEFAULT 0,
            CurrentStock INT DEFAULT 0
        )
    """, "Items")
    
    # Bảng 3: StockMovements
    print("   📋 Tạo bảng StockMovements...")
    tao_bang(ket_noi, """
        CREATE TABLE StockMovements (
            MovementID INT PRIMARY KEY IDENTITY(1,1),
            ItemID INT,
            WarehouseID INT,
            MovementType NVARCHAR(20),
            Quantity INT NOT NULL,
            MovementDate DATETIME DEFAULT GETDATE(),
            Notes NVARCHAR(500),
            FOREIGN KEY (ItemID) REFERENCES Items(ItemID),
            FOREIGN KEY (WarehouseID) REFERENCES Warehouses(WarehouseID)
        )
    """, "StockMovements")
    
    # Bảng 4: Suppliers
    print("   📋 Tạo bảng Suppliers...")
    tao_bang(ket_noi, """
        CREATE TABLE Suppliers (
            SupplierID INT PRIMARY KEY IDENTITY(1,1),
            SupplierName NVARCHAR(100) NOT NULL,
            ContactPerson NVARCHAR(100),
            Phone NVARCHAR(20),
            Email NVARCHAR(100),
            Address NVARCHAR(200),
            Rating DECIMAL(3,2)
        )
    """, "Suppliers")
    
    # Sinh dữ liệu
    print("\n   🔄 Sinh dữ liệu 500 dòng cho mỗi bảng...")
    sinh_du_lieu_inventorydb(ket_noi)
    
    ket_noi.close()
    print("\n   ✅ Hoàn thành InventoryDB!")
    return True

def sinh_du_lieu_inventorydb(ket_noi: pymssql.Connection):
    """Sinh 500 dòng dữ liệu cho InventoryDB"""
    con_tro = ket_noi.cursor()
    
    # 1. Warehouses (500 dòng)
    print("      📝 Warehouses (500 dòng)...")
    for i in range(500):
        ten_kho = f"Kho {chr(65 + (i % 26))}{i+1}"
        dia_diem = f"{random.randint(1, 500)} KCN {random.choice(['A', 'B', 'C'])}"
        thanh_pho = random.choice(DANH_SACH_TINH_THANH)
        suc_chua = random.randint(1000, 100000)
        quan_ly = f"{random.choice(DANH_SACH_TEN)} {random.choice(DANH_SACH_HO)}"
        
        con_tro.execute("""
            INSERT INTO Warehouses (WarehouseName, Location, City, Capacity, ManagerName)
            VALUES (%s, %s, %s, %s, %s)
        """, (ten_kho, dia_diem, thanh_pho, suc_chua, quan_ly))
    ket_noi.commit()
    
    # 2. Items (500 dòng)
    print("      📝 Items (500 dòng)...")
    danh_muc = ["Nguyên liệu", "Thành phẩm", "Bán thành phẩm", "Phụ kiện", "Công cụ"]
    don_vi = ["Cái", "Hộp", "Thùng", "Kg", "Mét"]
    for i in range(500):
        ma_hang = f"ITEM{i+1:04d}"
        ten_hang = f"Mặt hàng {random.choice(['A', 'B', 'C', 'D'])} {i+1}"
        loai = random.choice(danh_muc)
        dv = random.choice(don_vi)
        ton_toi_thieu = random.randint(10, 100)
        ton_hien_tai = random.randint(0, 1000)
        
        con_tro.execute("""
            INSERT INTO Items (ItemCode, ItemName, Category, Unit, MinStock, CurrentStock)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ma_hang, ten_hang, loai, dv, ton_toi_thieu, ton_hien_tai))
    ket_noi.commit()
    
    # 3. StockMovements (500 dòng)
    print("      📝 StockMovements (500 dòng)...")
    loai_gd = ["Nhập kho", "Xuất kho", "Chuyển kho", "Điều chỉnh"]
    for i in range(500):
        item_id = random.randint(1, 500)
        warehouse_id = random.randint(1, 500)
        loai = random.choice(loai_gd)
        so_luong = random.randint(1, 500)
        ngay_gd = datetime.now() - timedelta(days=random.randint(0, 365))
        ghi_chu = f"Giao dịch {loai} #{i+1}"
        
        con_tro.execute("""
            INSERT INTO StockMovements (ItemID, WarehouseID, MovementType, Quantity, MovementDate, Notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (item_id, warehouse_id, loai, so_luong, ngay_gd, ghi_chu))
    ket_noi.commit()
    
    # 4. Suppliers (500 dòng)
    print("      📝 Suppliers (500 dòng)...")
    for i in range(500):
        ten_ncc = f"Công ty {random.choice(['TNHH', 'CP', 'MTV'])} {random.choice(DANH_SACH_HO)} {i+1}"
        nguoi_lh = f"{random.choice(DANH_SACH_TEN)} {random.choice(DANH_SACH_HO)}"
        phone = f"02{random.randint(10000000, 99999999)}"
        email = f"contact{i+1}@company.com"
        dia_chi = f"{random.randint(1, 500)} Đường {random.randint(1, 50)}, {random.choice(DANH_SACH_TINH_THANH)}"
        danh_gia = round(random.uniform(3.0, 5.0), 2)
        
        con_tro.execute("""
            INSERT INTO Suppliers (SupplierName, ContactPerson, Phone, Email, Address, Rating)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ten_ncc, nguoi_lh, phone, email, dia_chi, danh_gia))
    ket_noi.commit()

# ============================================
# PHẦN 6: TẠO DATABASE 3 - EMPLOYEEDB (NHÂN VIÊN)
# ============================================

def tao_employeedb():
    """
    Tạo database EmployeeDB với 5 bảng:
    1. Employees (Nhân viên) - 500 dòng
    2. Departments (Phòng ban) - 500 dòng
    3. Salaries (Lương) - 500 dòng
    4. Attendance (Chấm công) - 500 dòng
    5. Benefits (Phúc lợi) - 500 dòng
    """
    print("\n" + "=" * 60)
    print("👥 DATABASE 3: EMPLOYEEDB (QUẢN LÝ NHÂN VIÊN)")
    print("=" * 60)
    
    if not tao_database('EmployeeDB'):
        return False
    
    ket_noi = ket_noi_sql_server('EmployeeDB')
    
    # Bảng 1: Employees
    print("\n   📋 Tạo bảng Employees...")
    tao_bang(ket_noi, """
        CREATE TABLE Employees (
            EmployeeID INT PRIMARY KEY IDENTITY(1,1),
            EmployeeCode NVARCHAR(20) NOT NULL,
            FullName NVARCHAR(100) NOT NULL,
            BirthDate DATE,
            Gender NVARCHAR(10),
            Phone NVARCHAR(20),
            Email NVARCHAR(100),
            Position NVARCHAR(50),
            HireDate DATE,
            Status NVARCHAR(20)
        )
    """, "Employees")
    
    # Bảng 2: Departments
    print("   📋 Tạo bảng Departments...")
    tao_bang(ket_noi, """
        CREATE TABLE Departments (
            DepartmentID INT PRIMARY KEY IDENTITY(1,1),
            DepartmentName NVARCHAR(100) NOT NULL,
            ManagerID INT,
            Location NVARCHAR(100),
            Budget DECIMAL(18,2),
            EmployeeCount INT DEFAULT 0
        )
    """, "Departments")
    
    # Bảng 3: Salaries
    print("   📋 Tạo bảng Salaries...")
    tao_bang(ket_noi, """
        CREATE TABLE Salaries (
            SalaryID INT PRIMARY KEY IDENTITY(1,1),
            EmployeeID INT,
            BaseSalary DECIMAL(18,2) NOT NULL,
            Bonus DECIMAL(18,2) DEFAULT 0,
            Deductions DECIMAL(18,2) DEFAULT 0,
            NetSalary DECIMAL(18,2),
            PaymentDate DATE,
            FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
        )
    """, "Salaries")
    
    # Bảng 4: Attendance
    print("   📋 Tạo bảng Attendance...")
    tao_bang(ket_noi, """
        CREATE TABLE Attendance (
            AttendanceID INT PRIMARY KEY IDENTITY(1,1),
            EmployeeID INT,
            WorkDate DATE NOT NULL,
            CheckIn TIME,
            CheckOut TIME,
            WorkHours DECIMAL(5,2),
            Status NVARCHAR(20),
            FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
        )
    """, "Attendance")
    
    # Bảng 5: Benefits
    print("   📋 Tạo bảng Benefits...")
    tao_bang(ket_noi, """
        CREATE TABLE Benefits (
            BenefitID INT PRIMARY KEY IDENTITY(1,1),
            EmployeeID INT,
            BenefitType NVARCHAR(50) NOT NULL,
            Amount DECIMAL(18,2),
            StartDate DATE,
            EndDate DATE,
            Status NVARCHAR(20),
            FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
        )
    """, "Benefits")
    
    # Sinh dữ liệu
    print("\n   🔄 Sinh dữ liệu 500 dòng cho mỗi bảng...")
    sinh_du_lieu_employeedb(ket_noi)
    
    ket_noi.close()
    print("\n   ✅ Hoàn thành EmployeeDB!")
    return True

def sinh_du_lieu_employeedb(ket_noi: pymssql.Connection):
    """Sinh 500 dòng dữ liệu cho EmployeeDB"""
    con_tro = ket_noi.cursor()
    
    # 1. Employees (500 dòng)
    print("      📝 Employees (500 dòng)...")
    gioi_tinh = ["Nam", "Nữ"]
    trang_thai = ["Đang làm", "Nghỉ việc", "Tạm nghỉ"]
    for i in range(500):
        ma_nv = f"NV{i+1:04d}"
        ten = f"{random.choice(DANH_SACH_TEN)} {random.choice(DANH_SACH_HO)}"
        ngay_sinh = datetime.now() - timedelta(days=random.randint(7300, 18250))  # 20-50 tuổi
        gt = random.choice(gioi_tinh)
        phone = f"09{random.randint(10000000, 99999999)}"
        email = f"{ma_nv.lower()}@company.com"
        chuc_vu = random.choice(DANH_SACH_CHUC_VU)
        ngay_vao = datetime.now() - timedelta(days=random.randint(0, 3650))
        tt = random.choice(trang_thai)
        
        con_tro.execute("""
            INSERT INTO Employees (EmployeeCode, FullName, BirthDate, Gender, Phone, Email, Position, HireDate, Status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (ma_nv, ten, ngay_sinh, gt, phone, email, chuc_vu, ngay_vao, tt))
    ket_noi.commit()
    
    # 2. Departments (500 dòng)
    print("      📝 Departments (500 dòng)...")
    for i in range(500):
        ten_pb = f"Phòng {random.choice(DANH_SACH_PHONG_BAN)} {i+1}"
        manager = random.randint(1, 500)
        vi_tri = f"Tầng {random.randint(1, 20)}, Tòa nhà {random.choice(['A', 'B', 'C'])}"
        ngan_sach = round(random.uniform(100000000, 1000000000), 2)
        so_nv = random.randint(5, 50)
        
        con_tro.execute("""
            INSERT INTO Departments (DepartmentName, ManagerID, Location, Budget, EmployeeCount)
            VALUES (%s, %s, %s, %s, %s)
        """, (ten_pb, manager, vi_tri, ngan_sach, so_nv))
    ket_noi.commit()
    
    # 3. Salaries (500 dòng)
    print("      📝 Salaries (500 dòng)...")
    for i in range(500):
        emp_id = random.randint(1, 500)
        luong_co_ban = round(random.uniform(5000000, 50000000), 2)
        thuong = round(random.uniform(0, 10000000), 2)
        khau_tru = round(random.uniform(0, 2000000), 2)
        luong_thuc = round(luong_co_ban + thuong - khau_tru, 2)
        ngay_tt = datetime.now() - timedelta(days=random.randint(0, 365))
        
        con_tro.execute("""
            INSERT INTO Salaries (EmployeeID, BaseSalary, Bonus, Deductions, NetSalary, PaymentDate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (emp_id, luong_co_ban, thuong, khau_tru, luong_thuc, ngay_tt))
    ket_noi.commit()
    
    # 4. Attendance (500 dòng)
    print("      📝 Attendance (500 dòng)...")
    trang_thai_cc = ["Đúng giờ", "Đi muộn", "Về sớm", "Nghỉ có phép", "Nghỉ không phép"]
    for i in range(500):
        emp_id = random.randint(1, 500)
        ngay_lam = datetime.now() - timedelta(days=random.randint(0, 365))
        gio_vao = f"{random.randint(7, 9):02d}:{random.randint(0, 59):02d}:00"
        gio_ra = f"{random.randint(17, 19):02d}:{random.randint(0, 59):02d}:00"
        gio_lam = round(random.uniform(6, 10), 2)
        tt_cc = random.choice(trang_thai_cc)
        
        con_tro.execute("""
            INSERT INTO Attendance (EmployeeID, WorkDate, CheckIn, CheckOut, WorkHours, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (emp_id, ngay_lam, gio_vao, gio_ra, gio_lam, tt_cc))
    ket_noi.commit()
    
    # 5. Benefits (500 dòng)
    print("      📝 Benefits (500 dòng)...")
    loai_pl = ["Bảo hiểm y tế", "Bảo hiểm xã hội", "Thưởng", "Trợ cấp", "Du lịch"]
    for i in range(500):
        emp_id = random.randint(1, 500)
        loai = random.choice(loai_pl)
        so_tien = round(random.uniform(500000, 10000000), 2)
        ngay_bd = datetime.now() - timedelta(days=random.randint(0, 365))
        ngay_kt = ngay_bd + timedelta(days=random.randint(30, 365))
        tt = random.choice(["Đang áp dụng", "Hết hạn", "Chờ duyệt"])
        
        con_tro.execute("""
            INSERT INTO Benefits (EmployeeID, BenefitType, Amount, StartDate, EndDate, Status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (emp_id, loai, so_tien, ngay_bd, ngay_kt, tt))
    ket_noi.commit()

# ============================================
# PHẦN 7: HÀM CHÍNH
# ============================================

def main():
    """
    Hàm chính - Tạo 3 database với dữ liệu mẫu
    """
    print("=" * 60)
    print("🚀 TẠO 3 DATABASE VỚI DỮ LIỆU MẪU")
    print("=" * 60)
    print(f"📅 Ngày tạo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"🎯 Mục tiêu:")
    print(f"   • 3 database khác nhau")
    print(f"   • Mỗi database có 4-5 bảng")
    print(f"   • Mỗi bảng có khoảng 500 dòng dữ liệu")
    print("")
    
    # Kiểm tra kết nối
    print("🔍 Kiểm tra kết nối SQL Server...")
    try:
        ket_noi_test = ket_noi_sql_server('master')
        ket_noi_test.close()
        print("   ✅ Kết nối SQL Server thành công!")
    except Exception as e:
        print(f"   ❌ Lỗi kết nối: {e}")
        print("\n💡 Hướng dẫn khắc phục:")
        print("   1. Kiểm tra Docker đang chạy: docker ps")
        print("   2. Start SQL Server: cd config && docker compose up -d")
        print("   3. Kiểm tra port 1235: netstat -an | grep 1235")
        return
    
    # Xác nhận
    xac_nhan = input("\n⚠️ Script sẽ XÓA và TẠO LẠI 3 database. Tiếp tục? (y/N): ").lower()
    if xac_nhan != 'y':
        print("❌ Đã hủy!")
        return
    
    # Tạo từng database
    thanh_cong = 0
    
    if tao_salesdb():
        thanh_cong += 1
    
    if tao_inventorydb():
        thanh_cong += 1
    
    if tao_employeedb():
        thanh_cong += 1
    
    # Tổng kết
    print("\n" + "=" * 60)
    print(f"📊 KẾT QUẢ: Đã tạo {thanh_cong}/3 database thành công!")
    print("=" * 60)
    
    if thanh_cong == 3:
        print("\n🎉 HOÀN THÀNH!")
        print("\n📋 Danh sách database:")
        print("   1. SalesDB - 5 bảng, ~2500 dòng")
        print("   2. InventoryDB - 4 bảng, ~2000 dòng")
        print("   3. EmployeeDB - 5 bảng, ~2500 dòng")
        print("\n🧪 Kiểm tra:")
        print("   python tests/test_hieu_suat_du_lieu_lon.py")
        print("\n🚀 Chạy server:")
        print("   python src/tableau_universal_connector.py")
    else:
        print("\n⚠️ Một số database tạo thất bại!")

if __name__ == "__main__":
    main()
