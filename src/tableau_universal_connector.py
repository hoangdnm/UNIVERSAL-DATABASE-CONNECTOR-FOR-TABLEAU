#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TABLEAU UNIVERSAL DATABASE CONNECTOR
Refactored version - Main Application

Dự án: Kết nối Tableau với bất kỳ SQL Server database nào
Tác giả: Đào Ngọc Minh Hoàng
Trường: FPT Polytechnic
Năm: 2024-2025
"""

from flask import Flask, render_template
import os
import sys

# Thêm thư mục src vào path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import routes
from routes.api_routes import register_routes


# Khởi tạo Flask app
app = Flask(__name__, 
           template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates'))


# Route chính - Trang Web Data Connector
@app.route('/')
def tableau_wdc():
    """
    Trang chính của Tableau Universal Database Connector
    Render HTML template từ file riêng
    """
    return render_template('wdc_template.html')


# Đăng ký tất cả API routes
register_routes(app)


def main():
    """
    Hàm main - Khởi động Flask server
    """
    print("=" * 70)
    print("🌐 TABLEAU UNIVERSAL DATABASE CONNECTOR")
    print("=" * 70)
    print("🚀 Đang khởi động server...")
    print("🔗 URL cho Tableau: http://127.0.0.1:5002")
    print("📊 Cấu hình database: config/database_config.json")
    print("")
    print("🎯 TÍNH NĂNG NÂNG CẤP - FOCUS NHIỀU BẢNG:")
    print("  ✅ Chọn nhiều bảng cùng lúc bằng checkbox")
    print("  ✅ Mỗi bảng là một dataset riêng biệt trong Tableau")
    print("  ✅ KHÔNG tự động kết hợp dữ liệu")
    print("  ✅ User có thể chọn từng bảng để phân tích")
    print("  ✅ Hỗ trợ câu truy vấn WHERE tùy chỉnh")
    print("")
    print("📝 REFACTORED VERSION:")
    print("  ✅ Tách HTML template ra file riêng")
    print("  ✅ Tách API routes thành module riêng")
    print("  ✅ Tách schema detector thành utils")
    print("  ✅ Code gọn hơn, dễ bảo trì hơn")
    print("")
    print("⏹️  Nhấn Ctrl+C để dừng server")
    print("=" * 70)
    
    # Chạy Flask server
    app.run(debug=True, host='127.0.0.1', port=5002)


if __name__ == '__main__':
    main()
