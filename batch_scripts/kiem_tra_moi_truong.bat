@echo off
chcp 65001 >nul
echo 🔧 KIỂM TRA MÔI TRƯỜNG DỰ ÁN
echo ==========================================

REM Lưu thư mục hiện tại và di chuyển về thư mục dự án
set "PROJECT_DIR=%~dp0\.."
cd /d "%PROJECT_DIR%"
echo 📁 Thư mục dự án: %CD%

REM Kiểm tra xem có đúng thư mục dự án không
if not exist "src\tableau_universal_connector.py" (
    echo ❌ Không tìm thấy file src\tableau_universal_connector.py
    echo 📁 Thư mục hiện tại: %CD%
    echo 💡 Đảm bảo bạn đang ở đúng thư mục dự án
    pause
    exit /b 1
)

echo.
echo 📋 KIỂM TRA CÁC THÀNH PHẦN QUAN TRỌNG:
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python đã cài đặt
    python --version
) else (
    echo ❌ Python chưa cài đặt hoặc không trong PATH
    echo 💡 Cần cài đặt Python 3.8+ từ python.org
)

echo.

REM Kiểm tra virtual environment
if exist "env\Scripts\python.exe" (
    echo ✅ Virtual environment tồn tại: env\
    call "env\Scripts\activate.bat"
    echo 🐍 Python trong env:
    python --version
) else (
    echo ❌ Virtual environment không tồn tại
    echo 💡 Tạo bằng: python -m venv env
)

echo.

REM Kiểm tra config
if exist "config\database_config.json" (
    echo ✅ Database config tồn tại
    type "config\database_config.json"
) else (
    echo ❌ Database config chưa có
    echo 💡 Chạy: python scripts\cau_hinh_database.py
)

echo.

REM Kiểm tra Docker
docker ps >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker đang chạy
    docker ps --filter "name=mssql" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
) else (
    echo ❌ Docker không chạy hoặc chưa cài đặt
    echo 💡 Khởi động Docker Desktop và chạy: docker-compose up -d
)

echo.

REM Kiểm tra các file quan trọng
echo 📂 CÁC FILE QUAN TRỌNG:
set files=src\tableau_universal_connector.py scripts\cau_hinh_database.py config\requirements.txt tests\kiem_thu_du_an.py
for %%f in (%files%) do (
    if exist "%%f" (
        echo ✅ %%f
    ) else (
        echo ❌ %%f - THIẾU
    )
)

echo.
echo 🎯 Nếu tất cả ✅ thì chạy: chay_universal_connector.bat
echo.
pause
