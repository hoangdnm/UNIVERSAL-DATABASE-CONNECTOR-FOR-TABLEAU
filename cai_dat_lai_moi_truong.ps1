# 🔧 SCRIPT TỰ ĐỘNG CÀI ĐẶT LẠI MÔI TRƯỜNG

# Bước 1: Xóa môi trường ảo cũ
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BƯỚC 1: Xóa môi trường ảo cũ" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

if (Test-Path "env") {
    Write-Host "Đang xóa thư mục env cũ..." -ForegroundColor Gray
    Remove-Item -Path "env" -Recurse -Force
    Write-Host "✅ Đã xóa thành công!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Không tìm thấy thư mục env" -ForegroundColor Yellow
}

Write-Host ""

# Bước 2: Kiểm tra phiên bản Python
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BƯỚC 2: Kiểm tra Python" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

$pythonVersion = python --version 2>&1
Write-Host "Python hiện tại: $pythonVersion" -ForegroundColor Gray

if ($pythonVersion -like "*3.12*") {
    Write-Host "✅ Python 3.12 - Hoàn hảo!" -ForegroundColor Green
} elseif ($pythonVersion -like "*3.11*") {
    Write-Host "✅ Python 3.11 - Tốt!" -ForegroundColor Green
} elseif ($pythonVersion -like "*3.10*") {
    Write-Host "✅ Python 3.10 - OK!" -ForegroundColor Green
} elseif ($pythonVersion -like "*3.14*") {
    Write-Host "❌ Python 3.14 - Quá mới, không tương thích!" -ForegroundColor Red
    Write-Host "" 
    Write-Host "🔴 VUI LÒNG CÀI PYTHON 3.12 TRƯỚC:" -ForegroundColor Red
    Write-Host "   1. Vào https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "   2. Tải Python 3.12.7" -ForegroundColor Yellow
    Write-Host "   3. Cài đặt (nhớ tick 'Add to PATH')" -ForegroundColor Yellow
    Write-Host "   4. Mở PowerShell MỚI và chạy lại script này" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Nhấn Enter để thoát"
    exit 1
} else {
    Write-Host "⚠️  Phiên bản Python: $pythonVersion" -ForegroundColor Yellow
    Write-Host "   Khuyến nghị: Python 3.10, 3.11 hoặc 3.12" -ForegroundColor Yellow
}

Write-Host ""

# Bước 3: Tạo môi trường ảo mới
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BƯỚC 3: Tạo môi trường ảo mới" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Đang tạo môi trường ảo..." -ForegroundColor Gray
python -m venv env

if (Test-Path "env\Scripts\activate.ps1") {
    Write-Host "✅ Tạo môi trường ảo thành công!" -ForegroundColor Green
} else {
    Write-Host "❌ Lỗi tạo môi trường ảo!" -ForegroundColor Red
    Read-Host "Nhấn Enter để thoát"
    exit 1
}

Write-Host ""

# Bước 4: Kích hoạt môi trường ảo
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BƯỚC 4: Kích hoạt môi trường ảo" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Đang kích hoạt..." -ForegroundColor Gray
& ".\env\Scripts\Activate.ps1"

Write-Host "✅ Đã kích hoạt môi trường ảo!" -ForegroundColor Green
Write-Host ""

# Bước 5: Nâng cấp pip
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BƯỚC 5: Nâng cấp pip" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Đang nâng cấp pip..." -ForegroundColor Gray
python -m pip install --upgrade pip --quiet

Write-Host "✅ Đã nâng cấp pip!" -ForegroundColor Green
Write-Host ""

# Bước 6: Cài đặt thư viện
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BƯỚC 6: Cài đặt thư viện" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "Đang cài đặt Flask..." -ForegroundColor Gray
pip install Flask==2.3.3 --quiet

Write-Host "Đang cài đặt requests..." -ForegroundColor Gray
pip install requests==2.31.0 --quiet

Write-Host "Đang cài đặt Werkzeug..." -ForegroundColor Gray
pip install Werkzeug==2.3.7 --quiet

Write-Host ""
Write-Host "Đang cài đặt pymssql (có thể mất vài phút)..." -ForegroundColor Gray
pip install pymssql

Write-Host ""
Write-Host "✅ Đã cài đặt tất cả thư viện!" -ForegroundColor Green
Write-Host ""

# Bước 7: Kiểm tra kết quả
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BƯỚC 7: Kiểm tra cài đặt" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan

Write-Host ""
Write-Host "Danh sách thư viện đã cài:" -ForegroundColor Gray
pip list

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎉 HOÀN THÀNH!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Bạn có thể chạy các lệnh sau:" -ForegroundColor Yellow
Write-Host "  - python src\tableau_universal_connector.py" -ForegroundColor Cyan
Write-Host "  - python Window_application\bai_1_cua_so_chinh.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Lưu ý: Môi trường ảo đã được kích hoạt!" -ForegroundColor Green
Write-Host "Nếu mở terminal mới, chạy: .\env\Scripts\activate" -ForegroundColor Yellow
Write-Host ""

Read-Host "Nhấn Enter để đóng"
