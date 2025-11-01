"""
========================================
BÀI 5: HOÀN THIỆN ỨNG DỤNG - TÍNH NĂNG NÂNG CAO
========================================

MỤC TIÊU:
---------
1. Lưu/tải lịch sử kết nối
2. Theme sáng/tối (Dark/Light mode)
3. Preview dữ liệu bảng trong Treeview
4. Xử lý lỗi toàn diện
5. Dialog cấu hình database
6. Xuất danh sách bảng ra file
7. Giao diện chuyên nghiệp

KIẾN THỨC MỚI:
--------------
- ttk.Treeview: Bảng hiển thị dữ liệu
- ttk.Notebook: Tab điều hướng
- Toplevel: Dialog/cửa sổ con
- JSON: Lưu/đọc cấu hình
- Try/Except: Xử lý lỗi
- Lambda: Hàm ẩn danh
- *args, **kwargs: Tham số linh hoạt

========================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from urllib.parse import urlencode
import webbrowser
from datetime import datetime
from typing import Dict, List, Optional
from PIL import Image, ImageTk

# ============================================
# PHẦN 1: KIỂM TRA PYODBC VÀ PYMSSQL
# ============================================

CO_PYODBC = False
CO_PYMSSQL = False

try:
    import pyodbc
    CO_PYODBC = True
    print("✓ pyodbc đã sẵn sàng - Hỗ trợ Windows Authentication")
except ImportError as e:
    print(f"⚠ Không thể import pyodbc: {e}")

try:
    import pymssql
    CO_PYMSSQL = True
    print("✓ pymssql đã sẵn sàng - Hỗ trợ SQL Server Authentication")
except ImportError as e:
    print(f"⚠ Không thể import pymssql: {e}")

if not CO_PYODBC and not CO_PYMSSQL:
    print("→ Sử dụng chế độ simulation")

# Import module ket noi database
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

try:
    import database_connector as db_conn
    CO_DATABASE_CONNECTOR = True
    print("✓ database_connector module đã sẵn sàng")
except ImportError as e:
    print(f"⚠ Không thể import database_connector: {e}")
    CO_DATABASE_CONNECTOR = False

# ============================================
# PHẦN 2: CÁC HÀM GIẢ LẬP
# ============================================

def doc_cau_hinh_database_gia_lap():
    """Đọc file cấu hình database"""
    # Dung module database_connector neu co
    if CO_DATABASE_CONNECTOR:
        return db_conn.doc_cau_hinh_database()
    
    # Fallback: doc truc tiep tu file
    config_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'config', 
        'database_config.json'
    )
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # Cấu hình mặc định (container hiện tại)
    return {
        "server": "127.0.0.1",
        "port": 1433,  # Container đang dùng port 1433
        "user": "sa",
        "password": "YourStrong!Pass123",
        "database": "master",
        "windows_auth": False
    }

def lay_danh_sach_database_gia_lap(config):
    """Lấy danh sách database"""
    # Dung module database_connector neu co
    if CO_DATABASE_CONNECTOR:
        try:
            return db_conn.lay_danh_sach_database()
        except Exception as e:
            print(f"Lỗi lấy danh sách database: {e}")
    
    # Fallback: tra ve du lieu gia lap
    return ["ECommerce_Test", "Inventory_DB", "Sales_DB", "HR_System", "Analytics"]

def lay_danh_sach_bang_gia_lap(config, database_name):
    """Lấy danh sách bảng"""
    # Dung module database_connector neu co
    if CO_DATABASE_CONNECTOR:
        try:
            return db_conn.lay_danh_sach_bang(database_name)
        except Exception as e:
            print(f"Lỗi lấy danh sách bảng: {e}")
    
    # Fallback: tra ve du lieu gia lap
    cac_bang_mau = {
        "ECommerce_Test": [
            "Customers", "Orders", "Products", "OrderDetails", 
            "Categories", "Suppliers", "Employees", "Shippers"
        ],
        "Inventory_DB": ["Items", "Warehouses", "Stock", "Suppliers", "Transfers"],
        "Sales_DB": ["Transactions", "Customers", "SalesReps", "Regions", "Targets"],
        "HR_System": ["Employees", "Departments", "Payroll", "Attendance", "Benefits"],
        "Analytics": ["WebTraffic", "UserBehavior", "Conversions", "Sessions", "Events"]
    }
    return cac_bang_mau.get(database_name, ["Table1", "Table2", "Table3"])

def lay_du_lieu_bang_gia_lap(config, database_name, table_name):
    """Lấy dữ liệu mẫu từ bảng (giả lập)"""
    # Trả về danh sách dictionary (mỗi dict = 1 dòng)
    if table_name == "Customers":
        return [
            {"CustomerID": 1, "Name": "Nguyễn Văn A", "Email": "a@example.com", "Phone": "0123456789"},
            {"CustomerID": 2, "Name": "Trần Thị B", "Email": "b@example.com", "Phone": "0987654321"},
            {"CustomerID": 3, "Name": "Lê Văn C", "Email": "c@example.com", "Phone": "0111222333"},
        ]
    elif table_name == "Orders":
        return [
            {"OrderID": 1001, "CustomerID": 1, "OrderDate": "2025-01-15", "Total": 500000},
            {"OrderID": 1002, "CustomerID": 2, "OrderDate": "2025-01-16", "Total": 750000},
            {"OrderID": 1003, "CustomerID": 1, "OrderDate": "2025-01-17", "Total": 1200000},
        ]
    else:
        return [
            {"ID": 1, "Column1": "Value 1", "Column2": "Data A"},
            {"ID": 2, "Column1": "Value 2", "Column2": "Data B"},
        ]

# ============================================
# PHẦN 3: CÁC HÀM KẾT NỐI THẬT
# ============================================

def doc_cau_hinh_database():
    """Đọc file cấu hình database từ JSON"""
    config_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'config', 
        'database_config.json'
    )
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {
        "server": "127.0.0.1",
        "port": 1235,
        "user": "sa",
        "password": "YourStrong!Pass123",
        "database": "master"
    }

def lay_danh_sach_database_that():
    """Lấy danh sách database từ SQL Server (kết nối thật)"""
    try:
        config = doc_cau_hinh_database()
        conn = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database='master'
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name 
            FROM sys.databases 
            WHERE name NOT IN ('master', 'tempdb', 'model', 'msdb')
            ORDER BY name
        """)
        databases = [row[0] for row in cursor.fetchall()]
        conn.close()
        print(f"✓ Tìm thấy {len(databases)} database: {databases}")
        return databases
    except Exception as e:
        print(f"⚠ Lỗi lấy danh sách database: {e}")
        return []

def lay_danh_sach_bang_that(config, database_name):
    """Lấy danh sách bảng từ database (kết nối thật)"""
    try:
        conn = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=database_name
        )
        cursor = conn.cursor()
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_TYPE = 'BASE TABLE'
            ORDER BY TABLE_NAME
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        print(f"✓ Tìm thấy {len(tables)} bảng trong {database_name}")
        return tables
    except Exception as e:
        print(f"⚠ Lỗi lấy danh sách bảng: {e}")
        return []

def lay_du_lieu_bang_that(config, database_name, table_name):
    """Lấy 100 dòng đầu từ bảng (kết nối thật)"""
    try:
        conn = pymssql.connect(
            server=config['server'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=database_name
        )
        cursor = conn.cursor(as_dict=True)
        cursor.execute(f"SELECT TOP 100 * FROM [{table_name}]")
        data = cursor.fetchall()
        conn.close()
        print(f"✓ Lấy được {len(data)} dòng từ {table_name}")
        return data
    except Exception as e:
        print(f"⚠ Lỗi lấy dữ liệu: {e}")
        return []

# ============================================
# PHẦN 4: CHỌN HÀM SỬ DỤNG
# ============================================

if CO_PYMSSQL:
    doc_config = doc_cau_hinh_database
    
    # Wrapper để tương thích với code cũ
    def lay_ds_database(config=None):
        """Lấy danh sách database"""
        return lay_danh_sach_database_that()
    
    def lay_ds_bang(config, database_name):
        """Lấy danh sách bảng"""
        return lay_danh_sach_bang_that(config, database_name)
    
    def lay_du_lieu_bang(config, database_name, table_name):
        """Lấy dữ liệu bảng"""
        return lay_du_lieu_bang_that(config, database_name, table_name)
else:
    doc_config = doc_cau_hinh_database_gia_lap
    lay_ds_database = lay_danh_sach_database_gia_lap
    lay_ds_bang = lay_danh_sach_bang_gia_lap
    lay_du_lieu_bang = lay_du_lieu_bang_gia_lap

# ============================================
# PHẦN 4: CẤU HÌNH THEME
# ============================================

# Theme Sáng (Light)
THEME_LIGHT = {
    "bg": "#f0f4f8",
    "fg": "#2c3e50",
    "header_bg": "#2c3e50",
    "header_fg": "white",
    "button_bg": "#3498db",
    "button_fg": "white",
    "success": "#27ae60",
    "error": "#e74c3c",
    "frame_bg": "white",
    "entry_bg": "white"
}

# Theme Tối (Dark)
THEME_DARK = {
    "bg": "#1e1e1e",
    "fg": "#e0e0e0",
    "header_bg": "#0d1117",
    "header_fg": "#58a6ff",
    "button_bg": "#238636",
    "button_fg": "white",
    "success": "#3fb950",
    "error": "#f85149",
    "frame_bg": "#2d2d2d",
    "entry_bg": "#0d1117"
}

# ============================================
# PHẦN 5: LỚP QUẢN LÝ LỊCH SỬ
# ============================================

class QuanLyLichSu:
    """
    Lớp quản lý lịch sử kết nối
    
    Lưu trữ:
    - Database đã chọn
    - Bảng đã chọn
    - URL đã tạo
    - Timestamp
    """
    
    def __init__(self, file_path: str = "connection_history.json"):
        """
        Khởi tạo quản lý lịch sử
        
        Tham số:
            file_path (str): Đường dẫn file lưu lịch sử
        """
        self.file_path = file_path
        self.lich_su: List[Dict] = self.tai_lich_su()
    
    def tai_lich_su(self) -> List[Dict]:
        """
        Tải lịch sử từ file JSON
        
        Trả về:
            List[Dict]: Danh sách lịch sử
        """
        if not os.path.exists(self.file_path):
            return []
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi đọc lịch sử: {e}")
            return []
    
    def luu_lich_su(self):
        """Lưu lịch sử vào file JSON"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.lich_su, f, ensure_ascii=False, indent=2)
            print(f"✓ Đã lưu lịch sử vào {self.file_path}")
        except Exception as e:
            print(f"✗ Lỗi lưu lịch sử: {e}")
    
    def them_muc(self, database: str, tables: List[str], url: str):
        """
        Thêm 1 mục vào lịch sử
        
        Tham số:
            database (str): Tên database
            tables (List[str]): Danh sách bảng
            url (str): URL đã tạo
        """
        muc_moi = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "database": database,
            "tables": tables,
            "url": url
        }
        
        # Thêm vào đầu danh sách (mới nhất lên trên)
        self.lich_su.insert(0, muc_moi)
        
        # Giữ tối đa 50 mục
        if len(self.lich_su) > 50:
            self.lich_su = self.lich_su[:50]
        
        self.luu_lich_su()
    
    def xoa_tat_ca(self):
        """Xóa toàn bộ lịch sử"""
        self.lich_su.clear()
        self.luu_lich_su()

# ============================================
# PHẦN 6: LỚP ỨNG DỤNG CHÍNH
# ============================================

class UngDungHoanChinh:
    """
    Ứng dụng hoàn chỉnh - Kết nối Tableau với SQL Server
    
    Tính năng:
    1. Chọn database và bảng
    2. Tạo URL kết nối
    3. Lịch sử kết nối
    4. Preview dữ liệu
    5. Dark/Light theme
    6. Cấu hình database
    7. Xuất danh sách bảng
    """
    
    def __init__(self):
        """Khởi tạo ứng dụng"""
        
        # ========== Tạo cửa sổ chính ==========
        self.cua_so = tk.Tk()
        self.cua_so.title("🔗 Tableau Database Connector - Pro Edition")
        self.cua_so.geometry("900x750")
        
        # ========== Thiết lập icon cửa sổ ==========
        try:
            icon_path = os.path.join(
                os.path.dirname(__file__),
                "assets",
                "images",
                "Windows 11 Colorfull Wallpaper.png"
            )
            if os.path.exists(icon_path):
                icon_img = Image.open(icon_path)
                # Resize xuống 64x64 để tránh lỗi X11 BadLength
                icon_img_resized = icon_img.resize((64, 64), Image.Resampling.LANCZOS)
                icon_photo = ImageTk.PhotoImage(icon_img_resized)
                self.cua_so.iconphoto(False, icon_photo)
                # Lưu reference để tránh garbage collection
                self.icon_photo = icon_photo
                print(f"✓ Đã load icon (64x64): {icon_path}")
        except Exception as e:
            print(f"⚠ Không thể load icon (bỏ qua): {e}")
        
        # ========== Biến lưu trữ ==========
        self.config: Optional[Dict] = None
        self.database_duoc_chon = tk.StringVar()
        self.cac_checkbox: Dict[str, tk.BooleanVar] = {}
        self.chon_tat_ca_var = tk.BooleanVar()
        self.theme_hien_tai = "light"  # "light" hoặc "dark"
        self.theme = THEME_LIGHT.copy()
        
        # Quản lý lịch sử
        self.quan_ly_lich_su = QuanLyLichSu()
        
        # ========== Tạo giao diện ==========
        self.tao_menu()
        self.tao_header()
        self.tao_tab_chinh()
        self.tao_thanh_trang_thai()
        
        # ========== Load dữ liệu ==========
        self.tai_cau_hinh()
        self.tai_danh_sach_database()
        
        # ========== Áp dụng theme ==========
        self.ap_dung_theme()
    
    # ============================================
    # PHẦN 7: TẠO MENU BAR
    # ============================================
    
    def tao_menu(self):
        """
        TẠO MENU BAR (THANH MENU)
        
        Cấu trúc:
        File    Edit    View    Help
        ├─ Open Config
        ├─ Save Config
        ├─ Exit
        """
        menubar = tk.Menu(self.cua_so)
        self.cua_so.config(menu=menubar)
        
        # Menu File
        menu_file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="⚙ Cấu Hình Database", command=self.mo_dialog_cau_hinh)
        menu_file.add_command(label="📂 Mở File Config", command=self.mo_file_config)
        menu_file.add_separator()
        menu_file.add_command(label="❌ Thoát", command=self.cua_so.quit)
        
        # Menu View
        menu_view = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=menu_view)
        menu_view.add_command(label="🌙 Chế Độ Tối", command=lambda: self.chuyen_theme("dark"))
        menu_view.add_command(label="☀ Chế Độ Sáng", command=lambda: self.chuyen_theme("light"))
        
        # Menu Help
        menu_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=menu_help)
        menu_help.add_command(label="📖 Hướng Dẫn", command=self.hien_thi_huong_dan)
        menu_help.add_command(label="ℹ Giới Thiệu", command=self.hien_thi_gioi_thieu)
    
    def tao_header(self):
        """Tạo header"""
        self.frame_header = tk.Frame(self.cua_so, height=80)
        self.frame_header.pack(fill='x')
        self.frame_header.pack_propagate(False)
        
        tieu_de = tk.Label(
            self.frame_header,
            text="🔗 TABLEAU DATABASE CONNECTOR",
            font=("Arial", 18, "bold")
        )
        tieu_de.pack(expand=True)
        
        # Lưu widget để cập nhật theme sau
        self.widgets_can_cap_nhat = [self.frame_header, tieu_de]
    
    # ============================================
    # PHẦN 8: TẠO TAB CHÍNH
    # ============================================
    
    def tao_tab_chinh(self):
        """
        TẠO TAB ĐIỀU HƯỚNG (ttk.Notebook)
        
        Các tab:
        1. Kết Nối - Chọn database/bảng, tạo URL
        2. Lịch Sử - Xem lịch sử kết nối
        3. Preview - Xem dữ liệu bảng
        """
        self.notebook = ttk.Notebook(self.cua_so)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tab 1: Kết Nối
        self.tab_ket_noi = tk.Frame(self.notebook)
        self.notebook.add(self.tab_ket_noi, text="  🔗 Kết Nối  ")
        self.tao_tab_ket_noi()
        
        # Tab 2: Lịch Sử
        self.tab_lich_su = tk.Frame(self.notebook)
        self.notebook.add(self.tab_lich_su, text="  📜 Lịch Sử  ")
        self.tao_tab_lich_su()
        
        # Tab 3: Preview
        self.tab_preview = tk.Frame(self.notebook)
        self.notebook.add(self.tab_preview, text="  👁 Preview Dữ Liệu  ")
        self.tao_tab_preview()
    
    def tao_tab_ket_noi(self):
        """Tạo nội dung tab Kết Nối"""
        # Phần chọn database
        self.tao_phan_chon_database(self.tab_ket_noi)
        
        # Phần chọn bảng
        self.tao_phan_chon_bang(self.tab_ket_noi)
        
        # Phần hiển thị URL
        self.tao_phan_ket_qua(self.tab_ket_noi)
        
        # Phần nút lệnh
        self.tao_phan_nut_lenh(self.tab_ket_noi)
    
    def tao_tab_lich_su(self):
        """
        TẠO TAB LỊCH SỬ - SỬ DỤNG TREEVIEW
        
        Treeview = bảng hiển thị dữ liệu dạng cột
        """
        frame = tk.Frame(self.tab_lich_su)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview với scrollbar
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Tạo Treeview
        columns = ("timestamp", "database", "tables", "url")
        self.tree_lich_su = ttk.Treeview(
            tree_frame,
            columns=columns,
            show='headings',  # Không hiện cột đầu tiên (icon)
            height=15
        )
        
        # Định nghĩa tiêu đề cột
        self.tree_lich_su.heading("timestamp", text="Thời Gian")
        self.tree_lich_su.heading("database", text="Database")
        self.tree_lich_su.heading("tables", text="Bảng")
        self.tree_lich_su.heading("url", text="URL")
        
        # Định nghĩa độ rộng cột
        self.tree_lich_su.column("timestamp", width=150)
        self.tree_lich_su.column("database", width=150)
        self.tree_lich_su.column("tables", width=200)
        self.tree_lich_su.column("url", width=350)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_lich_su.yview)
        self.tree_lich_su.configure(yscrollcommand=scrollbar.set)
        
        self.tree_lich_su.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Nút thao tác
        frame_nut = tk.Frame(frame)
        frame_nut.pack(fill='x', pady=(10, 0))
        
        tk.Button(
            frame_nut,
            text="🔄 Làm Mới",
            command=self.cap_nhat_lich_su,
            font=("Arial", 10)
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_nut,
            text="🗑 Xóa Tất Cả",
            command=self.xoa_lich_su,
            font=("Arial", 10)
        ).pack(side='left', padx=5)
        
        tk.Button(
            frame_nut,
            text="💾 Xuất File",
            command=self.xuat_lich_su,
            font=("Arial", 10)
        ).pack(side='left', padx=5)
        
        # Load lịch sử
        self.cap_nhat_lich_su()
    
    def tao_tab_preview(self):
        """
        TẠO TAB PREVIEW DỮ LIỆU
        
        Cho phép xem dữ liệu từ bảng trước khi kết nối Tableau
        """
        frame = tk.Frame(self.tab_preview)
        frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame chọn bảng
        frame_chon = tk.Frame(frame)
        frame_chon.pack(fill='x', pady=(0, 10))
        
        tk.Label(frame_chon, text="Chọn bảng:", font=("Arial", 10)).pack(side='left', padx=(0, 10))
        
        self.combo_bang_preview = ttk.Combobox(
            frame_chon,
            font=("Arial", 10),
            state="readonly",
            width=30
        )
        self.combo_bang_preview.pack(side='left', padx=(0, 10))
        
        tk.Button(
            frame_chon,
            text="👁 Xem Dữ Liệu",
            command=self.xem_du_lieu_bang,
            font=("Arial", 10)
        ).pack(side='left')
        
        # Treeview hiển thị dữ liệu
        tree_frame = tk.Frame(frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Treeview (sẽ tạo cột động)
        self.tree_preview = ttk.Treeview(tree_frame, show='headings', height=20)
        
        # Scrollbar dọc và ngang
        scrollbar_y = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree_preview.yview)
        scrollbar_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree_preview.xview)
        
        self.tree_preview.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )
        
        self.tree_preview.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
        
        # Label thống kê
        self.label_thong_ke_preview = tk.Label(
            frame,
            text="Chưa load dữ liệu",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        self.label_thong_ke_preview.pack(pady=(5, 0))
    
    # ============================================
    # PHẦN 9: CÁC PHẦN GD DIỆN (GIỐNG BÀI 4)
    # ============================================
    
    def tao_phan_chon_database(self, parent):
        """Tạo phần chọn database (hỗ trợ chọn nhiều với checkbox)"""
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=20, pady=(20, 10))
        
        # Header
        header_frame = tk.Frame(frame)
        header_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(
            header_frame,
            text="📊 Chọn Database (có thể chọn nhiều):",
            font=("Arial", 11, "bold")
        ).pack(side='left')
        
        self.nhan_database_chon = tk.Label(
            header_frame,
            text="Đã chọn: 0 database",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        self.nhan_database_chon.pack(side='right')
        
        # Canvas + Scrollbar cho checkbox list
        frame_canvas_db = tk.Frame(frame)
        frame_canvas_db.pack(fill='x')
        
        self.canvas_database = tk.Canvas(frame_canvas_db, highlightthickness=0, height=100)
        self.canvas_database.pack(side='left', fill='x', expand=True)
        
        scrollbar_db = ttk.Scrollbar(frame_canvas_db, orient="vertical", command=self.canvas_database.yview)
        scrollbar_db.pack(side='right', fill='y')
        
        self.canvas_database.configure(yscrollcommand=scrollbar_db.set)
        
        self.frame_danh_sach_database = tk.Frame(self.canvas_database)
        self.canvas_database.create_window((0, 0), window=self.frame_danh_sach_database, anchor='nw')
        
        self.frame_danh_sach_database.bind("<Configure>", lambda e: self.canvas_database.configure(scrollregion=self.canvas_database.bbox("all")))
        
        # Dictionary để lưu checkbox variables
        self.cac_checkbox_database = {}
        
        # Checkbox "Chọn tất cả database"
        self.chon_tat_ca_database_var = tk.BooleanVar()
        self.checkbox_chon_tat_ca_database = tk.Checkbutton(
            self.frame_danh_sach_database,
            text="☑ CHỌN TẤT CẢ DATABASE",
            variable=self.chon_tat_ca_database_var,
            command=self.xu_ly_chon_tat_ca_database,
            font=("Arial", 10, "bold")
        )
        self.checkbox_chon_tat_ca_database.pack(anchor='w', pady=(5, 10))
    
    def tao_phan_chon_bang(self, parent):
        """Tạo phần chọn bảng"""
        frame = tk.Frame(parent)
        frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Header
        frame_tieu_de = tk.Frame(frame)
        frame_tieu_de.pack(fill='x', pady=(0, 5))
        
        tk.Label(
            frame_tieu_de,
            text="📋 Chọn Bảng:",
            font=("Arial", 11, "bold")
        ).pack(side='left')
        
        self.nhan_thong_ke = tk.Label(
            frame_tieu_de,
            text="Đã chọn: 0/0 bảng",
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        self.nhan_thong_ke.pack(side='right')
        
        # Canvas + Scrollbar
        frame_canvas = tk.Frame(frame)
        frame_canvas.pack(fill='both', expand=True)
        
        self.canvas = tk.Canvas(frame_canvas, highlightthickness=0, height=150)
        self.canvas.pack(side='left', fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(frame_canvas, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side='right', fill='y')
        
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.frame_danh_sach_bang = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_danh_sach_bang, anchor='nw')
        
        self.frame_danh_sach_bang.bind("<Configure>", self.cap_nhat_kich_thuoc_canvas)
        
        # Checkbox "Chọn tất cả"
        self.checkbox_chon_tat_ca = tk.Checkbutton(
            self.frame_danh_sach_bang,
            text="☑ CHỌN TẤT CẢ",
            variable=self.chon_tat_ca_var,
            command=self.xu_ly_chon_tat_ca,
            font=("Arial", 10, "bold")
        )
        self.checkbox_chon_tat_ca.pack(anchor='w', pady=(5, 10))
    
    def tao_phan_ket_qua(self, parent):
        """Tạo phần hiển thị URL"""
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(
            frame,
            text="🔗 URL Kết Nối:",
            font=("Arial", 11, "bold")
        ).pack(anchor='w', pady=(0, 5))
        
        self.text_url = tk.Text(
            frame,
            height=3,
            font=("Courier", 9),
            wrap='word',
            state='disabled'
        )
        self.text_url.pack(fill='x')
    
    def tao_phan_nut_lenh(self, parent):
        """Tạo phần nút lệnh"""
        frame = tk.Frame(parent)
        frame.pack(fill='x', padx=20, pady=(0, 20))
        
        tk.Button(
            frame,
            text="🔧 TẠO URL",
            font=("Arial", 11, "bold"),
            command=self.tao_url_ket_noi,
            cursor="hand2",
            relief='raised',
            bd=2
        ).pack(side='left', padx=(0, 10), ipadx=15, ipady=8)
        
        tk.Button(
            frame,
            text="📋 SAO CHÉP",
            font=("Arial", 11, "bold"),
            command=self.sao_chep_url,
            cursor="hand2",
            relief='raised',
            bd=2
        ).pack(side='left', padx=(0, 10), ipadx=15, ipady=8)
        
        tk.Button(
            frame,
            text="🌐 MỞ TRÌNH DUYỆT",
            font=("Arial", 11, "bold"),
            command=self.mo_trong_trinh_duyet,
            cursor="hand2",
            relief='raised',
            bd=2
        ).pack(side='left', padx=(0, 10), ipadx=15, ipady=8)
        
        tk.Button(
            frame,
            text="💾 XUẤT DS BẢNG",
            font=("Arial", 11, "bold"),
            command=self.xuat_danh_sach_bang,
            cursor="hand2",
            relief='raised',
            bd=2
        ).pack(side='left', ipadx=15, ipady=8)
    
    def tao_thanh_trang_thai(self):
        """Tạo thanh trạng thái (status bar) ở dưới cùng"""
        self.frame_trang_thai = tk.Frame(self.cua_so, relief='sunken', bd=1, height=25)
        self.frame_trang_thai.pack(side='bottom', fill='x')
        
        self.label_trang_thai = tk.Label(
            self.frame_trang_thai,
            text=f"✓ Sẵn sàng | Chế độ: {'Kết nối thật' if CO_PYMSSQL else 'Simulation'}",
            font=("Arial", 9),
            anchor='w'
        )
        self.label_trang_thai.pack(side='left', padx=10)
    
    # ============================================
    # PHẦN 10: XỬ LÝ LOAD DỮ LIỆU
    # ============================================
    
    def tai_cau_hinh(self):
        """Đọc cấu hình database"""
        try:
            self.config = doc_config()
            self.cap_nhat_trang_thai(f"✓ Đã đọc cấu hình: {self.config['server']}")
        except Exception as e:
            self.cap_nhat_trang_thai(f"✗ Lỗi đọc cấu hình: {e}")
            messagebox.showerror("Lỗi", f"Không thể đọc cấu hình:\n{e}")
    
    def tai_danh_sach_database(self):
        """Tải danh sách database và tạo checkbox cho mỗi database"""
        if not self.config:
            return
        
        try:
            danh_sach = lay_ds_database(self.config)
            
            # Xóa các checkbox cũ
            for widget in self.frame_danh_sach_database.winfo_children():
                widget.destroy()
            self.cac_checkbox_database.clear()
            
            # Tạo lại checkbox "Chọn tất cả"
            self.chon_tat_ca_database_var = tk.BooleanVar()
            self.checkbox_chon_tat_ca_database = tk.Checkbutton(
                self.frame_danh_sach_database,
                text="☑ CHỌN TẤT CẢ DATABASE",
                variable=self.chon_tat_ca_database_var,
                command=self.xu_ly_chon_tat_ca_database,
                font=("Arial", 10, "bold")
            )
            self.checkbox_chon_tat_ca_database.pack(anchor='w', pady=(5, 10))
            
            # Tạo checkbox cho mỗi database
            for db in danh_sach:
                var = tk.BooleanVar()
                checkbox = tk.Checkbutton(
                    self.frame_danh_sach_database,
                    text=f"☑ {db}",
                    variable=var,
                    command=self.xu_ly_chon_database,
                    font=("Arial", 10)
                )
                checkbox.pack(anchor='w', pady=2)
                self.cac_checkbox_database[db] = var
            
            # Tự động chọn database đầu tiên
            if danh_sach:
                first_db = danh_sach[0]
                self.cac_checkbox_database[first_db].set(True)
                self.tai_danh_sach_bang_tu_nhieu_database([first_db])
            
            self.cap_nhat_nhan_database()
            self.cap_nhat_trang_thai(f"✓ Đã tải {len(danh_sach)} database")
        except Exception as e:
            self.cap_nhat_trang_thai(f"✗ Lỗi tải database: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải database:\n{e}")
    
    def tai_danh_sach_bang(self, database_name: str):
        """Tải danh sách bảng"""
        # Xóa checkbox cũ
        for widget in self.frame_danh_sach_bang.winfo_children():
            if widget != self.checkbox_chon_tat_ca:
                widget.destroy()
        
        self.cac_checkbox.clear()
        self.chon_tat_ca_var.set(False)
        
        try:
            danh_sach_bang = lay_ds_bang(self.config, database_name)
            
            if not danh_sach_bang:
                tk.Label(
                    self.frame_danh_sach_bang,
                    text="⚠ Không có bảng",
                    font=("Arial", 10)
                ).pack(anchor='w', pady=10)
                self.cap_nhat_thong_ke()
                return
            
            # Cập nhật combo preview
            self.combo_bang_preview['values'] = danh_sach_bang
            if danh_sach_bang:
                self.combo_bang_preview.current(0)
            
            # Tạo checkbox
            for ten_bang in danh_sach_bang:
                var = tk.BooleanVar()
                self.cac_checkbox[ten_bang] = var
                
                checkbox = tk.Checkbutton(
                    self.frame_danh_sach_bang,
                    text=f"  {ten_bang}",
                    variable=var,
                    command=self.cap_nhat_thong_ke,
                    font=("Arial", 10)
                )
                checkbox.pack(anchor='w', pady=2)
            
            self.cap_nhat_thong_ke()
            self.cap_nhat_trang_thai(f"✓ Đã tải {len(danh_sach_bang)} bảng từ '{database_name}'")
            
        except Exception as e:
            self.cap_nhat_trang_thai(f"✗ Lỗi tải bảng: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải bảng:\n{e}")
    
    def tai_danh_sach_bang_tu_nhieu_database(self, danh_sach_database: list):
        """Tải danh sách bảng từ nhiều database"""
        # Xóa checkbox cũ
        for widget in self.frame_danh_sach_bang.winfo_children():
            if widget != self.checkbox_chon_tat_ca:
                widget.destroy()
        
        self.cac_checkbox.clear()
        self.chon_tat_ca_var.set(False)
        
        if not danh_sach_database:
            self.cap_nhat_thong_ke()
            return
        
        try:
            # Load bảng từ từng database
            for db_name in danh_sach_database:
                danh_sach_bang = lay_ds_bang(self.config, db_name)
                
                if danh_sach_bang:
                    # Thêm label phân cách cho mỗi database
                    label_db = tk.Label(
                        self.frame_danh_sach_bang,
                        text=f"━━━ {db_name} ({len(danh_sach_bang)} bảng) ━━━",
                        font=("Arial", 9, "bold"),
                        fg="#2980b9"
                    )
                    label_db.pack(anchor='w', pady=(10, 5))
                    
                    # Thêm checkbox cho từng bảng với format DB.Table
                    for ten_bang in danh_sach_bang:
                        var = tk.BooleanVar(value=False)
                        # Key format: "DatabaseName.TableName"
                        key = f"{db_name}.{ten_bang}"
                        self.cac_checkbox[key] = var
                        
                        checkbox = ttk.Checkbutton(
                            self.frame_danh_sach_bang,
                            text=f"  • {ten_bang}",
                            variable=var,
                            command=self.cap_nhat_thong_ke
                        )
                        checkbox.pack(anchor='w', padx=20)
            
            # Cập nhật combo preview với format DB.Table
            danh_sach_bang_day_du = list(self.cac_checkbox.keys())
            self.combo_bang_preview['values'] = danh_sach_bang_day_du
            if danh_sach_bang_day_du:
                self.combo_bang_preview.current(0)
            
            self.cap_nhat_thong_ke()
            tong_bang = len(self.cac_checkbox)
            self.cap_nhat_trang_thai(f"✓ Đã tải {tong_bang} bảng từ {len(danh_sach_database)} database")
            
        except Exception as e:
            self.cap_nhat_trang_thai(f"✗ Lỗi tải bảng: {e}")
            messagebox.showerror("Lỗi", f"Không thể tải bảng:\n{e}")
    
    def lay_danh_sach_database_duoc_chon(self):
        """Lấy danh sách database được chọn từ checkbox"""
        return [db for db, var in self.cac_checkbox_database.items() if var.get()]
    
    def cap_nhat_nhan_database(self):
        """Cập nhật label số database đã chọn"""
        danh_sach_db = self.lay_danh_sach_database_duoc_chon()
        self.nhan_database_chon.config(text=f"Đã chọn: {len(danh_sach_db)} database")
    
    # ============================================
    # PHẦN 11: XỬ LÝ SỰ KIỆN
    # ============================================
    
    def xu_ly_chon_database(self):
        """Xử lý khi chọn database (hỗ trợ nhiều database với checkbox)"""
        danh_sach_db = self.lay_danh_sach_database_duoc_chon()
        self.cap_nhat_nhan_database()
        self.tai_danh_sach_bang_tu_nhieu_database(danh_sach_db)
        
        # Cập nhật trạng thái "Chọn tất cả database"
        if danh_sach_db and len(danh_sach_db) == len(self.cac_checkbox_database):
            self.chon_tat_ca_database_var.set(True)
        else:
            self.chon_tat_ca_database_var.set(False)
    
    def xu_ly_chon_tat_ca_database(self):
        """Xử lý chọn tất cả database"""
        gia_tri = self.chon_tat_ca_database_var.get()
        for var in self.cac_checkbox_database.values():
            var.set(gia_tri)
        # Trigger update
        self.xu_ly_chon_database()
    
    def xu_ly_chon_tat_ca(self):
        """Xử lý chọn tất cả"""
        gia_tri = self.chon_tat_ca_var.get()
        for var in self.cac_checkbox.values():
            var.set(gia_tri)
        self.cap_nhat_thong_ke()
    
    def cap_nhat_thong_ke(self):
        """Cập nhật số lượng đã chọn"""
        so_luong = sum(1 for var in self.cac_checkbox.values() if var.get())
        tong = len(self.cac_checkbox)
        self.nhan_thong_ke.config(text=f"Đã chọn: {so_luong}/{tong} bảng")
    
    def cap_nhat_kich_thuoc_canvas(self, event=None):
        """Cập nhật vùng cuộn canvas"""
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def cap_nhat_trang_thai(self, message: str):
        """Cập nhật thanh trạng thái"""
        self.label_trang_thai.config(text=message)
        self.cua_so.update_idletasks()
    
    # ============================================
    # PHẦN 12: TẠO URL VÀ CLIPBOARD
    # ============================================
    
    def tao_url_ket_noi(self):
        """Tạo URL kết nối (hỗ trợ nhiều database)"""
        danh_sach_db = self.lay_danh_sach_database_duoc_chon()
        
        if not danh_sach_db:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất 1 database!")
            return
        
        # cac_bang_da_chon có format: ["DB1.Table1", "DB2.Table2", ...]
        cac_bang_da_chon = [ten for ten, var in self.cac_checkbox.items() if var.get()]
        
        if not cac_bang_da_chon:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn ít nhất 1 bảng!")
            return
        
        # Format mới: databases=DB1,DB2&tables=DB1.Table1,DB2.Table2
        params = {
            'databases': ','.join(danh_sach_db),  # Nhiều database
            'tables': ','.join(cac_bang_da_chon)  # Format DB.Table
        }
        
        query_string = urlencode(params)
        base_url = "http://127.0.0.1:5002"
        url_hoan_chinh = f"{base_url}?{query_string}"
        
        self.text_url.config(state='normal')
        self.text_url.delete('1.0', 'end')
        self.text_url.insert('1.0', url_hoan_chinh)
        self.text_url.config(state='disabled')
        
        # Lưu vào lịch sử (dùng database đầu tiên làm đại diện)
        database_dai_dien = danh_sach_db[0] if len(danh_sach_db) == 1 else f"{len(danh_sach_db)} databases"
        self.quan_ly_lich_su.them_muc(database_dai_dien, cac_bang_da_chon, url_hoan_chinh)
        self.cap_nhat_lich_su()
        
        self.cap_nhat_trang_thai(f"✓ Đã tạo URL | Database: {len(danh_sach_db)} | Bảng: {len(cac_bang_da_chon)}")
        messagebox.showinfo("Thành công", f"✓ Đã tạo URL!\n\nDatabase: {len(danh_sach_db)}\nBảng: {len(cac_bang_da_chon)}")
    
    def sao_chep_url(self):
        """Sao chép URL vào clipboard"""
        url = self.text_url.get('1.0', 'end-1c')
        
        if not url or url.strip() == "":
            messagebox.showwarning("Cảnh báo", "Chưa có URL để sao chép!")
            return
        
        try:
            self.cua_so.clipboard_clear()
            self.cua_so.clipboard_append(url)
            self.cua_so.update()
            
            self.cap_nhat_trang_thai("✓ Đã sao chép URL vào clipboard")
            messagebox.showinfo("Thành công", "✓ Đã sao chép URL!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể sao chép:\n{e}")
    
    def mo_trong_trinh_duyet(self):
        """Mở URL trong trình duyệt"""
        url = self.text_url.get('1.0', 'end-1c')
        
        if not url or url.strip() == "":
            messagebox.showwarning("Cảnh báo", "Chưa có URL!")
            return
        
        try:
            webbrowser.open(url)
            self.cap_nhat_trang_thai("✓ Đã mở trình duyệt")
            messagebox.showinfo("Thành công", "✓ Đã mở URL!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể mở trình duyệt:\n{e}")
    
    # ============================================
    # PHẦN 13: LỊCH SỬ
    # ============================================
    
    def cap_nhat_lich_su(self):
        """Cập nhật Treeview lịch sử"""
        # Xóa dữ liệu cũ
        for item in self.tree_lich_su.get_children():
            self.tree_lich_su.delete(item)
        
        # Thêm dữ liệu mới
        for muc in self.quan_ly_lich_su.lich_su:
            self.tree_lich_su.insert(
                '',
                'end',
                values=(
                    muc['timestamp'],
                    muc['database'],
                    ', '.join(muc['tables'][:3]) + ('...' if len(muc['tables']) > 3 else ''),
                    muc['url'][:50] + '...'
                )
            )
    
    def xoa_lich_su(self):
        """Xóa toàn bộ lịch sử"""
        if messagebox.askyesno("Xác nhận", "Xóa toàn bộ lịch sử?"):
            self.quan_ly_lich_su.xoa_tat_ca()
            self.cap_nhat_lich_su()
            messagebox.showinfo("Thành công", "Đã xóa lịch sử!")
    
    def xuat_lich_su(self):
        """Xuất lịch sử ra file JSON"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.quan_ly_lich_su.lich_su, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Thành công", f"Đã xuất lịch sử!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file:\n{e}")
    
    # ============================================
    # PHẦN 14: PREVIEW DỮ LIỆU
    # ============================================
    
    def xem_du_lieu_bang(self):
        """Xem dữ liệu từ bảng đã chọn"""
        ten_bang_day_du = self.combo_bang_preview.get()  # Format: "DB.Table"
        
        if not ten_bang_day_du:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn bảng!")
            return
        
        # Tách database và table name
        if '.' in ten_bang_day_du:
            database, ten_bang = ten_bang_day_du.split('.', 1)
        else:
            messagebox.showwarning("Cảnh báo", "Format bảng không hợp lệ!")
            return
        
        try:
            # Lấy dữ liệu
            du_lieu = lay_du_lieu_bang(self.config, database, ten_bang)
            
            if not du_lieu:
                messagebox.showinfo("Thông báo", "Bảng không có dữ liệu")
                return
            
            # Xóa cột cũ
            self.tree_preview.delete(*self.tree_preview.get_children())
            self.tree_preview['columns'] = ()
            
            # Tạo cột mới
            columns = list(du_lieu[0].keys())
            self.tree_preview['columns'] = columns
            self.tree_preview['show'] = 'headings'
            
            for col in columns:
                self.tree_preview.heading(col, text=col)
                self.tree_preview.column(col, width=120)
            
            # Thêm dữ liệu
            for row in du_lieu:
                values = [row.get(col, '') for col in columns]
                self.tree_preview.insert('', 'end', values=values)
            
            self.label_thong_ke_preview.config(
                text=f"✓ Đã load {len(du_lieu)} dòng | {len(columns)} cột | Bảng: {ten_bang}"
            )
            
            self.cap_nhat_trang_thai(f"✓ Preview: {ten_bang} ({len(du_lieu)} dòng)")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể load dữ liệu:\n{e}")
    
    # ============================================
    # PHẦN 15: THEME (DARK/LIGHT MODE)
    # ============================================
    
    def chuyen_theme(self, theme_name: str):
        """
        Chuyển đổi theme
        
        Tham số:
            theme_name (str): "light" hoặc "dark"
        """
        self.theme_hien_tai = theme_name
        
        if theme_name == "dark":
            self.theme = THEME_DARK.copy()
        else:
            self.theme = THEME_LIGHT.copy()
        
        self.ap_dung_theme()
        self.cap_nhat_trang_thai(f"✓ Đã chuyển sang theme {theme_name}")
    
    def ap_dung_theme(self):
        """Áp dụng theme cho toàn bộ widget"""
        # Cửa sổ chính
        self.cua_so.configure(bg=self.theme['bg'])
        
        # Header
        if hasattr(self, 'frame_header'):
            self.frame_header.configure(bg=self.theme['header_bg'])
            for widget in self.frame_header.winfo_children():
                if isinstance(widget, tk.Label):
                    widget.configure(bg=self.theme['header_bg'], fg=self.theme['header_fg'])
        
        # Các tab
        for tab in [self.tab_ket_noi, self.tab_lich_su, self.tab_preview]:
            tab.configure(bg=self.theme['bg'])
            self.ap_dung_theme_recursive(tab)
    
    def ap_dung_theme_recursive(self, widget):
        """Áp dụng theme đệ quy cho widget và con"""
        try:
            if isinstance(widget, (tk.Frame, tk.Canvas)):
                widget.configure(bg=self.theme['bg'])
            elif isinstance(widget, tk.Label):
                widget.configure(bg=self.theme['bg'], fg=self.theme['fg'])
            elif isinstance(widget, tk.Button):
                widget.configure(bg=self.theme['button_bg'], fg=self.theme['button_fg'])
            elif isinstance(widget, tk.Text):
                widget.configure(bg=self.theme['entry_bg'], fg=self.theme['fg'])
            
            # Đệ quy cho widget con
            for child in widget.winfo_children():
                self.ap_dung_theme_recursive(child)
        except:
            pass
    
    # ============================================
    # PHẦN 16: DIALOG CẤU HÌNH
    # ============================================
    
    def mo_dialog_cau_hinh(self):
        """Mở dialog cấu hình database"""
        dialog = tk.Toplevel(self.cua_so)
        dialog.title("⚙ Cấu Hình Database")
        dialog.geometry("450x350")
        dialog.transient(self.cua_so)
        dialog.grab_set()
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        # Các trường nhập liệu
        fields = [
            ("Server:", "server"),
            ("Port:", "port"),
            ("User:", "user"),
            ("Password:", "password"),
            ("Database:", "database")
        ]
        
        entries = {}
        
        for i, (label_text, key) in enumerate(fields):
            tk.Label(frame, text=label_text, font=("Arial", 10)).grid(row=i, column=0, sticky='w', pady=5)
            
            entry = tk.Entry(frame, font=("Arial", 10), width=30)
            entry.grid(row=i, column=1, pady=5)
            
            # Load giá trị hiện tại
            if self.config and key in self.config:
                entry.insert(0, str(self.config[key]))
            
            # Ẩn password
            if key == "password":
                entry.config(show="*")
            
            entries[key] = entry
        
        # Nút lưu
        def luu_cau_hinh():
            new_config = {
                key: entry.get() 
                for key, entry in entries.items()
            }
            
            # Chuyển port sang int
            try:
                new_config['port'] = int(new_config['port'])
            except:
                messagebox.showerror("Lỗi", "Port phải là số!")
                return
            
            # Lưu vào file
            config_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'config',
                'database_config.json'
            )
            
            try:
                with open(config_path, 'w', encoding='utf-8') as f:
                    json.dump(new_config, f, indent=2)
                
                self.config = new_config
                messagebox.showinfo("Thành công", "Đã lưu cấu hình!")
                dialog.destroy()
                self.tai_danh_sach_database()
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu:\n{e}")
        
        tk.Button(
            frame,
            text="💾 Lưu",
            command=luu_cau_hinh,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2"
        ).grid(row=len(fields), column=0, columnspan=2, pady=(20, 0), ipadx=20, ipady=5)
    
    def mo_file_config(self):
        """Mở file config bằng notepad"""
        config_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'config',
            'database_config.json'
        )
        
        if os.path.exists(config_path):
            os.startfile(config_path)
        else:
            messagebox.showerror("Lỗi", "File config không tồn tại!")
    
    # ============================================
    # PHẦN 17: XUẤT DANH SÁCH BẢNG
    # ============================================
    
    def xuat_danh_sach_bang(self):
        """Xuất danh sách bảng đã chọn ra file"""
        cac_bang_da_chon = [ten for ten, var in self.cac_checkbox.items() if var.get()]
        
        if not cac_bang_da_chon:
            messagebox.showwarning("Cảnh báo", "Chưa chọn bảng nào!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == '.json':
                    # Xuất JSON
                    data = {
                        "database": self.database_duoc_chon.get(),
                        "tables": cac_bang_da_chon,
                        "count": len(cac_bang_da_chon),
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                
                elif ext == '.csv':
                    # Xuất CSV
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("Table Name\n")
                        for bang in cac_bang_da_chon:
                            f.write(f"{bang}\n")
                
                else:
                    # Xuất TXT
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"Database: {self.database_duoc_chon.get()}\n")
                        f.write(f"Số lượng bảng: {len(cac_bang_da_chon)}\n")
                        f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("\n=== DANH SÁCH BẢNG ===\n\n")
                        for i, bang in enumerate(cac_bang_da_chon, 1):
                            f.write(f"{i}. {bang}\n")
                
                messagebox.showinfo("Thành công", f"Đã xuất {len(cac_bang_da_chon)} bảng!\n{file_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file:\n{e}")
    
    # ============================================
    # PHẦN 18: MENU HELP
    # ============================================
    
    def hien_thi_huong_dan(self):
        """Hiển thị hướng dẫn sử dụng"""
        messagebox.showinfo(
            "Hướng Dẫn",
            "📖 HƯỚNG DẪN SỬ DỤNG\n\n"
            "1. Chọn Database từ dropdown\n"
            "2. Chọn các bảng cần kết nối\n"
            "3. Nhấn 'Tạo URL' để tạo URL kết nối\n"
            "4. Nhấn 'Sao Chép' để copy URL\n"
            "5. Mở Tableau và dán URL vào Web Data Connector\n\n"
            "💡 Mẹo:\n"
            "- Dùng tab 'Preview' để xem dữ liệu\n"
            "- Dùng tab 'Lịch Sử' để xem kết nối cũ\n"
            "- Chuyển theme: View → Chế độ Tối/Sáng"
        )
    
    def hien_thi_gioi_thieu(self):
        """Hiển thị thông tin giới thiệu"""
        messagebox.showinfo(
            "Giới Thiệu",
            "🔗 TABLEAU DATABASE CONNECTOR\n"
            "Pro Edition v1.0\n\n"
            "Ứng dụng kết nối Tableau với SQL Server\n"
            "Được xây dựng với Python + Tkinter\n\n"
            "✨ Tính năng:\n"
            "- Kết nối nhiều database\n"
            "- Chọn nhiều bảng cùng lúc\n"
            "- Lịch sử kết nối\n"
            "- Preview dữ liệu\n"
            "- Dark/Light mode\n"
            "- Xuất danh sách bảng\n\n"
            "📚 Dự án học tập - Bài 5"
        )
    
    # ============================================
    # PHẦN 19: CHẠY ỨNG DỤNG
    # ============================================
    
    def chay(self):
        """Chạy ứng dụng"""
        print("\n" + "=" * 60)
        print("🚀 TABLEAU DATABASE CONNECTOR - PRO EDITION")
        print("=" * 60)
        print(f"Chế độ: {'Kết nối thật' if CO_PYMSSQL else 'Simulation'}")
        print(f"Theme: {self.theme_hien_tai}")
        print(f"Lịch sử: {len(self.quan_ly_lich_su.lich_su)} mục")
        print("=" * 60 + "\n")
        
        self.cua_so.mainloop()

# ============================================
# PHẦN 20: ĐIỂM KHỞI CHẠY
# ============================================

if __name__ == "__main__":
    """
    Khởi chạy ứng dụng
    
    Cách chạy:
        python Window_application/bai_5_hoan_chinh.py
    """
    app = UngDungHoanChinh()
    app.chay()
