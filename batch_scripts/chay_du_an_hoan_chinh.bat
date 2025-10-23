@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

::############################################
:: SCRIPT CHẠY DỰ ÁN HOÀN CHỈNH (WINDOWS)
:: Tự động khởi động Web Server và Desktop App
::############################################

echo ========================================
echo   TABLEAU UNIVERSAL CONNECTOR
echo   Script Khởi Động Tự Động
echo ========================================
echo.

:: Lấy thư mục gốc của dự án
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."
cd /d "%PROJECT_DIR%"

:: Kiểm tra môi trường Python
echo [1/5] Kiểm tra môi trường Python...

:: Đếm số môi trường tìm thấy
set ENV_COUNT=0
set ENV_LIST=
set ENV_PATHS=

:: Kiểm tra env
if exist "%PROJECT_DIR%\env\Scripts\python.exe" (
    set /a ENV_COUNT+=1
    set "ENV_LIST=!ENV_LIST!  [!ENV_COUNT!] env (Thư mục gốc)%LF%"
    set "ENV_PATH_!ENV_COUNT!=%PROJECT_DIR%\env\Scripts\python.exe"
)

:: Kiểm tra venv
if exist "%PROJECT_DIR%\venv\Scripts\python.exe" (
    set /a ENV_COUNT+=1
    set "ENV_LIST=!ENV_LIST!  [!ENV_COUNT!] venv (Thư mục gốc)%LF%"
    set "ENV_PATH_!ENV_COUNT!=%PROJECT_DIR%\venv\Scripts\python.exe"
)

:: Kiểm tra .venv
if exist "%PROJECT_DIR%\.venv\Scripts\python.exe" (
    set /a ENV_COUNT+=1
    set "ENV_LIST=!ENV_LIST!  [!ENV_COUNT!] .venv (Thư mục gốc)%LF%"
    set "ENV_PATH_!ENV_COUNT!=%PROJECT_DIR%\.venv\Scripts\python.exe"
)

:: Kiểm tra Python hệ thống
where python >nul 2>&1
if !errorlevel! equ 0 (
    set /a ENV_COUNT+=1
    set "ENV_LIST=!ENV_LIST!  [!ENV_COUNT!] Python hệ thống%LF%"
    set "ENV_PATH_!ENV_COUNT!=python"
)

:: Nếu không tìm thấy môi trường nào
if !ENV_COUNT! equ 0 (
    echo [X] Không tìm thấy môi trường Python nào!
    echo     Vui lòng cài đặt Python hoặc tạo môi trường ảo.
    pause
    exit /b 1
)

:: Hiển thị danh sách môi trường
echo Tìm thấy !ENV_COUNT! môi trường:
echo !ENV_LIST!

:: Cho phép người dùng chọn
if !ENV_COUNT! equ 1 (
    echo Tự động chọn môi trường duy nhất
    set SELECTED=1
) else (
    set /p SELECTED="Chọn môi trường (1-!ENV_COUNT!): "
)

:: Kiểm tra lựa chọn hợp lệ
if !SELECTED! lss 1 (
    echo [X] Lựa chọn không hợp lệ!
    pause
    exit /b 1
)
if !SELECTED! gtr !ENV_COUNT! (
    echo [X] Lựa chọn không hợp lệ!
    pause
    exit /b 1
)

:: Lấy đường dẫn Python đã chọn
set "PYTHON_CMD=!ENV_PATH_%SELECTED%!"
echo [✓] Đã chọn môi trường !SELECTED!
echo.

:: Kiểm tra Python hoạt động
echo [2/5] Kiểm tra Python...
!PYTHON_CMD! --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [X] Không thể chạy Python!
    pause
    exit /b 1
)
for /f "delims=" %%v in ('!PYTHON_CMD! --version') do echo [✓] %%v
echo.

:: Kiểm tra các file cần thiết
echo [3/5] Kiểm tra các file dự án...

set "WEB_SERVER=%PROJECT_DIR%\src\tableau_universal_connector.py"
set "DESKTOP_APP=%PROJECT_DIR%\Window_application\bai_5_hoan_chinh.py"

if not exist "!WEB_SERVER!" (
    echo [X] Không tìm thấy: !WEB_SERVER!
    pause
    exit /b 1
)

if not exist "!DESKTOP_APP!" (
    echo [X] Không tìm thấy: !DESKTOP_APP!
    pause
    exit /b 1
)

echo [✓] Web Server: src\tableau_universal_connector.py
echo [✓] Desktop App: Window_application\bai_5_hoan_chinh.py
echo.

:: Kiểm tra port 5002
echo [4/5] Kiểm tra port 5002...
netstat -ano | findstr ":5002" | findstr "LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo [!] Port 5002 đang được sử dụng. Dừng process cũ...
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5002" ^| findstr "LISTENING"') do (
        taskkill /F /PID %%a >nul 2>&1
    )
    timeout /t 2 /nobreak >nul
    echo [✓] Đã dừng process cũ
) else (
    echo [✓] Port 5002 sẵn sàng
)
echo.

:: Khởi động Web Server
echo [5/5] Khởi động ứng dụng...
echo → Khởi động Web Server (port 5002)...

start /b "TableauWebServer" !PYTHON_CMD! "!WEB_SERVER!" > "%TEMP%\tableau_web_server.log" 2>&1

:: Đợi web server khởi động
echo   Đợi Web Server khởi động...
timeout /t 3 /nobreak >nul

:: Kiểm tra web server có chạy không
netstat -ano | findstr ":5002" | findstr "LISTENING" >nul 2>&1
if !errorlevel! equ 0 (
    echo [✓] Web Server đã khởi động
    echo     URL: http://127.0.0.1:5002
) else (
    echo [X] Web Server không khởi động được!
    echo     Xem log tại: %TEMP%\tableau_web_server.log
    type "%TEMP%\tableau_web_server.log"
    pause
    exit /b 1
)
echo.

:: Khởi động Desktop App
echo → Khởi động Desktop App...
start "TableauDesktopApp" !PYTHON_CMD! "!DESKTOP_APP!"
echo [✓] Desktop App đã khởi động
echo.

:: Hướng dẫn
echo ========================================
echo [✓] DỰ ÁN ĐÃ KHỞI ĐỘNG THÀNH CÔNG!
echo ========================================
echo.
echo Hướng dẫn sử dụng:
echo   1. Sử dụng Desktop App để chọn database và bảng
echo   2. Click 'Tạo URL' để tạo đường dẫn kết nối
echo   3. Click 'Mở Trình Duyệt' để mở web interface
echo   4. Sử dụng trong Tableau với Web Data Connector
echo.
echo Để dừng ứng dụng:
echo   - Đóng Desktop App
echo   - Nhấn phím bất kỳ trong terminal này để dừng Web Server
echo.
echo Log files:
echo   - Web Server: %TEMP%\tableau_web_server.log
echo.
echo ========================================

:: Đợi người dùng nhấn phím để dừng
pause

:: Dừng Web Server
echo.
echo Đang dừng Web Server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":5002" ^| findstr "LISTENING"') do (
    taskkill /F /PID %%a >nul 2>&1
)

echo [✓] Đã dừng tất cả ứng dụng
echo ========================================
pause
