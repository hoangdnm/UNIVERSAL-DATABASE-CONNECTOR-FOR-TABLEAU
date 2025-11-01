# HƯỚNG DẪN SỬ DỤNG SCRIPT

## � Script chạy ứng dụng: `run_full.sh`

Script **duy nhất** để chạy toàn bộ dự án Tableau Universal Connector.

### 📋 Tính năng

- ✅ Tự động tìm môi trường Python (env/venv/.venv/python3)
- ✅ Kiểm tra và cài đặt thư viện còn thiếu
- ✅ Kiểm tra và dọn port 5002 nếu bị chiếm
- ✅ Chạy Web Server (background) tại `http://127.0.0.1:5002`
- ✅ Chạy Desktop App (Modern UI - Discord style)
- ✅ Tự động dừng Web Server khi đóng Desktop App

---

## 🎯 Cách sử dụng

### Bước 1: Cấp quyền thực thi (chỉ làm 1 lần)
```bash
chmod +x batch_scripts/run_full.sh
```

### Bước 2: Chạy script
```bash
./batch_scripts/run_full.sh
```

### Bước 3: Sử dụng ứng dụng
1. **Desktop App** sẽ tự động mở với giao diện hiện đại
2. **Web Server** chạy ngầm ở `http://127.0.0.1:5002`
3. Sử dụng Desktop App để:
   - Chọn database và bảng
   - Tạo URL kết nối
   - Preview dữ liệu
   - Xem lịch sử

### Bước 4: Dừng ứng dụng
- **Cách 1:** Đóng cửa sổ Desktop App (Web Server tự động dừng)
- **Cách 2:** Nhấn `Ctrl+C` trong terminal

---

## � Chi tiết `run_full.sh`

**Script thực hiện 4 bước:**

#### [1/4] Kiểm tra môi trường Python
- Tự động tìm kiếm: `env/` → `venv/` → `.venv/` → `python3`
- Hiển thị phiên bản Python đang dùng

#### [2/4] Kiểm tra thư viện
- Kiểm tra: `flask`, `customtkinter`, `pyodbc`
- Tự động cài đặt nếu thiếu

#### [3/4] Kiểm tra port 5002
- Kiểm tra port có đang được sử dụng không
- Tự động dừng process cũ nếu có

#### [4/4] Khởi động ứng dụng
- Chạy Web Server (background, PID được lưu)
- Chạy Desktop App (Modern UI)
- Hiển thị thông tin PIDs và URL

**Output mẫu:**
```
============================================================
   TABLEAU UNIVERSAL CONNECTOR - FULL
   Web Server + Desktop App
============================================================

[1/4] Kiểm tra môi trường Python...
✓ Sử dụng môi trường: env/
✓ Python: Python 3.12.3

[2/4] Kiểm tra thư viện...
✓ Thư viện: OK

[3/4] Kiểm tra port 5002...
✓ Port sẵn sàng

[4/4] Khởi động ứng dụng...
→ Web Server (background)...
✓ Web Server đã chạy (PID: 12345)
  URL: http://127.0.0.1:5002

→ Desktop App (Modern UI)...
✓ Desktop App đã chạy (PID: 12346)

============================================================
✓ KHỞI ĐỘNG THÀNH CÔNG!
============================================================

PIDs:
  Web Server: 12345
  Desktop App: 12346

Để dừng:
  - Đóng cửa sổ Desktop App
  - Hoặc nhấn Ctrl+C

Log: /tmp/tableau_web_server.log
============================================================
```

---

## 🎨 Tính năng Modern UI

Desktop App sử dụng **CustomTkinter** với giao diện Discord/Teams style:

### 📱 Các trang chính:
- 🏠 **Trang chủ**: Hiển thị thống kê (databases, tables, connections)
- 🔌 **Kết nối**: Chọn database, bảng, tạo URL
- 👁️ **Preview**: Xem trước dữ liệu bảng (100 dòng đầu)
- 📜 **Lịch sử**: Xem/Xóa/Xuất lịch sử kết nối
- ⚙️ **Cài đặt**: Cấu hình ứng dụng

### 🎯 Các chức năng:
- ✅ Kết nối SQL Server (Windows Authentication)
- ✅ Tạo URL cho Tableau Web Data Connector
- ✅ Preview dữ liệu với Treeview
- ✅ Xóa toàn bộ lịch sử
- ✅ Xuất lịch sử ra JSON
- ✅ Xuất danh sách bảng (TXT/JSON/CSV)
- ✅ Chuyển đổi Dark/Light theme
- ✅ Mở file config JSON

---

## 🔧 Khắc phục sự cố

### ❌ Lỗi: "Permission denied"
```bash
chmod +x batch_scripts/run_full.sh
```

### ❌ Lỗi: "Python không tìm thấy"
```bash
# Cài đặt Python 3
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python3                   # Mac

# Tạo môi trường ảo
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### ❌ Lỗi: "Port 5002 đang được sử dụng"
Script tự động dọn port, nhưng nếu vẫn lỗi:
```bash
# Tìm và dừng process thủ công
lsof -ti:5002 | xargs kill -9
```

### ❌ Lỗi: SQL Server driver không tìm thấy
**Bình thường!** Ứng dụng sẽ tự động:
- Chuyển sang **chế độ Demo**
- Vẫn chạy đầy đủ tất cả tính năng
- Sử dụng dữ liệu mẫu để test

Để cài driver SQL Server thật:
```bash
# Xem hướng dẫn chi tiết
cat docs/HUONG_DAN_CAI_DAT_SQL_SERVER.md
```

### ❌ Desktop App không hiển thị
Kiểm tra CustomTkinter:
```bash
# Cài đặt lại
source env/bin/activate
pip install --upgrade customtkinter
```

---

## 📝 Lưu ý quan trọng

1. **Môi trường ảo** (khuyến nghị):
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt
   ```

2. **Port 5002**: Đảm bảo không bị chiếm dụng

3. **Quyền thực thi**: `chmod +x` cho file .sh

4. **Log file**: Xem chi tiết tại `/tmp/tableau_web_server.log`

---

## 📂 Cấu trúc thư mục

```
UNIVERSAL-DATABASE-CONNECTOR-FOR-TABLEAU/
├── batch_scripts/
│   ├── run_full.sh          ← Script chạy ứng dụng
│   └── README.md            ← File này
├── src/
│   ├── tableau_universal_connector.py   ← Web Server
│   └── database_connector.py            ← Database module
├── Window_application/
│   ├── modern_ui.py         ← Modern UI (Discord style)
│   ├── modern_components.py ← UI components
│   └── desktop_app.py       ← Desktop cổ điển
├── config/
│   └── database_config.json ← Cấu hình database
└── requirements.txt         ← Thư viện cần thiết
```

---

## 🚀 Quick Start

```bash
# 1. Clone hoặc tải project về
cd /media/hoangdao/D/UNIVERSAL-DATABASE-CONNECTOR-FOR-TABLEAU

# 2. Cấp quyền thực thi
chmod +x batch_scripts/run_full.sh

# 3. Chạy ngay
./batch_scripts/run_full.sh

# 4. Sử dụng Desktop App và Web Server!
```

---

## 📞 Hỗ trợ

- 📖 **Tài liệu đầy đủ**: `docs/`
- 📝 **Log file**: `/tmp/tableau_web_server.log`
- 🔧 **Config**: `config/database_config.json`
- 📜 **Lịch sử**: `connection_history.json`
