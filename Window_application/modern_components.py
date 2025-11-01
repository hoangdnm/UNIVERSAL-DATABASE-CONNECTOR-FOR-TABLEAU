

import customtkinter as ctk
from typing import Callable, Optional
from PIL import Image
import os

# ============================================
# CẤU HÌNH MÀU SẮC (DARK MODE - DISCORD STYLE)
# ============================================

class MauSac:
    """Bảng màu theo phong cách Discord"""
    # Màu nền
    NEN_TOI = "#2b2d31"  # Nền chính (giống Discord)
    NEN_SIDEBAR = "#1e1f22"  # Sidebar tối hơn
    NEN_CARD = "#383a40"  # Card/panel
    
    # Màu chữ
    CHU_TRANG = "#f2f3f5"  # Chữ trắng chính
    CHU_XAM = "#b5bac1"  # Chữ xám phụ
    
    # Màu điểm nhấn (accent colors)
    XANH_DISCORD = "#5865f2"  # Xanh Discord chính
    XANH_HOVER = "#4752c4"  # Xanh khi hover
    XANH_LAM = "#00aff4"  # Xanh lam Teams
    
    # Màu trạng thái
    XANH_LA = "#3ba55d"  # Thành công
    DO = "#ed4245"  # Lỗi/nguy hiểm
    VANG = "#faa81a"  # Cảnh báo
    
    # Màu viền
    VIEN = "#42464d"

# ============================================
# COMPONENT: SIDEBAR (THANH ĐIỀU HƯỚNG)
# ============================================

class SidebarHienDai(ctk.CTkFrame):
    """Thanh Sidebar hiện đại giống Discord"""
    
    def __init__(self, master, chieu_rong: int = 72, **kwargs):
        super().__init__(
            master,
            width=chieu_rong,
            fg_color=MauSac.NEN_SIDEBAR,
            corner_radius=0,
            **kwargs
        )
        
        self.pack_propagate(False)
        self.cac_nut = []
        self.nut_dang_chon = None
        
        # Logo/Avatar ở đầu
        self.tao_logo()
        
        # Separator (thanh ngăn)
        ctk.CTkFrame(
            self,
            height=2,
            fg_color=MauSac.VIEN
        ).pack(pady=10, padx=16, fill="x")
    
    def tao_logo(self):
        """Tạo logo/avatar ở đầu sidebar"""
        logo_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        logo_frame.pack(pady=20)
        
        # Đường dẫn tới hình ảnh logo
        logo_path = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "images",
            "Slack-01.webp"
        )
        
        try:
            # Tải và resize hình ảnh
            logo_image = Image.open(logo_path)
            logo_image = logo_image.resize((50, 50), Image.Resampling.LANCZOS)
            logo_ctk = ctk.CTkImage(
                light_image=logo_image,
                dark_image=logo_image,
                size=(50, 50)
            )
            
            # Hiển thị logo bằng Label
            ctk.CTkLabel(
                logo_frame,
                image=logo_ctk,
                text="",  # Không có chữ
                fg_color="transparent"
            ).pack()
            
        except Exception as e:
            # Nếu không tải được hình, dùng chữ TDC
            print(f"Không tải được logo: {e}")
            ctk.CTkButton(
                logo_frame,
                text="TDC",
                font=("Arial Black", 14, "bold"),
                text_color="#ffffff",
                width=50,
                height=50,
                fg_color=MauSac.XANH_DISCORD,
                hover_color=MauSac.XANH_DISCORD,
                corner_radius=25,
                state="disabled",
                cursor="arrow"
            ).pack()
    
    def them_nut(
        self,
        text: str,
        icon: str,
        command: Callable,
        tooltip: Optional[str] = None
    ):
        """Thêm nút điều hướng vào sidebar"""
        nut = NutSidebar(
            self,
            text=icon,
            command=lambda: self.chon_nut(nut, command),
            tooltip=tooltip or text
        )
        nut.pack(pady=4)
        self.cac_nut.append(nut)
        
        return nut
    
    def chon_nut(self, nut: 'NutSidebar', command: Callable):
        """Xử lý khi chọn nút"""
        # Bỏ chọn nút cũ
        if self.nut_dang_chon:
            self.nut_dang_chon.dat_trang_thai(False)
        
        # Chọn nút mới
        nut.dat_trang_thai(True)
        self.nut_dang_chon = nut
        
        # Gọi command
        if command:
            command()

class NutSidebar(ctk.CTkButton):
    """Nút trong sidebar với hiệu ứng đẹp"""
    
    def __init__(self, master, text: str, command: Callable, tooltip: str = "", **kwargs):
        self.tooltip = tooltip
        self.dang_chon = False
        
        super().__init__(
            master,
            text=text,
            width=48,
            height=48,
            corner_radius=24,  # Tròn hoàn toàn
            fg_color="transparent",
            hover_color=MauSac.XANH_DISCORD,
            text_color=MauSac.CHU_XAM,
            font=("Arial", 20),
            command=command,
            **kwargs
        )
        
        # Bind hover events để show tooltip
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
    
    def dat_trang_thai(self, dang_chon: bool):
        """Đặt trạng thái chọn/không chọn"""
        self.dang_chon = dang_chon
        if dang_chon:
            self.configure(
                fg_color=MauSac.XANH_DISCORD,
                text_color=MauSac.CHU_TRANG
            )
        else:
            self.configure(
                fg_color="transparent",
                text_color=MauSac.CHU_XAM
            )
    
    def on_enter(self, event):
        """Khi hover vào"""
        if not self.dang_chon:
            self.configure(corner_radius=16)  # Bo tròn ít hơn khi hover
    
    def on_leave(self, event):
        """Khi hover ra"""
        if not self.dang_chon:
            self.configure(corner_radius=24)  # Tròn hoàn toàn

# ============================================
# COMPONENT: CARD (KHUNG NỘI DUNG)
# ============================================

class CardHienDai(ctk.CTkFrame):
    """Card hiển thị nội dung"""
    
    def __init__(
        self,
        master,
        tieu_de: str = "",
        mo_ta: str = "",
        co_vien: bool = True,
        **kwargs
    ):
        super().__init__(
            master,
            fg_color=MauSac.NEN_CARD,
            corner_radius=8,
            border_width=1 if co_vien else 0,
            border_color=MauSac.VIEN,
            **kwargs
        )
        
        # Container chính
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=16, pady=16)
        
        # Header (nếu có tiêu đề)
        if tieu_de:
            self.header = ctk.CTkFrame(self.container, fg_color="transparent")
            self.header.pack(fill="x", pady=(0, 12))
            
            # Tiêu đề
            self.label_tieu_de = ctk.CTkLabel(
                self.header,
                text=tieu_de,
                font=("Arial", 16, "bold"),
                text_color=MauSac.CHU_TRANG,
                anchor="w"
            )
            self.label_tieu_de.pack(side="left", fill="x", expand=True)
        
        # Mô tả (nếu có)
        if mo_ta:
            self.label_mo_ta = ctk.CTkLabel(
                self.container,
                text=mo_ta,
                font=("Arial", 11),
                text_color=MauSac.CHU_XAM,
                anchor="w"
            )
            self.label_mo_ta.pack(fill="x", pady=(0, 8))
        
        # Nội dung (để thêm widget vào)
        self.noi_dung = ctk.CTkFrame(self.container, fg_color="transparent")
        self.noi_dung.pack(fill="both", expand=True)

# ============================================
# COMPONENT: BUTTON HIỆN ĐẠI
# ============================================

class NutHienDai(ctk.CTkButton):
    """Button hiện đại với nhiều style khác nhau"""
    
    STYLE_CHINH = "chinh"  # Primary (xanh Discord)
    STYLE_PHU = "phu"  # Secondary (xám)
    STYLE_THANH_CONG = "thanh_cong"  # Success (xanh lá)
    STYLE_NGUY_HIEM = "nguy_hiem"  # Danger (đỏ)
    
    def __init__(
        self,
        master,
        text: str,
        style: str = STYLE_CHINH,
        icon: str = "",
        **kwargs
    ):
        # Chọn màu theo style
        mau_map = {
            self.STYLE_CHINH: (MauSac.XANH_DISCORD, MauSac.XANH_HOVER),
            self.STYLE_PHU: ("#4e5058", "#6d6f78"),
            self.STYLE_THANH_CONG: (MauSac.XANH_LA, "#2d7d46"),
            self.STYLE_NGUY_HIEM: (MauSac.DO, "#c03537"),
        }
        
        fg_color, hover_color = mau_map.get(style, mau_map[self.STYLE_CHINH])
        
        # Text với icon
        text_full = f"{icon} {text}" if icon else text
        
        super().__init__(
            master,
            text=text_full,
            fg_color=fg_color,
            hover_color=hover_color,
            text_color=MauSac.CHU_TRANG,
            font=("Arial", 13, "bold"),
            corner_radius=6,
            height=40,
            cursor="hand2",
            **kwargs
        )

# ============================================
# COMPONENT: INPUT FIELD
# ============================================

class InputHienDai(ctk.CTkEntry):
    """Input field hiện đại"""
    
    def __init__(
        self,
        master,
        placeholder: str = "",
        **kwargs
    ):
        super().__init__(
            master,
            placeholder_text=placeholder,
            fg_color=MauSac.NEN_TOI,
            border_color=MauSac.VIEN,
            text_color=MauSac.CHU_TRANG,
            placeholder_text_color=MauSac.CHU_XAM,
            font=("Arial", 12),
            corner_radius=6,
            height=40,
            **kwargs
        )

# ============================================
# COMPONENT: BADGE (NHÃN SỐ THÔNG BÁO)
# ============================================

class Badge(ctk.CTkLabel):
    """Badge/tag nhỏ hiển thị số hoặc trạng thái"""
    
    def __init__(
        self,
        master,
        text: str = "0",
        mau_nen: str = MauSac.DO,
        **kwargs
    ):
        super().__init__(
            master,
            text=text,
            fg_color=mau_nen,
            text_color=MauSac.CHU_TRANG,
            font=("Arial", 10, "bold"),
            corner_radius=10,
            width=20,
            height=20,
            **kwargs
        )

# ============================================
# COMPONENT: SWITCH (CÔNG TẮC)
# ============================================

class SwitchHienDai(ctk.CTkSwitch):
    """Switch toggle hiện đại"""
    
    def __init__(
        self,
        master,
        text: str = "",
        **kwargs
    ):
        super().__init__(
            master,
            text=text,
            progress_color=MauSac.XANH_DISCORD,
            button_color=MauSac.CHU_TRANG,
            button_hover_color=MauSac.CHU_XAM,
            text_color=MauSac.CHU_TRANG,
            font=("Arial", 12),
            **kwargs
        )

# ============================================
# COMPONENT: HEADER BAR (THANH TIÊU ĐỀ)
# ============================================

class HeaderBar(ctk.CTkFrame):
    """Thanh header/tiêu đề giống Discord"""
    
    def __init__(
        self,
        master,
        tieu_de: str,
        mo_ta: str = "",
        **kwargs
    ):
        super().__init__(
            master,
            fg_color="transparent",
            **kwargs
        )
        
        # Cho phép tự động mở rộng chiều cao
        
        # Container
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=24, pady=16)
        
        # Tiêu đề
        ctk.CTkLabel(
            container,
            text=tieu_de,
            font=("Arial", 20, "bold"),
            text_color=MauSac.CHU_TRANG,
            anchor="w",
            wraplength=800  # Tự động xuống dòng nếu quá dài
        ).pack(side="top", anchor="w", fill="x")
        
        # Mô tả (nếu có)
        if mo_ta:
            ctk.CTkLabel(
                container,
                text=mo_ta,
                font=("Arial", 12),
                text_color=MauSac.CHU_XAM,
                anchor="w",
                wraplength=800  # Tự động xuống dòng nếu quá dài
            ).pack(side="top", anchor="w", pady=(6, 0), fill="x")
