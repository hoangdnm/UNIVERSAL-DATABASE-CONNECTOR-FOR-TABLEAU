# 🚀 HƯỚNG DẪN CHẠY DỰ ÁN NHANH

## 📦 Cài đặt Dependencies trước khi chạy

**QUAN TRỌNG**: Cài đặt tất cả thư viện cần thiết trước:

```bash
# Linux/Mac
cd /đường/dẫn/đến/dự/án
pip install -r requirements.txt

# Hoặc với môi trường ảo
./env/bin/pip install -r requirements.txt
```

```cmd
# Windows
cd C:\đường\dẫn\đến\dự\án
pip install -r requirements.txt

# Hoặc với môi trường ảo
env\Scripts\pip install -r requirements.txt
```

**File `requirements.txt` đã gộp tất cả thư viện cần thiết:**
- Flask (Web Server)
- pymssql, pyodbc (Database connectors)
- Pillow (Desktop GUI)
- requests, Werkzeug

---

## ✨ Tính năng của Script

Script **tự động** thực hiện các công việc sau:
- ✅ Tự động phát hiện môi trường Python (env, venv, .venv hoặc hệ thống)
- ✅ Cho phép **chọn** môi trường nếu có nhiều môi trường
- ✅ Kiểm tra các file dự án có đầy đủ không
- ✅ Tự động dọn dẹp port 5002 nếu đang bị chiếm
- ✅ Khởi động Web Server trong background
- ✅ Khởi động Desktop App
- ✅ Tự động dừng Web Server khi đóng Desktop App

## 🖥️ Cách sử dụng trên Linux/Mac

### Cách 1: Chạy trực tiếp
```bash
cd /đường/dẫn/đến/dự/án
./batch_scripts/chay_du_an_hoan_chinh.sh
```

### Cách 2: Chạy từ thư mục batch_scripts
```bash
cd batch_scripts
./chay_du_an_hoan_chinh.sh
```

### Lỗi "Permission denied"?
```bash
chmod +x batch_scripts/chay_du_an_hoan_chinh.sh
./batch_scripts/chay_du_an_hoan_chinh.sh
```

## 🪟 Cách sử dụng trên Windows

### Cách 1: Double-click
- Mở thư mục `batch_scripts`
- Double-click vào file `chay_du_an_hoan_chinh.bat`

### Cách 2: Chạy từ Command Prompt
```cmd
cd C:\đường\dẫn\đến\dự\án
batch_scripts\chay_du_an_hoan_chinh.bat
```

### Cách 3: Chạy từ PowerShell
```powershell
cd C:\đường\dẫn\đến\dự\án
.\batch_scripts\chay_du_an_hoan_chinh.bat
```

## 📋 Quy trình hoạt động

```
┌─────────────────────────────────────┐
│ 1. Phát hiện môi trường Python      │
│    - Tìm env, venv, .venv           │
│    - Cho phép chọn nếu có nhiều     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 2. Kiểm tra Python & các file       │
│    - Kiểm tra phiên bản Python      │
│    - Kiểm tra file Web Server       │
│    - Kiểm tra file Desktop App      │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 3. Kiểm tra & dọn dẹp port 5002     │
│    - Dừng process cũ nếu đang chạy  │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 4. Khởi động Web Server             │
│    - Chạy background trên port 5002 │
│    - Log: /tmp/tableau_web_server   │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ 5. Khởi động Desktop App            │
│    - Giao diện chọn database/bảng   │
│    - Tạo URL kết nối Tableau        │
└─────────────────────────────────────┘
```

## 📝 Khi chọn môi trường

Nếu có nhiều môi trường Python, script sẽ hiển thị danh sách:

```
Tìm thấy 3 môi trường:
  [1] env (Thư mục gốc)
  [2] venv (Thư mục gốc)
  [3] Python3 hệ thống

Chọn môi trường (1-3): _
```

Bạn chỉ cần nhập số (1, 2 hoặc 3) và nhấn Enter.

## 🎯 Ưu điểm

### ✅ Trước đây (phải chạy 2 lần):
```bash
# Terminal 1
./env/bin/python src/tableau_universal_connector.py

# Terminal 2 (phải mở terminal mới)
./env/bin/python Window_application/bai_5_hoan_chinh.py
```
❌ Mất thời gian  
❌ Dễ quên chạy Web Server  
❌ Phải quản lý 2 terminal  

### ✅ Bây giờ (chỉ 1 lần):
```bash
./batch_scripts/chay_du_an_hoan_chinh.sh
```
✅ 1 lệnh duy nhất  
✅ Tự động chọn môi trường  
✅ Tự động dọn dẹp  
✅ Tự động khởi động cả 2  

## 🛠️ Xử lý lỗi

### Lỗi: "Không tìm thấy môi trường Python"
**Giải pháp:**
```bash
# Tạo môi trường ảo mới
python3 -m venv env

# Hoặc cài đặt Python3
sudo apt install python3  # Linux
brew install python3       # Mac
```

### Lỗi: "Port 5002 đang được sử dụng"
**Giải pháp:** Script tự động xử lý! Nó sẽ dừng process cũ và khởi động lại.

### Lỗi: "Không tìm thấy file dự án"
**Giải pháp:** Đảm bảo bạn đang ở đúng thư mục dự án hoặc file không bị di chuyển.

## 📂 Cấu trúc thư mục

```
UNIVERSAL-DATABASE-CONNECTOR-FOR-TABLEAU/
├── batch_scripts/
│   ├── chay_du_an_hoan_chinh.sh     ← Script Linux/Mac
│   ├── chay_du_an_hoan_chinh.bat    ← Script Windows
│   └── README_SCRIPTS.md            ← File này
├── src/
│   └── tableau_universal_connector.py
├── Window_application/
│   └── bai_5_hoan_chinh.py
└── env/                              ← Môi trường ảo
```

## 🌍 Chạy được trên máy khác

Script được thiết kế để **tự động phát hiện** môi trường:
- ✅ Không hardcode đường dẫn cố định
- ✅ Tự động tìm thư mục gốc của dự án
- ✅ Tự động phát hiện Python trong env/venv/.venv
- ✅ Fallback sang Python hệ thống nếu không có env

**Điều kiện:** Máy khác cần có:
- Python 3.x (hoặc môi trường ảo đã setup)
- Các thư viện đã cài (Flask, pymssql, tkinter, pillow...)

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra log: `/tmp/tableau_web_server.log` (Linux) hoặc `%TEMP%\tableau_web_server.log` (Windows)
2. Chạy thủ công từng file để xác định lỗi:
   ```bash
   ./env/bin/python src/tableau_universal_connector.py
   ./env/bin/python Window_application/bai_5_hoan_chinh.py
   ```

## 🎉 Sử dụng

Giờ bạn chỉ cần **1 lệnh duy nhất** để chạy toàn bộ dự án! 🚀
