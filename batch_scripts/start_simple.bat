@echo off
chcp 65001 >nul
title Chạy Universal Connector (Đơn giản)
cls

echo 🚀 KHỞI ĐỘNG UNIVERSAL CONNECTOR
echo ==================================

REM Di chuyển về thư mục dự án
cd /d "%~dp0\.."
echo 📁 Thư mục: %CD%

REM Kiểm tra xem có đúng thư mục dự án không
if not exist "src\tableau_universal_connector.py" (
    echo ❌ Không tìm thấy file src\tableau_universal_connector.py
    echo 📁 Thư mục hiện tại: %CD%
    echo 💡 Đảm bảo bạn đang ở đúng thư mục dự án
    pause
    exit /b 1
)

echo.
echo 🔧 Kích hoạt virtual environment...
if exist "env\Scripts\activate.bat" (
    call "env\Scripts\activate.bat"
    echo ✅ Virtual environment đã kích hoạt
) else (
    echo ❌ Không tìm thấy virtual environment
    echo 💡 Tạo bằng: python -m venv env
    pause
    exit /b 1
)

echo.
echo 🔍 Kiểm tra thư viện...
python -c "import pymssql, flask; print('✅ Thư viện OK')"
if %errorlevel% neq 0 (
    echo ❌ Thiếu thư viện, đang cài đặt...
    pip install -r config\requirements.txt
)

echo.
echo 🌐 Khởi động server...
echo 📊 URL: http://127.0.0.1:5002
echo ⏹️  Nhấn Ctrl+C để dừng
echo.

python src\tableau_universal_connector.py

echo.
echo 👋 Server đã dừng
pause
