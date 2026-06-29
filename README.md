# 📊 智慧記帳與雲端發票整合儀表板 (Smart Financial Dashboard)

本專案為一款基於 Web 架構開發之個人財務管理系統。系統設計宗旨在於解決傳統記帳軟體「輸入繁瑣、防呆機制不全、圖表互動性低」等痛點。透過導入關鍵字預測演算法、動態時間區間運算模組，以及嚴謹的 CRUD 與防呆機制，實現高度自動化與視覺化的數據驅動財務管理。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-lightgrey.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap%205-purple.svg)
![Chart.js](https://img.shields.io/badge/Chart.js-3D%20Interactive-yellow.svg)

## 🔥 核心系統模組 (Core System Modules)

### 🧠 1. 智慧財務預測與雲端整合模組
* **一鍵載具同步模擬**：透過 Python `random` 模組實作亂數演算法，模擬實體條碼槍串接財政部電子發票之情境，自動生成連鎖商家消費明細。
* **關鍵字預測分類引擎**：於前端實作 DOM 陣列遍歷與字串比對演算法（O(n) 時間複雜度）。使用者輸入字串時，系統即時掃描 `keywordMap` 字典庫並自動觸發分類綁定，降低手動操作成本。
* **動態財務診斷報告**：後端運用 Python 字典 (Dictionary) 進行加總與排序找出最大開銷，即時生成客製化之理財建議。

### 📊 2. 雙核視覺化儀表板 (Dual-Core Data Visualization)
* **3D 浮動佔比分析**：整合 Chart.js，支援懸停（Hover）區塊放大預覽，並透過 JS 陣列 `reduce()` 動態換算出該品項佔總開銷之精確百分比 (`%`)。
* **互動式時序追蹤圖表**：導入 `interaction: 'index'` 模式之十字軸捕捉技術，解決傳統折線圖需精確點擊資料點的痛點，游標滑入垂直區間即可自動對齊並顯示精準數據。

### 🗓️ 3. 動態時間區間運算與雙預算監控
* **時間滑動視窗切換 (Sliding Time Window)**：後端透過 Python `datetime` 與 `timedelta` 進行精確的時間演算法推算，取代靜態寫死的日期，讓使用者能一鍵無縫切換「本週、上週、上上週」的歷史財務視角。
* **動態雙軌進度條**：開放使用者自訂「專屬月預算」，系統透過後端邏輯自動推算週預算基準線，並結合 Flask Jinja2 模板引擎，於前端即時渲染紅、黃、綠三色動態警告進度條。

### 🛡️ 4. 防呆機制與資料控制權 (Foolproof & CRUD)
* **時間序列資料防護**：導入 `Flatpickr` 套件強制封鎖 HTML 日期欄位之鍵盤輸入權限，徹底阻斷非法字串導致的系統崩潰。
* **互動式操作驗證**：全面採用 `SweetAlert2` 取代原生彈窗，於資料送出前進行雙重驗證 (Double Validation)，確保寫入資料庫之數值絕對合法。
* **無亂碼 CSV 報表匯出**：後端匯出 API 內建 `\ufeff` (UTF-8 BOM) 編碼處理，一鍵匯出無亂碼報表，確保資料能順利接軌 Excel 等數據分析軟體。

## 🛠️ 開發技術 (Tech Stack)
* **Backend**: Python, Flask, SQLAlchemy (ORM), SQLite
* **Frontend**: HTML5, CSS3, Bootstrap 5.3, JavaScript (ES6)
* **Libraries**: Chart.js, SweetAlert2, Flatpickr
* **Security**: Werkzeug Security (Hash 密碼雜湊加密), LocalStorage (前端狀態記憶)
* **Deployment**: Render CI/CD 雲端部署, Git/GitHub 版本控制