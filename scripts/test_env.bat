@echo off
chcp 65001 >nul
title Test Virtual Environment
cls

echo 🔧 TEST VIRTUAL ENVIRONMENT
echo ============================

REM Di chuyển về thư mục dự án
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"
echo 📁 Thư mục: %CD%

echo.
echo 1. Kiểm tra file activate:
if exist "env\Scripts\activate.bat" (
    echo ✅ activate.bat TỒN TẠI
) else (
    echo ❌ activate.bat KHÔNG TỒN TẠI
)

if exist "env\Scripts\python.exe" (
    echo ✅ python.exe TỒN TẠI
) else (
    echo ❌ python.exe KHÔNG TỒN TẠI
)

echo.
echo 2. Test Python hệ thống:
python --version

echo.
echo 3. Test Python trong virtual env:
"env\Scripts\python.exe" --version

echo.
echo 4. Test thư viện với Python hệ thống:
python -c "import pymssql; print('pymssql OK')" 2>nul || echo "pymssql THIẾU"
python -c "import flask; print('flask OK')" 2>nul || echo "flask THIẾU"

echo.
echo 5. Test thư viện với Python virtual env:
"env\Scripts\python.exe" -c "import pymssql; print('pymssql OK')" 2>nul || echo "pymssql THIẾU"
"env\Scripts\python.exe" -c "import flask; print('flask OK')" 2>nul || echo "flask THIẾU"

echo.
echo 6. Test activate script:
call "env\Scripts\activate.bat"
echo Current PATH: %PATH%
python --version
python -c "import pymssql; print('pymssql OK sau activate')" 2>nul || echo "pymssql THIẾU sau activate"

echo.
echo =============================
echo Test hoàn tất!
pause
