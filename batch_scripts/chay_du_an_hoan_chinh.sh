#!/bin/bash

##############################################
# SCRIPT CHẠY DỰ ÁN HOÀN CHỈNH
# Tự động khởi động Web Server và Desktop App
##############################################

# Màu sắc cho output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Lấy thư mục gốc của dự án (thư mục cha của batch_scripts)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  TABLEAU UNIVERSAL CONNECTOR${NC}"
echo -e "${BLUE}  Script Khởi Động Tự Động${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Kiểm tra thư mục env
echo -e "${YELLOW}[1/5] Kiểm tra môi trường Python...${NC}"

# Tìm kiếm các môi trường ảo có thể có
POSSIBLE_ENVS=()
ENV_PATHS=()

# Kiểm tra env trong thư mục gốc
if [ -d "$PROJECT_DIR/env" ]; then
    POSSIBLE_ENVS+=("env (Thư mục gốc)")
    ENV_PATHS+=("$PROJECT_DIR/env")
fi

if [ -d "$PROJECT_DIR/venv" ]; then
    POSSIBLE_ENVS+=("venv (Thư mục gốc)")
    ENV_PATHS+=("$PROJECT_DIR/venv")
fi

if [ -d "$PROJECT_DIR/.venv" ]; then
    POSSIBLE_ENVS+=(".venv (Thư mục gốc)")
    ENV_PATHS+=("$PROJECT_DIR/.venv")
fi

# Kiểm tra Python hệ thống
if command -v python3 &> /dev/null; then
    POSSIBLE_ENVS+=("Python3 hệ thống")
    ENV_PATHS+=("system")
fi

# Nếu không tìm thấy môi trường nào
if [ ${#POSSIBLE_ENVS[@]} -eq 0 ]; then
    echo -e "${RED}✗ Không tìm thấy môi trường Python nào!${NC}"
    echo -e "${YELLOW}Vui lòng cài đặt Python3 hoặc tạo môi trường ảo.${NC}"
    exit 1
fi

# Hiển thị danh sách môi trường
echo -e "${GREEN}Tìm thấy ${#POSSIBLE_ENVS[@]} môi trường:${NC}"
for i in "${!POSSIBLE_ENVS[@]}"; do
    echo -e "  ${BLUE}[$((i+1))]${NC} ${POSSIBLE_ENVS[$i]}"
done
echo ""

# Cho phép người dùng chọn
if [ ${#POSSIBLE_ENVS[@]} -eq 1 ]; then
    echo -e "${GREEN}Tự động chọn: ${POSSIBLE_ENVS[0]}${NC}"
    SELECTED_INDEX=0
else
    read -p "Chọn môi trường (1-${#POSSIBLE_ENVS[@]}): " CHOICE
    SELECTED_INDEX=$((CHOICE-1))
    
    # Kiểm tra lựa chọn hợp lệ
    if [ $SELECTED_INDEX -lt 0 ] || [ $SELECTED_INDEX -ge ${#POSSIBLE_ENVS[@]} ]; then
        echo -e "${RED}✗ Lựa chọn không hợp lệ!${NC}"
        exit 1
    fi
fi

SELECTED_ENV="${ENV_PATHS[$SELECTED_INDEX]}"
echo -e "${GREEN}✓ Đã chọn: ${POSSIBLE_ENVS[$SELECTED_INDEX]}${NC}"
echo ""

# Xác định lệnh Python
if [ "$SELECTED_ENV" = "system" ]; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="$SELECTED_ENV/bin/python"
    
    # Kiểm tra file python có tồn tại không
    if [ ! -f "$PYTHON_CMD" ]; then
        echo -e "${RED}✗ Không tìm thấy Python trong môi trường ảo!${NC}"
        echo -e "${YELLOW}Đường dẫn: $PYTHON_CMD${NC}"
        exit 1
    fi
fi

# Kiểm tra Python hoạt động
echo -e "${YELLOW}[2/5] Kiểm tra Python...${NC}"
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Không thể chạy Python!${NC}"
    exit 1
fi
echo ""

# Kiểm tra các file cần thiết
echo -e "${YELLOW}[3/5] Kiểm tra các file dự án...${NC}"

WEB_SERVER="$PROJECT_DIR/src/tableau_universal_connector.py"
DESKTOP_APP="$PROJECT_DIR/Window_application/bai_5_hoan_chinh.py"

if [ ! -f "$WEB_SERVER" ]; then
    echo -e "${RED}✗ Không tìm thấy: $WEB_SERVER${NC}"
    exit 1
fi

if [ ! -f "$DESKTOP_APP" ]; then
    echo -e "${RED}✗ Không tìm thấy: $DESKTOP_APP${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Web Server: src/tableau_universal_connector.py${NC}"
echo -e "${GREEN}✓ Desktop App: Window_application/bai_5_hoan_chinh.py${NC}"
echo ""

# Kiểm tra port 5002 có đang được sử dụng không
echo -e "${YELLOW}[4/5] Kiểm tra port 5002...${NC}"
if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠ Port 5002 đang được sử dụng. Dừng process cũ...${NC}"
    PID=$(lsof -ti:5002)
    kill -9 $PID 2>/dev/null
    sleep 1
    echo -e "${GREEN}✓ Đã dừng process cũ${NC}"
else
    echo -e "${GREEN}✓ Port 5002 sẵn sàng${NC}"
fi
echo ""

# Khởi động Web Server trong background
echo -e "${YELLOW}[5/5] Khởi động ứng dụng...${NC}"
echo -e "${BLUE}→ Khởi động Web Server (port 5002)...${NC}"

cd "$PROJECT_DIR"
$PYTHON_CMD "$WEB_SERVER" > /tmp/tableau_web_server.log 2>&1 &
WEB_SERVER_PID=$!

# Đợi web server khởi động
echo -e "${YELLOW}  Đợi Web Server khởi động...${NC}"
sleep 3

# Kiểm tra web server có chạy không
if ps -p $WEB_SERVER_PID > /dev/null; then
    echo -e "${GREEN}✓ Web Server đã khởi động (PID: $WEB_SERVER_PID)${NC}"
    echo -e "${GREEN}  URL: http://127.0.0.1:5002${NC}"
else
    echo -e "${RED}✗ Web Server không khởi động được!${NC}"
    echo -e "${YELLOW}Xem log tại: /tmp/tableau_web_server.log${NC}"
    cat /tmp/tableau_web_server.log
    exit 1
fi
echo ""

# Khởi động Desktop App
echo -e "${BLUE}→ Khởi động Desktop App...${NC}"
$PYTHON_CMD "$DESKTOP_APP" &
DESKTOP_APP_PID=$!

echo -e "${GREEN}✓ Desktop App đã khởi động (PID: $DESKTOP_APP_PID)${NC}"
echo ""

# Hướng dẫn
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ DỰ ÁN ĐÃ KHỞI ĐỘNG THÀNH CÔNG!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}Hướng dẫn sử dụng:${NC}"
echo -e "  1. Sử dụng Desktop App để chọn database và bảng"
echo -e "  2. Click 'Tạo URL' để tạo đường dẫn kết nối"
echo -e "  3. Click 'Mở Trình Duyệt' để mở web interface"
echo -e "  4. Sử dụng trong Tableau với Web Data Connector"
echo ""
echo -e "${YELLOW}Để dừng ứng dụng:${NC}"
echo -e "  - Đóng Desktop App"
echo -e "  - Nhấn Ctrl+C trong terminal này để dừng Web Server"
echo ""
echo -e "${YELLOW}Log files:${NC}"
echo -e "  - Web Server: /tmp/tableau_web_server.log"
echo ""

# Đợi Desktop App tắt
wait $DESKTOP_APP_PID

# Khi Desktop App đóng, tắt Web Server
echo -e "${YELLOW}Desktop App đã đóng. Dừng Web Server...${NC}"
kill $WEB_SERVER_PID 2>/dev/null
wait $WEB_SERVER_PID 2>/dev/null

echo -e "${GREEN}✓ Đã dừng tất cả ứng dụng${NC}"
echo -e "${BLUE}========================================${NC}"
