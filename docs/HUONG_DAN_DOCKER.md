# 🐳 HƯỚNG DẪN SỬ DỤNG SQL SERVER VỚI DOCKER

## 📋 Thông tin Docker

File cấu hình: `config/docker-compose.yml`

### Thông số kết nối:
- **Server**: `127.0.0.1` (localhost)
- **Port**: `1235` (mapping từ container port 1433)
- **User**: `sa`
- **Password**: `YourStrong!Pass123`
- **Database**: `master` (mặc định)

---

## 🚀 Khởi động SQL Server

### Bước 1: Cài đặt Docker
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Khởi động Docker
sudo systemctl start docker
sudo systemctl enable docker

# Thêm user vào group docker (không cần sudo)
sudo usermod -aG docker $USER
newgrp docker
```

### Bước 2: Chạy SQL Server
```bash
cd config/
docker-compose up -d
```

### Bước 3: Kiểm tra container
```bash
# Xem container đang chạy
docker ps

# Xem log
docker logs mssql_server

# Kiểm tra kết nối
docker exec -it mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Pass123'
```

---

## 🛑 Dừng và xóa SQL Server

### Dừng container
```bash
cd config/
docker-compose stop
```

### Xóa container (giữ data)
```bash
docker-compose down
```

### Xóa container và data
```bash
docker-compose down -v
```

---

## 🔧 Các lệnh Docker hữu ích

### Xem trạng thái
```bash
# Xem tất cả container
docker ps -a

# Xem log realtime
docker logs -f mssql_server

# Xem resource usage
docker stats mssql_server
```

### Vào container
```bash
# Vào bash
docker exec -it mssql_server bash

# Chạy sqlcmd
docker exec -it mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Pass123'
```

### Backup/Restore
```bash
# Backup database
docker exec mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Pass123' -Q "BACKUP DATABASE [YourDB] TO DISK='/var/opt/mssql/backup/YourDB.bak'"

# Copy backup ra ngoài
docker cp mssql_server:/var/opt/mssql/backup/YourDB.bak ./

# Copy backup vào container
docker cp ./YourDB.bak mssql_server:/var/opt/mssql/backup/

# Restore
docker exec mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Pass123' -Q "RESTORE DATABASE [YourDB] FROM DISK='/var/opt/mssql/backup/YourDB.bak'"
```

---

## 📝 Cấu hình ứng dụng

### File: `config/database_config.json`
```json
{
  "server": "127.0.0.1",
  "port": 1235,
  "user": "sa",
  "password": "YourStrong!Pass123",
  "database": "master",
  "windows_auth": false
}
```

**Lưu ý:**
- Port `1235` là port trên máy host
- Container SQL Server dùng port `1433` bên trong
- Mapping: `1235:1433`

---

## 🧪 Kiểm tra kết nối

### Python script
```bash
# Kiểm tra database hiện có
python tests/kiem_tra_database.py

# Tạo 3 database mẫu với 500 dòng mỗi bảng
python tests/tao_3_database_500_dong.py
```

### sqlcmd trong container
```bash
docker exec -it mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Pass123'
```

Sau đó chạy query:
```sql
SELECT name FROM sys.databases;
GO

USE master;
GO

SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES;
GO
```

---

## 🔒 Bảo mật

### Đổi password SA
```bash
docker exec -it mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Pass123' -Q "ALTER LOGIN sa WITH PASSWORD = 'NewPassword123!'"
```

Sau khi đổi, cập nhật file `config/database_config.json`

### Tạo user mới
```sql
-- Tạo login
CREATE LOGIN myuser WITH PASSWORD = 'MyPass123!';
GO

-- Tạo user trong database
USE master;
CREATE USER myuser FOR LOGIN myuser;
GO

-- Cấp quyền
ALTER ROLE db_datareader ADD MEMBER myuser;
ALTER ROLE db_datawriter ADD MEMBER myuser;
GO
```

---

## ❓ Khắc phục sự cố

### Lỗi: Port 1235 đã được sử dụng
```bash
# Kiểm tra process đang dùng port
lsof -i:1235

# Đổi port trong docker-compose.yml
# Ví dụ: "1236:1433"
```

### Lỗi: Container không khởi động
```bash
# Xem log chi tiết
docker logs mssql_server

# Xóa và tạo lại
docker-compose down -v
docker-compose up -d
```

### Lỗi: Không kết nối được từ Python
```bash
# Kiểm tra container đang chạy
docker ps | grep mssql

# Kiểm tra port mapping
docker port mssql_server

# Kiểm tra firewall
sudo ufw allow 1235/tcp

# Test kết nối
telnet 127.0.0.1 1235
```

### Lỗi: Password không đúng
```bash
# Reset password SA
docker exec -it mssql_server /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P 'YourStrong!Pass123' -Q "ALTER LOGIN sa WITH PASSWORD = 'YourStrong!Pass123'"
```

---

## 📊 Dữ liệu mẫu

### Tạo database và bảng test
```bash
# Chạy script tạo 3 database với 500 dòng/bảng
python tests/tao_3_database_500_dong.py
```

Script sẽ tạo:
1. **SalesDB** - 5 bảng về bán hàng
2. **InventoryDB** - 4 bảng về kho
3. **EmployeeDB** - 5 bảng về nhân viên

Mỗi bảng có ~500 dòng dữ liệu ngẫu nhiên

---

## 🎯 Quick Start

```bash
# 1. Khởi động SQL Server
cd config/
docker-compose up -d

# 2. Đợi 10 giây để SQL Server khởi động
sleep 10

# 3. Tạo dữ liệu mẫu
cd ..
python tests/tao_3_database_500_dong.py

# 4. Chạy ứng dụng
./run.sh
```

Xong! Giờ có thể sử dụng ứng dụng với SQL Server trong Docker 🎉
