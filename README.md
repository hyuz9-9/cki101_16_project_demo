# Flask 專案與 Docker 封裝說明

本專案是一個簡單的 Flask 網頁應用程式，並附帶支援多平台 (ARM / X86) 建置與運行的 Dockerfile 設定。

## 功能簡介
- 當訪問 `/` 時，會看到網頁顯示 `我是功能-` 文字。

---

## 本地開發與運行 (Virtual Environment)

### 1. 啟用虛擬環境
在專案根目錄下，根據您的作業系統執行以下指令啟用 `venv`：

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

### 2. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 3. 啟動 Flask
```bash
python app.py
```
啟動後可訪問 [http://127.0.0.1:5000](http://127.0.0.1:5000)。

---

## Docker 封裝與部署

本專案的 Docker 基礎映像檔採用 `python:3.13-slim`，與本地開發環境的 Python 3.13 版本完全一致。

### 1. 支援 ARM / X86 多平台建置

由於 Apple Silicon (M1/M2/M3) 等 macOS 系統為 ARM 架構，若在本地直接執行 `docker build`，預設會產生 **ARM (linux/arm64)** 的映像檔。

若要同時建置支援 **ARM** 與 **X86 (linux/amd64)** 的映像檔，或建置特定平台的映像檔，請參考以下方式：

#### 方式 A：建置目前本機架構的映像檔 (Mac M系列預設為 ARM)
```bash
docker build -t flask-app-demo .
```

#### 方式 B：指定建置 ARM 架構映像檔
```bash
docker build --platform linux/arm64 -t flask-app-demo:arm64 .
```

#### 方式 C：指定建置 X86 架構映像檔 (相容 Intel/AMD)
```bash
docker build --platform linux/amd64 -t flask-app-demo:amd64 .
```

#### 方式 D：使用 buildx 同時建置多架構 (ARM & X86) 並推送至 Docker Hub
```bash
# 建立並啟用支援多平台建置的 builder
docker buildx create --name mybuilder --use
docker buildx inspect --bootstrap

# 建置並推送支援 linux/amd64 與 linux/arm64 雙架構的映像檔
docker buildx build --platform linux/amd64,linux/arm64 -t <您的Docker帳號>/flask-app-demo:latest --push .
```

---

### 2. 運行 Container 並進行 Port 映射 (80 -> 5000)

Flask 預設在容器內監聽 **5000** port。若希望在運行 container 時將其映射到主機的 **80** port，請執行以下指令：

```bash
docker run -d -p 80:5000 --name flask-app-container flask-app-demo
```

運行成功後，即可直接透過 [http://localhost](http://localhost) 訪問網頁。

---

### 3. 使用 Docker Compose 啟動服務

我們也提供了 `docker-compose.yml` 設定檔。請在專案根目錄下執行以下指令以啟動服務：

- **啟動服務（背景運行）：**
  ```bash
  docker compose up -d --build
  ```
- **查看執行狀態與日誌：**
  ```bash
  docker compose logs -f
  ```
- **停止並刪除容器：**
  ```bash
  docker compose down
  ```

同樣地，啟動後可直接透過 [http://localhost](http://localhost) 訪問網頁。

