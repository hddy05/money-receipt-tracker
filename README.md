# 📊 智慧記帳與雲端發票整合儀表板 (Smart Financial Dashboard)

這是一款專為現代人打造的**「免手動、全自動化」**個人財務管理 SaaS 系統。
我們拋棄了傳統記帳軟體繁瑣的表單輸入，導入了「雲端發票綁定」、「智慧財務預測大腦」以及「高互動雙核視覺化儀表板」，讓記帳回歸直覺，用數據驅動你的消費決策。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205-purple.svg)
![Chart.js](https://img.shields.io/badge/Chart.js-3D%20Interactive-yellow.svg)

## 🔥 核心商業級功能 (Core Features)

### 🧠 1. 智慧財務大腦與雲端整合
* **一鍵載具同步**：支援實體條碼槍或手動輸入手機條碼（如 `/ABCDEFG`），一鍵模擬串接財政部電子發票，瞬間完成記帳。
* **AI 分類預測引擎**：自動偵測品項關鍵字（如輸入「高鐵」自動歸類「交通行車」），徹底告別手動選單。
* **動態財務診斷報告**：系統會自動抓取當月最大開銷類別，並結合預算消耗比例，即時生成客製化的理財建議。

### 📊 2. 雙核視覺化儀表板 (Dual-Core Dashboard)
* **3D 浮動圓餅圖**：支援懸停（Hover）爆發放大預覽，並即時換算出該品項佔總開銷的「精確百分比 (%)」。
* **免瞄準折線圖**：導入專業理財軟體（如 TradingView）的 `interaction: 'index'` 模式，無需精準對齊小圓點，滑鼠移入即可自動對齊十字軸並顯示當日精確花費。

### 🗓️ 3. 時間阻尼引擎與雙軌預算監控
* **動態週/月視角切換**：致敬 iOS 原生設計的「膠囊型切換滑塊」，一鍵無縫切換「本週、上週、上上週」的財務視角。
* **動態雙軌進度條**：開放使用者自訂「專屬月預算」，系統會自動推算週預算基準線，並在上方顯示紅、黃、綠三色動態警告進度條。

### 🛡️ 4. 極致防呆與資料控制權 (CRUD)
* **Flatpickr 防呆日曆**：強制封鎖鍵盤非法輸入，搭配蘋果風格圓角日曆，確保時間序列資料的絕對乾淨。
* **SweetAlert2 互動體驗**：全面取代原生醜陋彈窗。並開放使用者透過高質感對話框「➕自訂專屬分類」、「✏️快速修改帳務」與「🗑️一鍵刪除」。
* **無亂碼 CSV 報表匯出**：內建 UTF-8 BOM 處理，一鍵下載發票紀錄，完美串接 Excel 進行後續財務規劃。

## 🛠️ 技術棧 (Tech Stack)
* **Backend**: Python, Flask, SQLAlchemy, SQLite
* **Frontend**: HTML5, CSS3, Bootstrap 5.3, JavaScript (ES6)
* **Libraries**: Chart.js, SweetAlert2, Flatpickr
* **Security**: Werkzeug Security (Hash Encryption), LocalStorage Theme Memory
* **Deployment**: Render CI/CD 雲端部署