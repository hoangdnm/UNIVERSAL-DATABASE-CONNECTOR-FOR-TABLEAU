# 📋 HƯỚNG DẪN SỬ DỤNG CÁC SCRIPTS

## 🚀 **CHẠY UNIVERSAL CONNECTOR**

### 1. Cách nhanh nhất (Khuyến nghị)
```bash
# Double-click file này:
batch_scripts\start_simple.bat
```

### 2. Cách đầy đủ
```bash
# Double-click file này:
batch_scripts\chay_universal_connector.bat
```

### 3. Kiểm tra môi trường
```bash
# Double-click file này:
batch_scripts\kiem_tra_moi_truong.bat
```

---

## 🔧 **SCRIPTS TIỆN ÍCH**

### 📁 Trong thư mục `scripts/`

| Script | Mục đích | Cách chạy |
|--------|----------|-----------|
| `test_env.bat` | Kiểm tra virtual environment | Double-click |
| `kiem_tra_ket_noi_sql.py` | Kiểm tra kết nối SQL Server | `python scripts/kiem_tra_ket_noi_sql.py` |
| `tao_database_test.py` | Tạo database test nhanh | `python scripts/tao_database_test.py` |
| `cau_hinh_database.py` | Cấu hình database connection | `python scripts/cau_hinh_database.py` |
| `khoi_tao_database.py` | Khởi tạo database với dữ liệu | `python scripts/khoi_tao_database.py` |
| `demo_universal.py` | Demo Universal Connector | `python scripts/demo_universal.py` |
| `tao_du_lieu_1k.py` | Tạo 1000 dòng dữ liệu test | `python scripts/tao_du_lieu_1k.py` |
| `tao_bao_cao_tong_ket.py` | Tạo báo cáo tổng kết | `python scripts/tao_bao_cao_tong_ket.py` |

### 📁 Trong thư mục `tests/`

| Test Script | Mục đích | Cách chạy |
|-------------|----------|-----------|
| `demo_hoan_chinh.py` | Demo toàn bộ hệ thống | `python tests/demo_hoan_chinh.py` |
| `kiem_thu_universal.py` | Test Universal Connector | `python tests/kiem_thu_universal.py` |
| `kiem_thu_du_an.py` | Test toàn bộ dự án | `python tests/kiem_thu_du_an.py` |
| `test_hieu_suat_1k.py` | Test hiệu suất 1000 dòng | `python tests/test_hieu_suat_1k.py` |
| `test_hieu_suat_toan_dien.py` | Test hiệu suất toàn diện | `python tests/test_hieu_suat_toan_dien.py` |

---

## 🔥 **QUICK START - 3 BƯỚC**

### Bước 1: Khởi động SQL Server
```bash
docker ps                    # Kiểm tra SQL Server đang chạy
# Nếu không chạy:
docker-compose up -d
```

### Bước 2: Chạy Universal Connector
```bash
# Double-click:
batch_scripts\start_simple.bat
```

### Bước 3: Kết nối Tableau
1. Mở **Tableau Desktop**
2. Chọn **Web Data Connector**
3. Nhập URL: `http://127.0.0.1:5002`
4. Chọn database và bảng
5. Kết nối!

---

## 🆘 **KHI GẶP VẤNĐỀ**

### ❌ Không kết nối được SQL Server
```bash
# Chạy script debug:
python scripts/kiem_tra_ket_noi_sql.py

# Hoặc test virtual environment:
scripts/test_env.bat
```

### ❌ Thiếu thư viện Python
```bash
# Activate virtual environment và cài đặt:
env\Scripts\activate
pip install -r config/requirements.txt
```

### ❌ Không có database
```bash
# Tạo database test nhanh:
python scripts/tao_database_test.py
```

---

## 💡 **TIPS HỮU ÍCH**

- **File .bat nào tốt nhất?** → `batch_scripts\start_simple.bat` (nhanh, đơn giản)
- **Test nhanh kết nối?** → `scripts\test_env.bat`
- **Tạo dữ liệu test?** → `python scripts\tao_database_test.py`
- **Debug toàn diện?** → `python scripts\kiem_tra_ket_noi_sql.py`

---

**🎯 Lưu ý:** Tất cả scripts đều có thể chạy từ thư mục gốc `test_ind/`
