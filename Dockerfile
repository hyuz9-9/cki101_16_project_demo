# 使用與專案 Python 版本一致的基礎映像檔 (Python 3.13)
# python:3.13-slim 為官方提供之多架構映像檔，預設支援 ARM64 (如 Apple Silicon) 與 AMD64 (X86)
FROM python:3.13-slim

# 設定容器內部工作目錄
WORKDIR /app

# 複製並安裝相依套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 複製主程式與範本資料夾
COPY app.py .
COPY templates/ ./templates/


# 宣告容器內部監聽的 Port (Flask 預設為 5000)
EXPOSE 5000

# 停用 Python 的標準輸出緩衝區，確保日誌能即時輸出到 container log
ENV PYTHONUNBUFFERED=1

# 啟動應用程式
CMD ["python", "app.py"]
