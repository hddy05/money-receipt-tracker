# 📊 智慧記帳與載具整合儀表板 (Smart Finance Tracker)

這是一款專為現代數位生活打造的智慧記帳系統，結合了直覺的視覺化 UI、防呆互動設計與進階資料庫查詢功能。本系統拋棄了傳統繁瑣的表單輸入，引入智慧預測與雲端發票綁定概念，實現流暢的個人財務自動化管理。

🔗 **線上 Live Demo:** [點擊這裡體驗](https://invoice-tracker-qqa6.onrender.com)

## 🚀 核心亮點功能 (Key Features)

- **🔐 獨立安全帳戶**：採用密碼雜湊加密 (Hash)，每位使用者的財務資料完全獨立且安全。
- **🌓 智慧雙主題 (Dark/Light Mode)**：內建無縫切換的深淺色電競質感主題，並利用 `localStorage` 記憶使用者偏好。
- **🧠 智慧財務大腦與預測**：
  - **自動分類預測**：輸入「高鐵」或「RTX 4070 顯示卡」等關鍵字，系統將自動選定「交通」或「3C」分類。
  - **動態診斷報告**：根據當月花費最高的類別與預算消耗比例，即時生成客製化財務建議。
- **📊 雙核視覺化儀表板**：整合 Chart.js，即時呈現「支出分類圓餅圖」與「消費趨勢折線圖」。
- **🛒 雲端載具綁定對接**：支援實體條碼槍掃描，可一鍵模擬同步財政部電子發票，並自動生成逼真的連鎖商家消費明細。
- **🛡️ 終極防呆機制**：嚴格的輸入驗證，阻擋非法數值（負數、字母），並全面導入 SweetAlert2 取代傳統系統彈窗，提供極致的 UX 體驗。
- **📥 商業級報表匯出**：支援將個人發票明細一鍵匯出為無亂碼的 CSV 檔案，便於後續 Excel 理財規劃。

## 🛠️ 技術棧 (Tech Stack)

- **後端 (Backend):** Python 3, Flask, Flask-Login, Werkzeug
- **資料庫 (Database):** SQLite (透過 SQLAlchemy ORM 進行關聯管理與進階查詢)
- **前端 (Frontend):** HTML5, CSS3, Bootstrap 5.3, JavaScript (ES6)
- **資料視覺化 & 互動:** Chart.js, SweetAlert2
- **部署 (Deployment):** Render CI/CD

## 💻 本地端運行指南 (Local Setup)

1. 複製此專案到本地端：
   ```bash
   git clone [你的 GitHub Repo 網址]