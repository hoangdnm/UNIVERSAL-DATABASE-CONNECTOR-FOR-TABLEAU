@echo off
echo ====================================
echo  RESTART FLASK SERVER
echo ====================================
echo.

REM Kill any existing Python processes running the server
echo [1/3] Dung server cu...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *tableau_universal_connector*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo [2/3] Khoi dong server moi...
echo.
start "Tableau WDC Server" cmd /k "cd /d %~dp0 && python src\tableau_universal_connector.py"

timeout /t 3 /nobreak >nul

echo.
echo [3/3] Hoan thanh!
echo.
echo ============================================
echo  Server dang chay tai: http://127.0.0.1:5002
echo ============================================
echo.
echo Nhan phim bat ky de dong cua so nay...
pause >nul
