📦 環境佈署 (Installation & Setup)
1. 前置需求 (Prerequisites)
NVIDIA DGX Spark 或具備相同架構之 NVIDIA GPU 伺服器

已安裝 NVIDIA Container Toolkit 的 Ubuntu 環境

Blender 4.0+ (需支援 Python API 擴充)

WhatsApp Business 帳號與 API 憑證

2. 複製專案與環境初始化
Bash
git clone [https://github.com/xandy168/Spark3D.git](https://github.com/xandy168/Spark3D.git)
cd Spark3D
# 建立並啟動 Docker 本地 AI 環境
docker-compose up -d --build
3. 配置 blender-mcp 擴充
將 src/mcp_server 佈署至 Blender 的 Python 環境中，確保 MCP 伺服器能夠正確調用 Blender 內部的幾何網格編輯 (Mesh Editing) 與渲染模組：

Bash
# 在 Blender 內置 Python 環境中綁定 MCP 依賴
pip install -r src/mcp_server/requirements.txt
4. 設定 openclaw 與 WhatsApp Webhook
修改 config.yaml，填入您的本地 Nemotron API Endpoint 以及 WhatsApp API 驗證 Token：

YAML
llm:
  base_url: "http://localhost:8000/v1"
  model: "Nemotron-Local"
whatsapp:
  verify_token: "YOUR_VERIFY_TOKEN"
  access_token: "YOUR_ACCESS_TOKEN"
💡 使用範例 (Usage Showcase)
文字輸入： 在 WhatsApp 輸入 建立一個直徑 5 單位、帶有 8 個散熱孔的科技感圓柱底座。

多模態輸入： 拍攝一張筆記本上的機械外殼手繪草圖，上傳至 WhatsApp 並附帶文字 轉換為 3D 概念模型。

系統回應： NemoClaw 在後台完成解析與建模後，將會自動把高解析度的 .png 渲染圖或 .fbx/.obj 模型檔案直接回傳至您的 WhatsApp 對話框中。

📄 開源授權 (License)
本專案採用 MIT 授權條款。詳情請參閱 LICENSE 檔案。

Designed by 陳炫光
"""

with open("README.md", "w", encoding="utf-8") as f:
f.write(readme_content)

print("README.md successfully created.")
