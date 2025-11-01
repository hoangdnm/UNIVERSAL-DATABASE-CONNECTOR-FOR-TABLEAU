#!/bin/bash

#################################################
# SCRIPT CHẠY ĐẦY ĐỦ
# Chạy cả Web Server và Desktop App
#################################################

# Màu sắc
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Lấy thư mục dự án
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}============================================================${NC}"
echo -e "${BLUE}   TABLEAU UNIVERSAL CONNECTOR - FULL${NC}"
echo -e "${BLUE}   Web Server + Desktop App${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

cd "$PROJECT_DIR"

# Tìm môi trường Python
echo -e "${YELLOW}[1/4] Kiểm tra môi trường Python...${NC}"

if [ -d "env" ]; then
    PYTHON_CMD="$PROJECT_DIR/env/bin/python"
    echo -e "${GREEN}✓ Sử dụng môi trường: env/${NC}"
elif [ -d "venv" ]; then
    PYTHON_CMD="$PROJECT_DIR/venv/bin/python"
    echo -e "${GREEN}✓ Sử dụng môi trường: venv/${NC}"
elif [ -d ".venv" ]; then
    PYTHON_CMD="$PROJECT_DIR/.venv/bin/python"
    echo -e "${GREEN}✓ Sử dụng môi trường: .venv/${NC}"
else
    PYTHON_CMD="python3"
    echo -e "${YELLOW}⚠ Sử dụng Python hệ thống${NC}"
fi

if ! command -v $PYTHON_CMD &> /dev/null; then
    echo -e "${RED}✗ Python không tìm thấy!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python: $($PYTHON_CMD --version)${NC}"
echo ""

# Kiểm tra thư viện
echo -e "${YELLOW}[2/4] Kiểm tra thư viện...${NC}"

MISSING_LIBS=0

$PYTHON_CMD -c "import flask" 2>/dev/null || MISSING_LIBS=1
$PYTHON_CMD -c "import customtkinter" 2>/dev/null || MISSING_LIBS=1

if [ $MISSING_LIBS -eq 1 ]; then
    echo -e "${YELLOW}⚠ Đang cài đặt thư viện còn thiếu...${NC}"
    $PYTHON_CMD -m pip install flask customtkinter pyodbc
fi

echo -e "${GREEN}✓ Thư viện: OK${NC}"
echo ""

# Kiểm tra port
echo -e "${YELLOW}[3/4] Kiểm tra port 5002...${NC}"
if command -v lsof &> /dev/null; then
    if lsof -Pi :5002 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Dừng process cũ trên port 5002...${NC}"
        kill -9 $(lsof -ti:5002) 2>/dev/null
        sleep 1
    fi
fi
echo -e "${GREEN}✓ Port sẵn sàng${NC}"
echo ""

# Khởi động Web Server
echo -e "${YELLOW}[4/4] Khởi động ứng dụng...${NC}"
echo -e "${BLUE}→ Web Server (background)...${NC}"

$PYTHON_CMD src/tableau_universal_connector.py > /tmp/tableau_web_server.log 2>&1 &
WEB_PID=$!

sleep 2

if ps -p $WEB_PID > /dev/null; then
    echo -e "${GREEN}✓ Web Server đã chạy (PID: $WEB_PID)${NC}"
    echo -e "${GREEN}  URL: http://127.0.0.1:5002${NC}"
else
    echo -e "${RED}✗ Web Server lỗi!${NC}"
    cat /tmp/tableau_web_server.log
    exit 1
fi
echo ""

# Khởi động Desktop App
echo -e "${BLUE}→ Desktop App (Modern UI)...${NC}"
$PYTHON_CMD Window_application/modern_ui.py &
DESKTOP_PID=$!

echo -e "${GREEN}✓ Desktop App đã chạy (PID: $DESKTOP_PID)${NC}"
echo ""

# Hướng dẫn
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}✓ KHỞI ĐỘNG THÀNH CÔNG!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "${YELLOW}PIDs:${NC}"
echo -e "  Web Server: $WEB_PID"
echo -e "  Desktop App: $DESKTOP_PID"
echo ""
echo -e "${YELLOW}Để dừng:${NC}"
echo -e "  - Đóng cửa sổ Desktop App"
echo -e "  - Hoặc nhấn Ctrl+C"
echo ""
echo -e "${YELLOW}Log: /tmp/tableau_web_server.log${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""

# Chờ Desktop App đóng
wait $DESKTOP_PID

# Dừng Web Server
echo -e "${YELLOW}Dừng Web Server...${NC}"
kill $WEB_PID 2>/dev/null
wait $WEB_PID 2>/dev/null

echo -e "${GREEN}✓ Đã dừng tất cả${NC}"
