# 🚀 BATCH SCRIPTS - Universal Connector

## 📁 Các file .bat trong thư mục này

### ⭐ **start_simple.bat** (KHUYẾN NGHỊ)
```bash
# Cách chạy nhanh nhất:
batch_scripts\start_simple.bat
```
- ✅ Đơn giản, nhanh chóng
- ✅ Tự động activate virtual environment  
- ✅ Kiểm tra và cài đặt thư viện nếu thiếu
- ✅ Khởi động Universal Connector

### 🔧 **chay_universal_connector.bat** 
```bash
# Cách chạy đầy đủ:
batch_scripts\chay_universal_connector.bat
```
- ✅ Kiểm tra toàn diện hệ thống
- ✅ Kiểm tra SQL Server connection
- ✅ Detailed error handling
- ✅ Thông báo chi tiết hơn

### 🔍 **kiem_tra_moi_truong.bat**
```bash
# Kiểm tra môi trường:
batch_scripts\kiem_tra_moi_truong.bat
```
- ✅ Kiểm tra Docker và SQL Server
- ✅ Kiểm tra Python và thư viện
- ✅ Chẩn đoán vấn đề
- ✅ Không chạy server (chỉ kiểm tra)

---

## 🎯 **QUICK START**

### Cho người mới bắt đầu:
```bash
# 1. Double-click file này:
batch_scripts\start_simple.bat

# 2. Mở trình duyệt: http://127.0.0.1:5002
```

### Khi gặp vấn đề:
```bash
# 1. Chạy script kiểm tra:
batch_scripts\kiem_tra_moi_truong.bat

# 2. Sửa vấn đề theo hướng dẫn
# 3. Chạy lại start_simple.bat
```

---

## 💡 **TIPS**

- **File nào chạy nhanh nhất?** → `start_simple.bat`
- **Debug khi có lỗi?** → `kiem_tra_moi_truong.bat`  
- **Cần kiểm tra đầy đủ?** → `chay_universal_connector.bat`

---

## 🌐 **Sau khi chạy thành công:**

1. **Mở trình duyệt:** http://127.0.0.1:5002
2. **Chọn database** từ dropdown
3. **Chọn bảng** dữ liệu
4. **Kết nối với Tableau Desktop**

**URL cho Tableau:** `http://127.0.0.1:5002`
