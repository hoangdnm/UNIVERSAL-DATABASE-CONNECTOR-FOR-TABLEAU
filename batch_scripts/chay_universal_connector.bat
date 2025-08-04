@echo off
chcp 65001 >nul
title Tableau Universal Database Connector
cls

echo 🚀 TABLEAU UNIVERSAL DATABASE CONNECTOR
echo ==========================================

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
echo � Kích hoạt virtual environment...
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
echo 📡 Kiểm tra SQL Server...
python -c "import pymssql; conn = pymssql.connect(server='127.0.0.1', port=1235, user='sa', password='YourStrong!Pass123', database='master'); conn.close(); print('✅ SQL Server OK')" 2>nul
if %errorlevel% neq 0 (
    echo ❌ SQL Server không kết nối được
    echo 💡 Kiểm tra Docker: docker ps
    echo 💡 Khởi động SQL Server: docker-compose up -d
    echo 💡 Hoặc chạy: scripts\tao_database_test.py
    pause
    exit /b 1
)

echo.
echo 🌐 Khởi động Universal Connector...
echo 📊 URL cho Tableau: http://127.0.0.1:5002
echo 🌍 URL cho Web Browser: http://127.0.0.1:5002
echo ⏹️  Nhấn Ctrl+C để dừng server
echo.

python src\tableau_universal_connector.py

echo.
echo 👋 Server đã dừng
pause
