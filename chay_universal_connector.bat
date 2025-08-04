@echo off
chcp 65001 >nul
echo 🚀 CHẠY UNIVERSAL TABLEAU CONNECTOR
echo ==========================================

REM Lưu thư mục hiện tại và chuyển về thư mục dự án
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"
echo 📁 Thư mục dự án: %PROJECT_DIR%

echo.
echo 📋 Bước 1: Kiểm tra config
if exist "config\database_config.json" (
    echo ✅ Config file tồn tại
) else (
    echo ❌ Không tìm thấy config file
    echo 💡 Chạy: python scripts\cau_hinh_database.py
    pause
    exit
)

echo.
echo 📋 Bước 2: Kiểm tra và kích hoạt Python env
if exist "env\Scripts\activate.bat" (
    echo ✅ Tìm thấy Python environment
    call "%PROJECT_DIR%env\Scripts\activate.bat"
    echo ✅ Đã kích hoạt Python environment
) else (
    echo ❌ Không tìm thấy Python environment tại: %PROJECT_DIR%env\Scripts\
    echo 💡 Hãy tạo environment bằng: python -m venv env
    pause
    exit
)

echo.
echo 📋 Bước 3: Kiểm tra dependencies
echo 🔍 Kiểm tra thư viện Python cần thiết...
python -c "import pymssql, flask; print('✅ Tất cả thư viện đã cài đặt')" 2>nul || (
    echo ❌ Thiếu thư viện Python
    echo 💡 Đang cài đặt dependencies...
    pip install -r "%PROJECT_DIR%config\requirements.txt"
)

echo.
echo 📋 Bước 4: Chạy Universal Connector
echo 🌐 Server sẽ chạy tại: http://127.0.0.1:5002
echo 📊 Để kết nối Tableau: Web Data Connector -> http://127.0.0.1:5002
echo 🎯 Nhấn Ctrl+C để dừng server
echo.

cd /d "%PROJECT_DIR%src"
if exist "tableau_universal_connector.py" (
    echo ✅ Tìm thấy Universal Connector
    echo 🚀 Đang khởi động server...
    echo.
    python tableau_universal_connector.py
) else (
    echo ❌ Không tìm thấy tableau_universal_connector.py trong thư mục src
    cd /d "%PROJECT_DIR%"
    pause
    exit
)

REM Quay về thư mục gốc khi kết thúc
cd /d "%PROJECT_DIR%"
echo.
echo 🎯 Server đã dừng. Nhấn phím bất kỳ để thoát...
pause
