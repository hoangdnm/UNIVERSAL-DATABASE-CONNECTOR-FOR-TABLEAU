# 🗄️ HƯỚNG DẪN CÀI ĐẶT VÀ CẤU HÌNH SQL SERVER

## 📋 MỤC LỤC
1. [Kiểm tra SQL Server đã cài chưa](#1-kiểm-tra-sql-server-đã-cài-chưa)
2. [Cài đặt SQL Server](#2-cài-đặt-sql-server)
3. [Cấu hình SQL Server](#3-cấu-hình-sql-server)
4. [Kiểm tra kết nối](#4-kiểm-tra-kết-nối)
5. [Khắc phục lỗi thường gặp](#5-khắc-phục-lỗi-thường-gặp)

---

## 1. Kiểm tra SQL Server đã cài chưa

### Cách 1: Kiểm tra Services
1. Nhấn `Win + R`
2. Gõ `services.msc` và nhấn Enter
3. Tìm các service có tên bắt đầu bằng `SQL Server`
   - ✅ Nếu thấy: SQL Server đã được cài
   - ❌ Nếu không thấy: Cần cài SQL Server

### Cách 2: Kiểm tra bằng lệnh
```bash
# Mở Command Prompt hoặc PowerShell
sc query MSSQLSERVER
```

**Kết quả:**
- ✅ `STATE: RUNNING` → SQL Server đang chạy
- ⚠️ `STATE: STOPPED` → SQL Server đã cài nhưng chưa chạy
- ❌ `Lỗi` → SQL Server chưa được cài

---

## 2. Cài đặt SQL Server

### Option 1: SQL Server Express (MIỄN PHÍ - Khuyến nghị cho học tập)

#### Bước 1: Tải về
1. Truy cập: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
2. Chọn **SQL Server 2022 Express** (hoặc phiên bản mới nhất)
3. Tải file cài đặt (khoảng 50MB)

#### Bước 2: Cài đặt
1. Chạy file vừa tải về
2. Chọn **Basic** (Cơ bản)
3. Chấp nhận License Terms
4. Chọn nơi cài đặt (để mặc định)
5. Đợi quá trình cài đặt hoàn tất (5-10 phút)

#### Bước 3: Cài SQL Server Management Studio (SSMS)
1. Sau khi cài xong SQL Server, click vào **Install SSMS**
2. Hoặc tải từ: https://aka.ms/ssmsfullsetup
3. Cài đặt SSMS (dùng để quản lý database)

### Option 2: SQL Server Developer (MIỄN PHÍ - Đầy đủ tính năng)

1. Tải về: https://www.microsoft.com/en-us/sql-server/sql-server-downloads
2. Chọn **Developer Edition**
3. Làm theo các bước tương tự như Express

---

## 3. Cấu hình SQL Server

### 3.1. Khởi động SQL Server Service

#### Cách 1: Qua Services Manager
1. Nhấn `Win + R` → gõ `services.msc`
2. Tìm `SQL Server (MSSQLSERVER)`
3. Chuột phải → **Start**
4. Đặt **Startup Type** = **Automatic**

#### Cách 2: Qua Command
```bash
# Mở Command Prompt với quyền Administrator
net start MSSQLSERVER
```

### 3.2. Bật SQL Server Authentication

#### Bước 1: Mở SQL Server Management Studio (SSMS)
1. Tìm **Microsoft SQL Server Management Studio** trong Start Menu
2. Cửa sổ Connect:
   - Server name: `localhost` hoặc `.` hoặc `(local)`
   - Authentication: **Windows Authentication**
   - Click **Connect**

#### Bước 2: Enable Mixed Mode Authentication
1. Chuột phải vào **Server name** (ở Object Explorer)
2. Chọn **Properties**
3. Chọn **Security** (bên trái)
4. Chọn **SQL Server and Windows Authentication mode**
5. Click **OK**

#### Bước 3: Restart SQL Server
```bash
# Mở Command Prompt với quyền Administrator
net stop MSSQLSERVER
net start MSSQLSERVER
```

### 3.3. Cấu hình tài khoản SA

#### Bước 1: Enable tài khoản SA
1. Trong SSMS, mở **Security** → **Logins**
2. Chuột phái vào **sa** → **Properties**
3. Tab **General**:
   - Đặt password mới (ví dụ: `YourStrong!Pass123`)
   - **✅ Ghi nhớ password này!**
4. Tab **Status**:
   - Login: **Enabled**
5. Click **OK**

#### Bước 2: Test đăng nhập
1. Ngắt kết nối SSMS (File → Disconnect)
2. Connect lại với:
   - Server name: `localhost`
   - Authentication: **SQL Server Authentication**
   - Login: `sa`
   - Password: `YourStrong!Pass123` (password bạn vừa đặt)

### 3.4. Bật TCP/IP Protocol

#### Bước 1: Mở SQL Server Configuration Manager
- Tìm **SQL Server Configuration Manager** trong Start Menu
- Hoặc gõ: `SQLServerManager16.msc` (16 là version, có thể khác)

#### Bước 2: Enable TCP/IP
1. Mở **SQL Server Network Configuration**
2. Chọn **Protocols for MSSQLSERVER**
3. Chuột phải vào **TCP/IP** → **Enable**
4. Chuột phải vào **TCP/IP** → **Properties**

#### Bước 3: Cấu hình Port
1. Tab **IP Addresses**
2. Kéo xuống **IPALL**
3. Đặt:
   - **TCP Dynamic Ports**: để trống
   - **TCP Port**: `1433`
4. Click **OK**

#### Bước 4: Restart SQL Server
1. Trong Configuration Manager
2. Chọn **SQL Server Services**
3. Chuột phải **SQL Server (MSSQLSERVER)** → **Restart**

### 3.5. Cấu hình Firewall (nếu cần)

```bash
# Mở Command Prompt với quyền Administrator
netsh advfirewall firewall add rule name="SQL Server" dir=in action=allow protocol=TCP localport=1433
```

---

## 4. Kiểm tra kết nối

### 4.1. Kiểm tra Port đã mở chưa

```bash
# Mở Command Prompt
netstat -an | findstr 1433
```

**Kết quả mong đợi:**
```
TCP    0.0.0.0:1433           0.0.0.0:0              LISTENING
TCP    [::]:1433              [::]:0                 LISTENING
```

### 4.2. Test kết nối qua SSMS

1. Mở SSMS
2. Server name: `127.0.0.1,1433` hoặc `localhost,1433`
3. Authentication: **SQL Server Authentication**
4. Login: `sa`
5. Password: `YourStrong!Pass123`
6. Click **Connect**

### 4.3. Test kết nối qua Python Script

```bash
# Chạy script dò tìm cấu hình
python scripts/do_cau_hinh_sql_server.py

# Hoặc kiểm tra kết nối
python scripts/kiem_tra_ket_noi_sql.py
```

### 4.4. Cấu hình file config

Nếu kết nối thành công, tạo/sửa file `config/database_config.json`:

```json
{
  "server": "127.0.0.1",
  "port": 1433,
  "user": "sa",
  "password": "YourStrong!Pass123",
  "database": "master"
}
```

**⚠️ LƯU Ý:** Thay `YourStrong!Pass123` bằng password thực tế của bạn!

---

## 5. Khắc phục lỗi thường gặp

### Lỗi 1: "SQL Server service is not running"

**Nguyên nhân:** Service chưa chạy

**Khắc phục:**
```bash
net start MSSQLSERVER
```

### Lỗi 2: "Login failed for user 'sa'"

**Nguyên nhân:** 
- Password sai
- Tài khoản SA chưa enable
- Chưa bật SQL Server Authentication

**Khắc phục:**
1. Đăng nhập bằng Windows Authentication
2. Enable tài khoản SA (xem mục 3.3)
3. Enable Mixed Mode (xem mục 3.2)
4. Restart SQL Server

### Lỗi 3: "Cannot connect to server"

**Nguyên nhân:**
- TCP/IP chưa bật
- Port chưa đúng
- Firewall chặn

**Khắc phục:**
1. Bật TCP/IP (xem mục 3.4)
2. Kiểm tra port (mục 4.1)
3. Cấu hình Firewall (mục 3.5)

### Lỗi 4: "Port 1433 is already in use"

**Nguyên nhân:** Port bị chiếm bởi ứng dụng khác

**Khắc phục:**

#### Option 1: Tìm và tắt ứng dụng đang dùng port
```bash
netstat -ano | findstr :1433
# Ghi nhớ PID (cột cuối)
taskkill /PID <PID> /F
```

#### Option 2: Đổi port SQL Server
1. Mở SQL Server Configuration Manager
2. TCP/IP Properties → IP Addresses → IPALL
3. Đổi TCP Port sang `1435` hoặc `1533`
4. Restart SQL Server
5. Cập nhật `config/database_config.json`

### Lỗi 5: "SQL Server không có trong Services"

**Nguyên nhân:** SQL Server chưa được cài đặt

**Khắc phục:** Quay lại [Mục 2: Cài đặt SQL Server](#2-cài-đặt-sql-server)

---

## 6. Tạo Database mẫu để test

Sau khi kết nối thành công:

```bash
# Tạo database mẫu
python scripts/khoi_tao_database.py

# Hoặc tạo bằng SSMS:
# 1. Mở SSMS
# 2. Chuột phải Databases → New Database
# 3. Tên: TestDB
# 4. Click OK
```

---

## 7. Chạy Universal Connector

```bash
# Chạy connector
python src/tableau_universal_connector.py

# Mở trình duyệt
http://127.0.0.1:5002
```

---

## 📞 Hỗ trợ thêm

Nếu vẫn gặp vấn đề:

1. **Kiểm tra log lỗi:**
   ```bash
   # Log SQL Server thường ở:
   C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\Log\ERRORLOG
   ```

2. **Chạy script chẩn đoán:**
   ```bash
   python scripts/do_cau_hinh_sql_server.py
   ```

3. **Đọc tài liệu:**
   - `docs/README.md`
   - `docs/HUONG_DAN_SCRIPTS.md`

---

## ✅ Checklist hoàn thành

- [ ] SQL Server đã cài đặt
- [ ] SQL Server service đang chạy
- [ ] TCP/IP đã enable
- [ ] Port 1433 đang listen
- [ ] Tài khoản SA đã enable và có password
- [ ] Mixed Mode Authentication đã bật
- [ ] Kết nối qua SSMS thành công
- [ ] File `config/database_config.json` đã cấu hình đúng
- [ ] Script Python kết nối thành công
- [ ] Đã tạo database mẫu
- [ ] Universal Connector chạy được

---

**🎓 Dự án tốt nghiệp - Tableau Universal Database Connector**

**Chúc bạn thành công! 🚀**
