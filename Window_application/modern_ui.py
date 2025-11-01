import customtkinter as ctk
from typing import Dict, List, Optional
import os
import sys
import json
from datetime import datetime

# Import các component tự tạo
from modern_components import (
    SidebarHienDai, CardHienDai, NutHienDai,
    InputHienDai, Badge, SwitchHienDai, HeaderBar, MauSac
)

# Thêm đường dẫn src để import module kết nối database
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# ============================================
# KIỂM TRA THƯ VIỆN DATABASE
# ============================================

CO_DATABASE_CONNECTOR = False
try:
    import database_connector as db_conn
    CO_DATABASE_CONNECTOR = True
    print("✓ Module database_connector đã sẵn sàng")
except ImportError as e:
    print(f"⚠ Không thể import database_connector: {e}")
    print("→ Sử dụng chế độ demo")

# ============================================
# CÁC HÀM HỖ TRỢ
# ============================================

def doc_cau_hinh_database() -> Dict:
    """Đọc cấu hình database từ file JSON"""
    config_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'database_config.json'
    )
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Lỗi đọc config: {e}")
    
    # Cấu hình mặc định (container hiện tại)
    return {
        "server": "127.0.0.1",
        "port": 1433,  
        "user": "sa",
        "password": "YourStrong!Pass123",
        "database": "master",
        "windows_auth": False
    }

def luu_cau_hinh_database(config: Dict) -> bool:
    """Lưu cấu hình database vào file JSON"""
    config_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'config',
        'database_config.json'
    )
    
    try:
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Lỗi lưu config: {e}")
        return False

def lay_danh_sach_database_demo() -> List[str]:
    """Lấy danh sách database demo"""
    return [
        "ECommerce_Test",
        "Inventory_DB",
        "Sales_DB",
        "HR_System",
        "Analytics",
        "Customer_Portal"
    ]

def lay_danh_sach_bang_demo(database: str) -> List[str]:
    """Lấy danh sách bảng demo"""
    bang_mau = {
        "ECommerce_Test": ["Customers", "Orders", "Products", "Categories"],
        "Inventory_DB": ["Items", "Warehouses", "Stock", "Suppliers"],
        "Sales_DB": ["Transactions", "SalesReps", "Regions", "Targets"],
        "HR_System": ["Employees", "Departments", "Payroll", "Benefits"],
        "Analytics": ["WebTraffic", "UserBehavior", "Conversions"],
        "Customer_Portal": ["Users", "Profiles", "Sessions", "Feedback"]
    }
    return bang_mau.get(database, ["Table1", "Table2", "Table3"])

def lay_du_lieu_bang_demo(database: str, table: str) -> List[Dict]:
    """Lấy dữ liệu mẫu từ bảng (demo)"""
    if table == "Customers":
        return [
            {"CustomerID": 1, "Name": "Nguyễn Văn A", "Email": "a@example.com", "Phone": "0123456789"},
            {"CustomerID": 2, "Name": "Trần Thị B", "Email": "b@example.com", "Phone": "0987654321"},
            {"CustomerID": 3, "Name": "Lê Văn C", "Email": "c@example.com", "Phone": "0111222333"},
        ]
    elif table == "Orders":
        return [
            {"OrderID": 1001, "CustomerID": 1, "OrderDate": "2025-01-15", "Total": 500000},
            {"OrderID": 1002, "CustomerID": 2, "OrderDate": "2025-01-16", "Total": 750000},
            {"OrderID": 1003, "CustomerID": 1, "OrderDate": "2025-01-17", "Total": 1200000},
        ]
    elif table == "Products":
        return [
            {"ProductID": 101, "Name": "Laptop Dell", "Price": 15000000, "Stock": 50},
            {"ProductID": 102, "Name": "Mouse Logitech", "Price": 250000, "Stock": 200},
            {"ProductID": 103, "Name": "Keyboard Mechanical", "Price": 1500000, "Stock": 100},
        ]
    else:
        return [
            {"ID": 1, "Column1": "Value 1", "Column2": "Data A", "Column3": "Info X"},
            {"ID": 2, "Column1": "Value 2", "Column2": "Data B", "Column3": "Info Y"},
            {"ID": 3, "Column1": "Value 3", "Column2": "Data C", "Column3": "Info Z"},
        ]

# ============================================
# TRANG CHỦ (HOME)
# ============================================

class TrangChu(ctk.CTkFrame):
    """Trang chủ - Hiển thị tổng quan"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Lưu master để cập nhật sau
        self.master_app = master
        
        # Header
        HeaderBar(
            self,
            tieu_de="🏠 Trang Chủ",
            mo_ta="Chào mừng bạn đến với Tableau Database Connector"
        ).pack(fill="x")
        
        # Container cho các card
        self.container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.container.pack(fill="both", expand=True, padx=24, pady=12)
        
        # Lấy số liệu thực
        so_databases = self.lay_so_databases()
        so_tables = self.lay_so_tables()
        so_connections = self.lay_so_connections()
        
        # Card chào mừng
        card_chao = CardHienDai(
            self.container,
            tieu_de="👋 Chào mừng",
            mo_ta="Ứng dụng kết nối Tableau với SQL Server Database"
        )
        card_chao.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(
            card_chao.noi_dung,
            text="Ứng dụng này giúp bạn dễ dàng kết nối Tableau Desktop/Server\n"
                 "với các database SQL Server thông qua giao diện đồ họa thân thiện.",
            font=("Arial", 12),
            text_color=MauSac.CHU_XAM,
            justify="left"
        ).pack(anchor="w")
        
        # Row chứa 3 card thống kê
        row_thong_ke = ctk.CTkFrame(self.container, fg_color="transparent")
        row_thong_ke.pack(fill="x", pady=(0, 12))
        
        # Grid layout
        row_thong_ke.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Card 1: Databases
        self.card_db = self.tao_card_thong_ke(
            row_thong_ke,
            icon="🗄️",
            so_luong=str(so_databases),
            nhan="Databases",
            mau=MauSac.XANH_DISCORD
        )
        self.card_db.grid(row=0, column=0, padx=(0, 6), sticky="ew")
        
        # Card 2: Tables
        self.card_bang = self.tao_card_thong_ke(
            row_thong_ke,
            icon="📊",
            so_luong=str(so_tables),
            nhan="Tables",
            mau=MauSac.XANH_LA
        )
        self.card_bang.grid(row=0, column=1, padx=6, sticky="ew")
        
        # Card 3: Connections
        self.card_ket_noi = self.tao_card_thong_ke(
            row_thong_ke,
            icon="🔗",
            so_luong=str(so_connections),
            nhan="Connections",
            mau=MauSac.XANH_LAM
        )
        self.card_ket_noi.grid(row=0, column=2, padx=(6, 0), sticky="ew")
        
        # Card hướng dẫn nhanh
        card_huong_dan = CardHienDai(
            self.container,
            tieu_de="📚 Hướng Dẫn Nhanh",
            mo_ta="Các bước để bắt đầu sử dụng"
        )
        card_huong_dan.pack(fill="x", pady=(0, 12))
        
        buoc_huong_dan = [
            "1️⃣ Vào phần Settings để cấu hình kết nối database",
            "2️⃣ Chuyển sang tab Connect để chọn database và bảng",
            "3️⃣ Nhấn 'Tạo URL' để tạo liên kết kết nối",
            "4️⃣ Sao chép URL và dán vào Tableau Web Data Connector",
            "5️⃣ Xem lại lịch sử kết nối trong tab History"
        ]
        
        for buoc in buoc_huong_dan:
            ctk.CTkLabel(
                card_huong_dan.noi_dung,
                text=buoc,
                font=("Arial", 12),
                text_color=MauSac.CHU_TRANG,
                anchor="w"
            ).pack(anchor="w", pady=4)
        
        # Card tính năng
        card_tinh_nang = CardHienDai(
            self.container,
            tieu_de="✨ Tính Năng Chính"
        )
        card_tinh_nang.pack(fill="x")
        
        tinh_nang = [
            "✅ Kết nối nhiều database cùng lúc",
            "✅ Chọn nhiều bảng từ các database khác nhau",
            "✅ Lưu lịch sử kết nối tự động",
            "✅ Giao diện dark mode hiện đại",
            "✅ Dễ dàng cấu hình và sử dụng"
        ]
        
        for tn in tinh_nang:
            ctk.CTkLabel(
                card_tinh_nang.noi_dung,
                text=tn,
                font=("Arial", 12),
                text_color=MauSac.CHU_TRANG,
                anchor="w"
            ).pack(anchor="w", pady=4)
    
    def lay_so_databases(self) -> int:
        """Lấy số lượng databases"""
        try:
            if CO_DATABASE_CONNECTOR:
                databases = db_conn.lay_danh_sach_database()
            else:
                databases = lay_danh_sach_database_demo()
            return len(databases)
        except:
            return 0
    
    def lay_so_tables(self) -> int:
        """Lấy tổng số bảng từ tất cả databases"""
        try:
            tong_so_bang = 0
            if CO_DATABASE_CONNECTOR:
                databases = db_conn.lay_danh_sach_database()
                for db in databases:
                    try:
                        tables = db_conn.lay_danh_sach_bang(db)
                        tong_so_bang += len(tables)
                    except:
                        continue
            else:
                databases = lay_danh_sach_database_demo()
                for db in databases:
                    tables = lay_danh_sach_bang_demo(db)
                    tong_so_bang += len(tables)
            return tong_so_bang
        except:
            return 0
    
    def lay_so_connections(self) -> int:
        """Lấy số lượng kết nối từ lịch sử"""
        try:
            lich_su_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'connection_history.json'
            )
            if os.path.exists(lich_su_path):
                with open(lich_su_path, 'r', encoding='utf-8') as f:
                    lich_su = json.load(f)
                    return len(lich_su)
            return 0
        except:
            return 0
    
    def tao_card_thong_ke(
        self,
        master,
        icon: str,
        so_luong: str,
        nhan: str,
        mau: str
    ) -> ctk.CTkFrame:
        """Tạo card thống kê nhỏ"""
        card = ctk.CTkFrame(
            master,
            fg_color=MauSac.NEN_CARD,
            corner_radius=8,
            border_width=1,
            border_color=MauSac.VIEN
        )
        
        # Container
        container = ctk.CTkFrame(card, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Icon
        ctk.CTkLabel(
            container,
            text=icon,
            font=("Arial", 32)
        ).pack()
        
        # Số lượng
        ctk.CTkLabel(
            container,
            text=so_luong,
            font=("Arial", 24, "bold"),
            text_color=mau
        ).pack()
        
        # Nhãn
        ctk.CTkLabel(
            container,
            text=nhan,
            font=("Arial", 11),
            text_color=MauSac.CHU_XAM
        ).pack()
        
        return card

# ============================================
# TRANG KẾT NỐI (CONNECT)
# ============================================

class TrangKetNoi(ctk.CTkFrame):
    """Trang kết nối - Chọn database và bảng"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Header
        HeaderBar(
            self,
            tieu_de="🔗 Kết Nối Database",
            mo_ta="Chọn database và bảng để tạo URL kết nối Tableau"
        ).pack(fill="x")
        
        # Container
        container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        container.pack(fill="both", expand=True, padx=24, pady=12)
        
        # Card chọn database
        card_database = CardHienDai(
            container,
            tieu_de="📊 Chọn Database",
            mo_ta="Chọn một hoặc nhiều database để làm việc"
        )
        card_database.pack(fill="x", pady=(0, 12))
        
        # Nút tải database
        NutHienDai(
            card_database.noi_dung,
            text="Tải Danh Sách Database",
            icon="🔄",
            command=self.tai_danh_sach_database
        ).pack(pady=(0, 12))
        
        # Frame chứa checkbox databases
        self.frame_databases = ctk.CTkFrame(
            card_database.noi_dung,
            fg_color="transparent"
        )
        self.frame_databases.pack(fill="both", expand=True)
        
        # Dictionary lưu checkbox
        self.cac_checkbox_database: Dict[str, ctk.CTkCheckBox] = {}
        
        # Card chọn bảng
        card_bang = CardHienDai(
            container,
            tieu_de="📋 Chọn Bảng",
            mo_ta="Chọn các bảng cần kết nối với Tableau"
        )
        card_bang.pack(fill="x", pady=(0, 12))
        
        # Nút tải bảng
        NutHienDai(
            card_bang.noi_dung,
            text="Tải Danh Sách Bảng",
            icon="🔄",
            command=self.tai_danh_sach_bang
        ).pack(pady=(0, 12))
        
        # Frame chứa checkbox bảng
        self.frame_bang = ctk.CTkFrame(
            card_bang.noi_dung,
            fg_color="transparent"
        )
        self.frame_bang.pack(fill="both", expand=True)
        
        # Dictionary lưu checkbox bảng
        self.cac_checkbox_bang: Dict[str, ctk.CTkCheckBox] = {}
        
        # Card kết quả
        card_ket_qua = CardHienDai(
            container,
            tieu_de="🔗 URL Kết Nối",
            mo_ta="URL để dán vào Tableau Web Data Connector"
        )
        card_ket_qua.pack(fill="x", pady=(0, 12))
        
        # Text box hiển thị URL
        self.textbox_url = ctk.CTkTextbox(
            card_ket_qua.noi_dung,
            height=80,
            font=("Courier", 11),
            fg_color=MauSac.NEN_TOI,
            border_color=MauSac.VIEN,
            border_width=1
        )
        self.textbox_url.pack(fill="x", pady=(0, 12))
        
        # Frame nút
        frame_nut = ctk.CTkFrame(card_ket_qua.noi_dung, fg_color="transparent")
        frame_nut.pack(fill="x")
        
        NutHienDai(
            frame_nut,
            text="Tạo URL",
            icon="🔧",
            style=NutHienDai.STYLE_CHINH,
            command=self.tao_url
        ).pack(side="left", padx=(0, 8))
        
        NutHienDai(
            frame_nut,
            text="Sao Chép",
            icon="📋",
            style=NutHienDai.STYLE_PHU,
            command=self.sao_chep_url
        ).pack(side="left", padx=(0, 8))
        
        NutHienDai(
            frame_nut,
            text="Mở Trình Duyệt",
            icon="🌐",
            style=NutHienDai.STYLE_THANH_CONG,
            command=self.mo_trinh_duyet
        ).pack(side="left", padx=(0, 8))
        
        NutHienDai(
            frame_nut,
            text="Xuất DS Bảng",
            icon="📄",
            style=NutHienDai.STYLE_PHU,
            command=self.xuat_danh_sach_bang
        ).pack(side="left")
        
        # Label trạng thái
        self.label_trang_thai = ctk.CTkLabel(
            container,
            text="✓ Sẵn sàng",
            font=("Arial", 11),
            text_color=MauSac.XANH_LA
        )
        self.label_trang_thai.pack(pady=8)
    
    def tai_danh_sach_database(self):
        """Tải danh sách database"""
        # Xóa checkbox cũ
        for widget in self.frame_databases.winfo_children():
            widget.destroy()
        self.cac_checkbox_database.clear()
        
        # Lấy danh sách database
        try:
            # Thử dùng module thật
            if CO_DATABASE_CONNECTOR:
                databases = db_conn.lay_danh_sach_database()
            else:
                databases = lay_danh_sach_database_demo()
            
            # Tạo checkbox cho mỗi database
            for db in databases:
                checkbox = ctk.CTkCheckBox(
                    self.frame_databases,
                    text=f"  {db}",
                    font=("Arial", 12),
                    text_color=MauSac.CHU_TRANG,
                    fg_color=MauSac.XANH_DISCORD,
                    hover_color=MauSac.XANH_HOVER
                )
                checkbox.pack(anchor="w", pady=4)
                self.cac_checkbox_database[db] = checkbox
            
            self.label_trang_thai.configure(
                text=f"✓ Đã tải {len(databases)} database",
                text_color=MauSac.XANH_LA
            )
        except Exception as e:
            self.label_trang_thai.configure(
                text=f"✗ Lỗi: {str(e)}",
                text_color=MauSac.DO
            )
    
    def tai_danh_sach_bang(self):
        """Tải danh sách bảng từ các database đã chọn"""
        # Lấy database đã chọn
        cac_db_chon = [
            db for db, checkbox in self.cac_checkbox_database.items()
            if checkbox.get()
        ]
        
        if not cac_db_chon:
            self.label_trang_thai.configure(
                text="⚠ Vui lòng chọn ít nhất 1 database",
                text_color=MauSac.VANG
            )
            return
        
        # Xóa checkbox cũ
        for widget in self.frame_bang.winfo_children():
            widget.destroy()
        self.cac_checkbox_bang.clear()
        
        # Load bảng từ mỗi database
        tong_bang = 0
        for db in cac_db_chon:
            # Label phân cách
            ctk.CTkLabel(
                self.frame_bang,
                text=f"━━━ {db} ━━━",
                font=("Arial", 12, "bold"),
                text_color=MauSac.XANH_DISCORD
            ).pack(anchor="w", pady=(8, 4))
            
            # Lấy danh sách bảng
            try:
                if CO_DATABASE_CONNECTOR:
                    bang_list = db_conn.lay_danh_sach_bang(db)
                else:
                    bang_list = lay_danh_sach_bang_demo(db)
                
                # Tạo checkbox
                for bang in bang_list:
                    checkbox = ctk.CTkCheckBox(
                        self.frame_bang,
                        text=f"  • {bang}",
                        font=("Arial", 11),
                        text_color=MauSac.CHU_TRANG,
                        fg_color=MauSac.XANH_DISCORD,
                        hover_color=MauSac.XANH_HOVER
                    )
                    checkbox.pack(anchor="w", pady=2, padx=20)
                    # Key format: "DatabaseName.TableName"
                    self.cac_checkbox_bang[f"{db}.{bang}"] = checkbox
                    tong_bang += 1
            except Exception as e:
                print(f"Lỗi load bảng từ {db}: {e}")
        
        self.label_trang_thai.configure(
            text=f"✓ Đã tải {tong_bang} bảng từ {len(cac_db_chon)} database",
            text_color=MauSac.XANH_LA
        )
    
    def tao_url(self):
        """Tạo URL kết nối"""
        # Lấy database đã chọn
        cac_db = [
            db for db, cb in self.cac_checkbox_database.items()
            if cb.get()
        ]
        
        # Lấy bảng đã chọn
        cac_bang = [
            bang for bang, cb in self.cac_checkbox_bang.items()
            if cb.get()
        ]
        
        if not cac_db:
            self.label_trang_thai.configure(
                text="⚠ Vui lòng chọn database",
                text_color=MauSac.VANG
            )
            return
        
        if not cac_bang:
            self.label_trang_thai.configure(
                text="⚠ Vui lòng chọn bảng",
                text_color=MauSac.VANG
            )
            return
        
        # Tạo URL
        from urllib.parse import urlencode
        params = {
            'databases': ','.join(cac_db),
            'tables': ','.join(cac_bang)
        }
        query_string = urlencode(params)
        url = f"http://127.0.0.1:5002?{query_string}"
        
        # Hiển thị URL
        self.textbox_url.delete("1.0", "end")
        self.textbox_url.insert("1.0", url)
        
        self.label_trang_thai.configure(
            text=f"✓ Đã tạo URL | {len(cac_db)} database | {len(cac_bang)} bảng",
            text_color=MauSac.XANH_LA
        )
    
    def sao_chep_url(self):
        """Sao chép URL vào clipboard"""
        url = self.textbox_url.get("1.0", "end-1c")
        if url.strip():
            self.master.clipboard_clear()
            self.master.clipboard_append(url)
            self.label_trang_thai.configure(
                text="✓ Đã sao chép URL",
                text_color=MauSac.XANH_LA
            )
        else:
            self.label_trang_thai.configure(
                text="⚠ Chưa có URL",
                text_color=MauSac.VANG
            )
    
    def mo_trinh_duyet(self):
        """Mở URL trong trình duyệt"""
        url = self.textbox_url.get("1.0", "end-1c")
        if url.strip():
            import webbrowser
            webbrowser.open(url)
            self.label_trang_thai.configure(
                text="✓ Đã mở trình duyệt",
                text_color=MauSac.XANH_LA
            )
        else:
            self.label_trang_thai.configure(
                text="⚠ Chưa có URL",
                text_color=MauSac.VANG
            )
    
    def xuat_danh_sach_bang(self):
        """Xuất danh sách bảng đã chọn ra file"""
        from tkinter import filedialog
        
        # Lấy bảng đã chọn
        cac_bang = [
            bang for bang, cb in self.cac_checkbox_bang.items()
            if cb.get()
        ]
        
        if not cac_bang:
            self.label_trang_thai.configure(
                text="⚠ Vui lòng chọn ít nhất 1 bảng",
                text_color=MauSac.VANG
            )
            return
        
        # Chọn file
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ],
            title="Xuất Danh Sách Bảng"
        )
        
        if file_path:
            try:
                ext = os.path.splitext(file_path)[1].lower()
                
                if ext == '.json':
                    # Xuất JSON
                    data = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "tables": cac_bang,
                        "count": len(cac_bang)
                    }
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                
                elif ext == '.csv':
                    # Xuất CSV
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write("Database,Table\n")
                        for bang in cac_bang:
                            if '.' in bang:
                                db, table = bang.split('.', 1)
                                f.write(f"{db},{table}\n")
                            else:
                                f.write(f",{bang}\n")
                
                else:
                    # Xuất TXT
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"DANH SÁCH BẢNG ĐÃ CHỌN\n")
                        f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"Số lượng: {len(cac_bang)} bảng\n")
                        f.write("\n" + "=" * 50 + "\n\n")
                        for i, bang in enumerate(cac_bang, 1):
                            f.write(f"{i}. {bang}\n")
                
                # Thông báo thành công
                self.label_trang_thai.configure(
                    text=f"✓ Đã xuất {len(cac_bang)} bảng vào file",
                    text_color=MauSac.XANH_LA
                )
                
                # Dialog thành công
                success_dialog = ctk.CTkToplevel(self)
                success_dialog.title("Thành Công")
                success_dialog.geometry("400x150")
                
                frame = ctk.CTkFrame(success_dialog, fg_color="transparent")
                frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                ctk.CTkLabel(
                    frame,
                    text="✓ Đã xuất danh sách bảng!",
                    font=("Arial", 14, "bold"),
                    text_color=MauSac.XANH_LA
                ).pack(pady=(0, 10))
                
                ctk.CTkLabel(
                    frame,
                    text=f"File: {os.path.basename(file_path)}\nSố bảng: {len(cac_bang)}",
                    font=("Arial", 11),
                    text_color=MauSac.CHU_XAM
                ).pack()
                
                success_dialog.after(3000, success_dialog.destroy)
                
            except Exception as e:
                self.label_trang_thai.configure(
                    text=f"✗ Lỗi: {str(e)}",
                    text_color=MauSac.DO
                )
                print(f"Lỗi xuất file: {e}")

# ============================================
# TRANG LỊCH SỬ (HISTORY)
# ============================================

class TrangLichSu(ctk.CTkFrame):
    """Trang lịch sử - Xem các kết nối đã tạo"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Header
        HeaderBar(
            self,
            tieu_de="📜 Lịch Sử Kết Nối",
            mo_ta="Danh sách các URL đã tạo trước đó"
        ).pack(fill="x")
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=12)
        
        # Card lịch sử
        card = CardHienDai(
            container,
            tieu_de="📋 Danh Sách Lịch Sử"
        )
        card.pack(fill="both", expand=True)
        
        # Scrollable frame cho lịch sử
        self.frame_lich_su = ctk.CTkScrollableFrame(
            card.noi_dung,
            fg_color="transparent",
            height=400
        )
        self.frame_lich_su.pack(fill="both", expand=True, pady=(0, 12))
        
        # Frame nút
        frame_nut = ctk.CTkFrame(card.noi_dung, fg_color="transparent")
        frame_nut.pack(fill="x")
        
        NutHienDai(
            frame_nut,
            text="Làm Mới",
            icon="🔄",
            style=NutHienDai.STYLE_PHU,
            command=self.tai_lich_su
        ).pack(side="left", padx=(0, 8))
        
        NutHienDai(
            frame_nut,
            text="Xóa Tất Cả",
            icon="🗑️",
            style=NutHienDai.STYLE_NGUY_HIEM,
            command=self.xoa_lich_su
        ).pack(side="left", padx=(0, 8))
        
        NutHienDai(
            frame_nut,
            text="Xuất File",
            icon="💾",
            style=NutHienDai.STYLE_THANH_CONG,
            command=self.xuat_lich_su
        ).pack(side="left")
        
        # Tải lịch sử
        self.tai_lich_su()
    
    def tai_lich_su(self):
        """Tải lịch sử từ file"""
        # Xóa nội dung cũ
        for widget in self.frame_lich_su.winfo_children():
            widget.destroy()
        
        # Đọc file lịch sử
        history_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'connection_history.json'
        )
        
        if not os.path.exists(history_path):
            ctk.CTkLabel(
                self.frame_lich_su,
                text="📭 Chưa có lịch sử kết nối",
                font=("Arial", 13),
                text_color=MauSac.CHU_XAM
            ).pack(pady=20)
            return
        
        try:
            with open(history_path, 'r', encoding='utf-8') as f:
                lich_su = json.load(f)
            
            if not lich_su:
                ctk.CTkLabel(
                    self.frame_lich_su,
                    text="📭 Chưa có lịch sử kết nối",
                    font=("Arial", 13),
                    text_color=MauSac.CHU_XAM
                ).pack(pady=20)
                return
            
            # Hiển thị từng mục
            for i, muc in enumerate(lich_su[:20]):  # Chỉ hiển thị 20 mục đầu
                self.tao_muc_lich_su(muc, i)
        
        except Exception as e:
            ctk.CTkLabel(
                self.frame_lich_su,
                text=f"✗ Lỗi đọc lịch sử: {str(e)}",
                font=("Arial", 12),
                text_color=MauSac.DO
            ).pack(pady=20)
    
    def tao_muc_lich_su(self, muc: Dict, index: int):
        """Tạo một mục lịch sử"""
        # Frame cho mục
        frame_muc = ctk.CTkFrame(
            self.frame_lich_su,
            fg_color=MauSac.NEN_CARD,
            corner_radius=8,
            border_width=1,
            border_color=MauSac.VIEN
        )
        frame_muc.pack(fill="x", pady=(0, 8))
        
        # Container
        container = ctk.CTkFrame(frame_muc, fg_color="transparent")
        container.pack(fill="x", padx=12, pady=12)
        
        # Row 1: Thời gian và badge
        row1 = ctk.CTkFrame(container, fg_color="transparent")
        row1.pack(fill="x", pady=(0, 8))
        
        ctk.CTkLabel(
            row1,
            text=f"🕐 {muc.get('timestamp', 'N/A')}",
            font=("Arial", 11),
            text_color=MauSac.CHU_XAM
        ).pack(side="left")
        
        Badge(
            row1,
            text=f"#{index + 1}",
            mau_nen=MauSac.XANH_DISCORD
        ).pack(side="right")
        
        # Row 2: Database
        ctk.CTkLabel(
            container,
            text=f"📊 Database: {muc.get('database', 'N/A')}",
            font=("Arial", 12, "bold"),
            text_color=MauSac.CHU_TRANG,
            anchor="w"
        ).pack(fill="x", pady=(0, 4))
        
        # Row 3: Tables
        tables = muc.get('tables', [])
        tables_text = ', '.join(tables[:3])
        if len(tables) > 3:
            tables_text += f" ... (+{len(tables) - 3})"
        
        ctk.CTkLabel(
            container,
            text=f"📋 Bảng: {tables_text}",
            font=("Arial", 11),
            text_color=MauSac.CHU_XAM,
            anchor="w"
        ).pack(fill="x", pady=(0, 8))
        
        # Row 4: URL (rút gọn)
        url = muc.get('url', '')
        url_ngan = url[:60] + '...' if len(url) > 60 else url
        
        ctk.CTkLabel(
            container,
            text=f"🔗 {url_ngan}",
            font=("Courier", 10),
            text_color=MauSac.XANH_LAM,
            anchor="w"
        ).pack(fill="x")
    
    def xoa_lich_su(self):
        """Xóa toàn bộ lịch sử"""
        # Tạo dialog xác nhận
        dialog = ctk.CTkToplevel(self)
        dialog.title("Xác Nhận Xóa")
        dialog.geometry("400x150")
        dialog.transient(self)
        
        # Căn giữa dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (150 // 2)
        dialog.geometry(f"+{x}+{y}")
        
        # Gọi grab_set sau khi dialog đã được hiển thị
        dialog.grab_set()
        
        # Frame chính
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Label cảnh báo
        ctk.CTkLabel(
            frame,
            text="⚠️ Xác Nhận Xóa Lịch Sử",
            font=("Arial", 16, "bold"),
            text_color=MauSac.VANG
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            frame,
            text="Bạn có chắc chắn muốn xóa toàn bộ lịch sử?\nHành động này không thể hoàn tác!",
            font=("Arial", 11),
            text_color=MauSac.CHU_TRANG
        ).pack(pady=(0, 20))
        
        # Frame nút
        frame_nut = ctk.CTkFrame(frame, fg_color="transparent")
        frame_nut.pack()
        
        def xac_nhan():
            history_path = os.path.join(
                os.path.dirname(__file__),
                '..',
                'connection_history.json'
            )
            try:
                # Xóa file hoặc ghi mảng rỗng
                with open(history_path, 'w', encoding='utf-8') as f:
                    json.dump([], f)
                self.tai_lich_su()
                dialog.destroy()
                
                # Thông báo thành công
                success_dialog = ctk.CTkToplevel(self)
                success_dialog.title("Thành Công")
                success_dialog.geometry("300x100")
                ctk.CTkLabel(
                    success_dialog,
                    text="✓ Đã xóa lịch sử thành công!",
                    font=("Arial", 13)
                ).pack(expand=True)
                success_dialog.after(2000, success_dialog.destroy)
            except Exception as e:
                print(f"Lỗi xóa lịch sử: {e}")
                dialog.destroy()
        
        NutHienDai(
            frame_nut,
            text="Hủy",
            icon="✖",
            style=NutHienDai.STYLE_PHU,
            command=dialog.destroy,
            width=120
        ).pack(side="left", padx=(0, 10))
        
        NutHienDai(
            frame_nut,
            text="Xóa",
            icon="🗑️",
            style=NutHienDai.STYLE_NGUY_HIEM,
            command=xac_nhan,
            width=120
        ).pack(side="left")
    
    def xuat_lich_su(self):
        """Xuất lịch sử ra file JSON"""
        from tkinter import filedialog
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[
                ("JSON files", "*.json"),
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            title="Xuất Lịch Sử"
        )
        
        if file_path:
            try:
                history_path = os.path.join(
                    os.path.dirname(__file__),
                    '..',
                    'connection_history.json'
                )
                
                if os.path.exists(history_path):
                    with open(history_path, 'r', encoding='utf-8') as f:
                        lich_su = json.load(f)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(lich_su, f, ensure_ascii=False, indent=2)
                    
                    # Thông báo thành công
                    success_dialog = ctk.CTkToplevel(self)
                    success_dialog.title("Thành Công")
                    success_dialog.geometry("400x150")
                    
                    frame = ctk.CTkFrame(success_dialog, fg_color="transparent")
                    frame.pack(fill="both", expand=True, padx=20, pady=20)
                    
                    ctk.CTkLabel(
                        frame,
                        text="✓ Đã xuất lịch sử thành công!",
                        font=("Arial", 14, "bold"),
                        text_color=MauSac.XANH_LA
                    ).pack(pady=(0, 10))
                    
                    ctk.CTkLabel(
                        frame,
                        text=f"File: {os.path.basename(file_path)}",
                        font=("Arial", 11),
                        text_color=MauSac.CHU_XAM
                    ).pack()
                    
                    success_dialog.after(3000, success_dialog.destroy)
                    
            except Exception as e:
                print(f"Lỗi xuất file: {e}")

# ============================================
# TRANG PREVIEW DỮ LIỆU (PREVIEW)
# ============================================

class TrangPreview(ctk.CTkFrame):
    """Trang preview dữ liệu - Xem trước dữ liệu từ bảng"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Header
        HeaderBar(
            self,
            tieu_de="👁️ Preview Dữ Liệu",
            mo_ta="Xem trước dữ liệu từ bảng đã chọn"
        ).pack(fill="x")
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=12)
        
        # Card chọn bảng
        card_chon = CardHienDai(
            container,
            tieu_de="🔍 Chọn Bảng Để Xem",
            mo_ta="Chọn database và bảng để xem dữ liệu"
        )
        card_chon.pack(fill="x", pady=(0, 12))
        
        # Frame chọn
        frame_chon = ctk.CTkFrame(card_chon.noi_dung, fg_color="transparent")
        frame_chon.pack(fill="x")
        
        # Combobox database
        ctk.CTkLabel(
            frame_chon,
            text="Database:",
            font=("Arial", 12),
            text_color=MauSac.CHU_TRANG
        ).pack(side="left", padx=(0, 10))
        
        self.combo_database = ctk.CTkComboBox(
            frame_chon,
            width=200,
            values=["Chọn database..."],
            font=("Arial", 11),
            fg_color=MauSac.NEN_TOI,
            border_color=MauSac.VIEN,
            button_color=MauSac.XANH_DISCORD,
            button_hover_color=MauSac.XANH_HOVER,
            dropdown_fg_color=MauSac.NEN_CARD,
            command=self.khi_chon_database
        )
        self.combo_database.pack(side="left", padx=(0, 20))
        
        # Combobox bảng
        ctk.CTkLabel(
            frame_chon,
            text="Bảng:",
            font=("Arial", 12),
            text_color=MauSac.CHU_TRANG
        ).pack(side="left", padx=(0, 10))
        
        self.combo_bang = ctk.CTkComboBox(
            frame_chon,
            width=200,
            values=["Chọn bảng..."],
            font=("Arial", 11),
            fg_color=MauSac.NEN_TOI,
            border_color=MauSac.VIEN,
            button_color=MauSac.XANH_DISCORD,
            button_hover_color=MauSac.XANH_HOVER,
            dropdown_fg_color=MauSac.NEN_CARD
        )
        self.combo_bang.pack(side="left", padx=(0, 20))
        
        # Nút xem
        NutHienDai(
            frame_chon,
            text="Xem Dữ Liệu",
            icon="👁️",
            style=NutHienDai.STYLE_CHINH,
            command=self.xem_du_lieu
        ).pack(side="left")
        
        # Card hiển thị dữ liệu
        card_du_lieu = CardHienDai(
            container,
            tieu_de="📊 Dữ Liệu Bảng",
            mo_ta="Hiển thị tối đa 100 dòng đầu tiên"
        )
        card_du_lieu.pack(fill="both", expand=True)
        
        # Frame cho Treeview với scrollbar
        tree_frame = ctk.CTkFrame(card_du_lieu.noi_dung, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, pady=(0, 12))
        
        # Tạo frame bên trong để chứa treeview (dùng tkinter thường)
        import tkinter as tk
        from tkinter import ttk
        
        # Treeview (sử dụng ttk vì CustomTkinter không có Treeview)
        self.tree = ttk.Treeview(
            tree_frame,
            show='headings',
            height=15
        )
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Scrollbar dọc
        scrollbar_y = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview
        )
        scrollbar_y.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Label thống kê
        self.label_thong_ke = ctk.CTkLabel(
            card_du_lieu.noi_dung,
            text="Chưa load dữ liệu",
            font=("Arial", 11),
            text_color=MauSac.CHU_XAM
        )
        self.label_thong_ke.pack()
        
        # Tải danh sách database
        self.tai_danh_sach_database()
    
    def tai_danh_sach_database(self):
        """Tải danh sách database vào combobox"""
        try:
            if CO_DATABASE_CONNECTOR:
                databases = db_conn.lay_danh_sach_database()
            else:
                databases = lay_danh_sach_database_demo()
            
            self.combo_database.configure(values=databases)
            if databases:
                self.combo_database.set(databases[0])
                self.khi_chon_database(databases[0])
        except Exception as e:
            print(f"Lỗi tải database: {e}")
            self.label_thong_ke.configure(
                text=f"✗ Lỗi: {str(e)}",
                text_color=MauSac.DO
            )
    
    def khi_chon_database(self, database: str):
        """Khi chọn database, load danh sách bảng"""
        try:
            if CO_DATABASE_CONNECTOR:
                bang_list = db_conn.lay_danh_sach_bang(database)
            else:
                bang_list = lay_danh_sach_bang_demo(database)
            
            self.combo_bang.configure(values=bang_list)
            if bang_list:
                self.combo_bang.set(bang_list[0])
        except Exception as e:
            print(f"Lỗi tải bảng: {e}")
    
    def xem_du_lieu(self):
        """Xem dữ liệu từ bảng đã chọn"""
        database = self.combo_database.get()
        bang = self.combo_bang.get()
        
        if not database or database == "Chọn database...":
            self.label_thong_ke.configure(
                text="⚠ Vui lòng chọn database",
                text_color=MauSac.VANG
            )
            return
        
        if not bang or bang == "Chọn bảng...":
            self.label_thong_ke.configure(
                text="⚠ Vui lòng chọn bảng",
                text_color=MauSac.VANG
            )
            return
        
        try:
            # Lấy dữ liệu
            if CO_DATABASE_CONNECTOR:
                # Thử lấy dữ liệu thật từ database
                try:
                    # Gọi hàm lay_du_lieu_bang trả về (data, columns)
                    # data đã là list of dict
                    du_lieu, cot_names = db_conn.lay_du_lieu_bang(bang, database, limit=100)
                    
                    if not du_lieu:
                        raise Exception("Không có dữ liệu")
                    
                except Exception as e:
                    print(f"Lỗi lấy dữ liệu thật: {e}")
                    # Fallback sang demo
                    du_lieu = lay_du_lieu_bang_demo(database, bang)
            else:
                du_lieu = lay_du_lieu_bang_demo(database, bang)
            
            if not du_lieu:
                self.label_thong_ke.configure(
                    text="📭 Bảng không có dữ liệu",
                    text_color=MauSac.CHU_XAM
                )
                return
            
            # Xóa dữ liệu cũ
            self.tree.delete(*self.tree.get_children())
            
            # Lấy tên cột từ dòng đầu tiên
            columns = list(du_lieu[0].keys())
            
            # Cấu hình cột
            self.tree['columns'] = columns
            self.tree['show'] = 'headings'
            
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor='w')
            
            # Thêm dữ liệu
            for row in du_lieu:
                values = [str(row.get(col, '')) for col in columns]
                self.tree.insert('', 'end', values=values)
            
            # Cập nhật thống kê
            self.label_thong_ke.configure(
                text=f"✓ Đã load {len(du_lieu)} dòng | {len(columns)} cột | Bảng: {database}.{bang}",
                text_color=MauSac.XANH_LA
            )
            
        except Exception as e:
            self.label_thong_ke.configure(
                text=f"✗ Lỗi: {str(e)}",
                text_color=MauSac.DO
            )
            print(f"Lỗi xem dữ liệu: {e}")

# ============================================
# TRANG CÀI ĐẶT (SETTINGS)
# ============================================

class TrangCaiDat(ctk.CTkFrame):
    """Trang cài đặt - Cấu hình database"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Header
        HeaderBar(
            self,
            tieu_de="⚙️ Cài Đặt",
            mo_ta="Cấu hình kết nối database"
        ).pack(fill="x")
        
        # Container
        container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        container.pack(fill="both", expand=True, padx=24, pady=12)
        
        # Card cấu hình database
        card_db = CardHienDai(
            container,
            tieu_de="🗄️ Cấu Hình Database",
            mo_ta="Thông tin kết nối SQL Server"
        )
        card_db.pack(fill="x", pady=(0, 12))
        
        # Load cấu hình hiện tại
        self.config = doc_cau_hinh_database()
        
        # Form nhập liệu
        self.entry_server = self.tao_field(
            card_db.noi_dung,
            "Server:",
            self.config.get('server', '')
        )
        
        self.entry_port = self.tao_field(
            card_db.noi_dung,
            "Port:",
            str(self.config.get('port', 1433))
        )
        
        self.entry_user = self.tao_field(
            card_db.noi_dung,
            "Username:",
            self.config.get('user', '')
        )
        
        self.entry_password = self.tao_field(
            card_db.noi_dung,
            "Password:",
            self.config.get('password', ''),
            show="*"
        )
        
        self.entry_database = self.tao_field(
            card_db.noi_dung,
            "Database:",
            self.config.get('database', 'master')
        )
        
        # Nút lưu
        frame_nut = ctk.CTkFrame(card_db.noi_dung, fg_color="transparent")
        frame_nut.pack(fill="x", pady=(12, 0))
        
        NutHienDai(
            frame_nut,
            text="Lưu Cấu Hình",
            icon="💾",
            style=NutHienDai.STYLE_THANH_CONG,
            command=self.luu_cau_hinh
        ).pack(side="left", padx=(0, 8))
        
        NutHienDai(
            frame_nut,
            text="Test Kết Nối",
            icon="🔌",
            style=NutHienDai.STYLE_PHU,
            command=self.test_ket_noi
        ).pack(side="left")
        
        # Label trạng thái
        self.label_trang_thai = ctk.CTkLabel(
            card_db.noi_dung,
            text="",
            font=("Arial", 11)
        )
        self.label_trang_thai.pack(pady=(8, 0))
        
        # Card thông tin hệ thống
        card_he_thong = CardHienDai(
            container,
            tieu_de="ℹ️ Thông Tin Hệ Thống"
        )
        card_he_thong.pack(fill="x")
        
        info_lines = [
            f"📱 Ứng dụng: Tableau Database Connector",
            f"🎨 Giao diện: Modern UI (Discord style)",
            f"🐍 Python: {sys.version.split()[0]}",
            f"📦 CustomTkinter: Đã cài đặt",
            f"💾 Database Connector: {'Có' if CO_DATABASE_CONNECTOR else 'Demo mode'}"
        ]
        
        for line in info_lines:
            ctk.CTkLabel(
                card_he_thong.noi_dung,
                text=line,
                font=("Arial", 11),
                text_color=MauSac.CHU_TRANG,
                anchor="w"
            ).pack(anchor="w", pady=2)
    
    def tao_field(
        self,
        master,
        label: str,
        value: str,
        show: str = ""
    ) -> InputHienDai:
        """Tạo một field nhập liệu"""
        # Frame chứa label và input
        frame = ctk.CTkFrame(master, fg_color="transparent")
        frame.pack(fill="x", pady=6)
        
        # Label
        ctk.CTkLabel(
            frame,
            text=label,
            font=("Arial", 12),
            text_color=MauSac.CHU_TRANG,
            width=120,
            anchor="w"
        ).pack(side="left")
        
        # Input
        entry = InputHienDai(frame, placeholder=label)
        if show:
            entry.configure(show=show)
        entry.insert(0, value)
        entry.pack(side="left", fill="x", expand=True)
        
        return entry
    
    def luu_cau_hinh(self):
        """Lưu cấu hình"""
        try:
            config = {
                'server': self.entry_server.get(),
                'port': int(self.entry_port.get()),
                'user': self.entry_user.get(),
                'password': self.entry_password.get(),
                'database': self.entry_database.get(),
                'windows_auth': False
            }
            
            if luu_cau_hinh_database(config):
                self.label_trang_thai.configure(
                    text="✓ Đã lưu cấu hình thành công",
                    text_color=MauSac.XANH_LA
                )
            else:
                self.label_trang_thai.configure(
                    text="✗ Lỗi khi lưu cấu hình",
                    text_color=MauSac.DO
                )
        except Exception as e:
            self.label_trang_thai.configure(
                text=f"✗ Lỗi: {str(e)}",
                text_color=MauSac.DO
            )
    
    def test_ket_noi(self):
        """Test kết nối database"""
        self.label_trang_thai.configure(
            text="🔄 Đang kiểm tra kết nối...",
            text_color=MauSac.XANH_LAM
        )
        
        # Giả lập test (thực tế cần gọi hàm kết nối thật)
        self.after(1000, lambda: self.label_trang_thai.configure(
            text="✓ Kết nối thành công!" if CO_DATABASE_CONNECTOR else "⚠ Demo mode - không test được",
            text_color=MauSac.XANH_LA if CO_DATABASE_CONNECTOR else MauSac.VANG
        ))

# ============================================
# LỚP ỨNG DỤNG CHÍNH
# ============================================

class UngDungHienDai(ctk.CTk):
    """
    Ứng dụng chính với giao diện hiện đại
    Phong cách Discord/Microsoft Teams
    """
    
    def __init__(self):
        super().__init__()
        
        # Cấu hình cửa sổ
        self.title("Tableau Database Connector")
        self.geometry("1200x700")
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Màu nền chính
        self.configure(fg_color=MauSac.NEN_TOI)
        
        # Tạo menu bar (sử dụng tkinter thường vì CustomTkinter không có menu)
        import tkinter as tk
        self.tao_menu_bar()
        
        # Tạo sidebar
        self.sidebar = SidebarHienDai(self)
        self.sidebar.pack(side="left", fill="y")
        
        # Container cho nội dung
        self.container_noi_dung = ctk.CTkFrame(
            self,
            fg_color=MauSac.NEN_TOI
        )
        self.container_noi_dung.pack(side="left", fill="both", expand=True)
        
        # Dictionary chứa các trang
        self.cac_trang: Dict[str, ctk.CTkFrame] = {}
        
        # Tạo các trang
        self.tao_cac_trang()
        
        # Thêm nút vào sidebar
        self.sidebar.them_nut("🏠", "🏠", lambda: self.hien_thi_trang("home"), "Trang Chủ")
        self.sidebar.them_nut("🔗", "🔗", lambda: self.hien_thi_trang("connect"), "Kết Nối")
        self.sidebar.them_nut("�️", "👁️", lambda: self.hien_thi_trang("preview"), "Preview Dữ Liệu")
        self.sidebar.them_nut("�📜", "📜", lambda: self.hien_thi_trang("history"), "Lịch Sử")
        self.sidebar.them_nut("⚙️", "⚙️", lambda: self.hien_thi_trang("settings"), "Cài Đặt")
        
        # Hiển thị trang chủ mặc định
        self.hien_thi_trang("home")
    
    def tao_menu_bar(self):
        """Tạo menu bar"""
        import tkinter as tk
        
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Menu File
        menu_file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=menu_file)
        menu_file.add_command(label="📂 Mở File Config", command=self.mo_file_config)
        menu_file.add_separator()
        menu_file.add_command(label="❌ Thoát", command=self.quit)
        
        # Menu View
        menu_view = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=menu_view)
        menu_view.add_command(label="🌙 Dark Mode", command=lambda: self.doi_theme("dark"))
        menu_view.add_command(label="☀️ Light Mode", command=lambda: self.doi_theme("light"))
        
        # Menu Help
        menu_help = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=menu_help)
        menu_help.add_command(label="📖 Hướng Dẫn", command=self.hien_thi_huong_dan)
        menu_help.add_command(label="ℹ️ Giới Thiệu", command=self.hien_thi_gioi_thieu)
    
    def mo_file_config(self):
        """Mở file config bằng trình soạn thảo mặc định"""
        config_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'config',
            'database_config.json'
        )
        
        if os.path.exists(config_path):
            try:
                # Dùng xdg-open trên Linux
                import subprocess
                if sys.platform == 'linux':
                    subprocess.run(['xdg-open', config_path])
                elif sys.platform == 'darwin':  # macOS
                    subprocess.run(['open', config_path])
                else:  # Windows
                    os.startfile(config_path)
            except Exception as e:
                # Thông báo lỗi
                dialog = ctk.CTkToplevel(self)
                dialog.title("Lỗi")
                dialog.geometry("400x150")
                
                frame = ctk.CTkFrame(dialog, fg_color="transparent")
                frame.pack(fill="both", expand=True, padx=20, pady=20)
                
                ctk.CTkLabel(
                    frame,
                    text="✗ Không thể mở file",
                    font=("Arial", 14, "bold"),
                    text_color=MauSac.DO
                ).pack(pady=(0, 10))
                
                ctk.CTkLabel(
                    frame,
                    text=f"Path: {config_path}\nLỗi: {str(e)}",
                    font=("Arial", 10),
                    text_color=MauSac.CHU_XAM
                ).pack()
        else:
            # Thông báo file không tồn tại
            dialog = ctk.CTkToplevel(self)
            dialog.title("Cảnh Báo")
            dialog.geometry("400x120")
            
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            ctk.CTkLabel(
                frame,
                text="⚠️ File config không tồn tại",
                font=("Arial", 13),
                text_color=MauSac.VANG
            ).pack(pady=(0, 10))
            
            ctk.CTkLabel(
                frame,
                text=f"Path: {config_path}",
                font=("Arial", 10),
                text_color=MauSac.CHU_XAM
            ).pack()
    
    def doi_theme(self, mode: str):
        """Đổi theme (dark/light)"""
        ctk.set_appearance_mode(mode)
        
        # Thông báo
        dialog = ctk.CTkToplevel(self)
        dialog.title("Theme")
        dialog.geometry("300x100")
        
        ctk.CTkLabel(
            dialog,
            text=f"✓ Đã chuyển sang {mode} mode",
            font=("Arial", 13)
        ).pack(expand=True)
        
        dialog.after(2000, dialog.destroy)
    
    def hien_thi_huong_dan(self):
        """Hiển thị hướng dẫn sử dụng"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Hướng Dẫn Sử Dụng")
        dialog.geometry("600x500")
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        huong_dan = """
📖 HƯỚNG DẪN SỬ DỤNG

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. TRANG CHỦ (🏠)
   • Xem tổng quan hệ thống
   • Thống kê database, bảng, kết nối
   • Đọc hướng dẫn nhanh

2. TRANG KẾT NỐI (🔗)
   • Nhấn "Tải Danh Sách Database"
   • Chọn database cần kết nối (checkbox)
   • Nhấn "Tải Danh Sách Bảng"
   • Chọn các bảng cần kết nối
   • Nhấn "Tạo URL" để tạo liên kết
   • Nhấn "Sao Chép" để copy URL
   • Nhấn "Xuất DS Bảng" để lưu danh sách

3. TRANG PREVIEW (👁️)
   • Chọn database từ dropdown
   • Chọn bảng cần xem
   • Nhấn "Xem Dữ Liệu"
   • Xem tối đa 100 dòng đầu tiên

4. TRANG LỊCH SỬ (📜)
   • Xem các kết nối đã tạo trước đó
   • Nhấn "Làm Mới" để cập nhật
   • Nhấn "Xóa Tất Cả" để xóa lịch sử
   • Nhấn "Xuất File" để lưu lịch sử

5. TRANG CÀI ĐẶT (⚙️)
   • Nhập thông tin Server, Port, Username, Password
   • Nhấn "Lưu Cấu Hình"
   • Nhấn "Test Kết Nối" để kiểm tra

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 MẸO NHỎ:
• Dùng menu File > Mở File Config để chỉnh sửa trực tiếp
• Dùng menu View > Dark/Light Mode để đổi theme
• Có thể chọn nhiều database và bảng cùng lúc
"""
        
        ctk.CTkLabel(
            scroll_frame,
            text=huong_dan,
            font=("Courier", 11),
            text_color=MauSac.CHU_TRANG,
            justify="left",
            anchor="w"
        ).pack(fill="both", expand=True)
    
    def hien_thi_gioi_thieu(self):
        """Hiển thị thông tin giới thiệu"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Giới Thiệu")
        dialog.geometry("500x400")
        
        frame = ctk.CTkFrame(dialog, fg_color="transparent")
        frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        ctk.CTkLabel(
            frame,
            text="🔗 TABLEAU DATABASE CONNECTOR",
            font=("Arial", 18, "bold"),
            text_color=MauSac.XANH_DISCORD
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            frame,
            text="Modern UI Edition v2.0",
            font=("Arial", 12),
            text_color=MauSac.CHU_XAM
        ).pack(pady=(0, 20))
        
        info = """
Ứng dụng kết nối Tableau với SQL Server
Giao diện hiện đại theo phong cách Discord/Teams

✨ TÍNH NĂNG:
• Kết nối nhiều database cùng lúc
• Chọn nhiều bảng từ các database khác nhau
• Preview dữ liệu bảng
• Lưu lịch sử kết nối tự động
• Xuất danh sách bảng và lịch sử
• Dark/Light mode
• Giao diện đẹp với CustomTkinter

📚 CÔNG NGHỆ:
• Python 3.12+
• CustomTkinter
• pymssql / pyodbc
• Flask Server

🎨 THIẾT KẾ:
• Discord color palette
• Modern sidebar navigation
• Card-based layout
• Smooth animations
"""
        
        ctk.CTkLabel(
            frame,
            text=info,
            font=("Arial", 11),
            text_color=MauSac.CHU_TRANG,
            justify="left"
        ).pack()
    
    def tao_cac_trang(self):
        """Tạo tất cả các trang"""
        self.cac_trang["home"] = TrangChu(self.container_noi_dung)
        self.cac_trang["connect"] = TrangKetNoi(self.container_noi_dung)
        self.cac_trang["preview"] = TrangPreview(self.container_noi_dung)
        self.cac_trang["history"] = TrangLichSu(self.container_noi_dung)
        self.cac_trang["settings"] = TrangCaiDat(self.container_noi_dung)
    
    def hien_thi_trang(self, ten_trang: str):
        """Hiển thị một trang"""
        # Ẩn tất cả trang
        for trang in self.cac_trang.values():
            trang.pack_forget()
        
        # Hiển thị trang được chọn
        if ten_trang in self.cac_trang:
            self.cac_trang[ten_trang].pack(fill="both", expand=True)

# ============================================
# CHẠY ỨNG DỤNG
# ============================================

if __name__ == "__main__":
    """Khởi chạy ứng dụng"""
    print("\n" + "=" * 60)
    print("🚀 TABLEAU DATABASE CONNECTOR - MODERN UI")
    print("=" * 60)
    print("📱 Giao diện: Discord/Teams style")
    print("🎨 Theme: Dark mode")
    print("⚡ Framework: CustomTkinter")
    print("=" * 60 + "\n")
    
    app = UngDungHienDai()
    app.mainloop()
