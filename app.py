from flask import Flask, jsonify, render_template, request # 🌟 新增了 request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ==========================================
# 資料庫模型設計 (維持不變)
# ==========================================
class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inv_num = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.String(8), nullable=False)
    seller_name = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    is_winner = db.Column(db.Boolean, default=False) # 🌟 這個欄位現在要派上用場了！
    details = db.relationship('InvoiceDetail', backref='invoice', lazy=True)

class InvoiceDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(20), nullable=True)
# 🌟 新增這兩行：確保雲端引擎 (gunicorn) 啟動時，一定會建立空白資料表！
with app.app_context():
    db.create_all()
# ==========================================
# 首頁渲染邏輯
# ==========================================
@app.route('/')
def index():
    all_invoices = Invoice.query.order_by(Invoice.id.desc()).all()
    category_totals = db.session.query(
        InvoiceDetail.category,
        func.sum(InvoiceDetail.unit_price * InvoiceDetail.quantity).label('total')
    ).group_by(InvoiceDetail.category).all()
    chart_data = {row.category: row.total for row in category_totals}
    return render_template('index.html', invoices=all_invoices, chart_data=chart_data)

# ==========================================
# 核心 API 1：模擬載具同步 (維持不變)
# ==========================================
@app.route('/api/sync_mock', methods=['GET'])
def sync_mock_data():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=8))
    random_inv_num = f"{letters}-{numbers}"

    item_pool = [
        {"item_name": "RTX 4070 顯示卡", "unit_price": 18990},
        {"item_name": "16GB DDR5 記憶體", "unit_price": 2990},
        {"item_name": "水手牌特級強力粉", "unit_price": 150},
        {"item_name": "六吋巴斯克蛋糕模具", "unit_price": 250},
        {"item_name": "統一超商 大杯拿鐵", "unit_price": 55},
        {"item_name": "高鐵單程票", "unit_price": 1490}
    ]
    purchased_items = random.sample(item_pool, k=random.randint(1, 2))
    total_amount = sum(item['unit_price'] for item in purchased_items)

    new_invoice = Invoice(
        inv_num=random_inv_num, date="20260603", seller_name="系統模擬商家", total_amount=total_amount
    )
    db.session.add(new_invoice)
    db.session.commit()

    for item in purchased_items:
        category = "其他" 
        if any(kw in item['item_name'] for kw in ["拿鐵", "便當", "茶"]): category = "餐飲食品"
        elif any(kw in item['item_name'] for kw in ["顯示卡", "記憶體"]): category = "數位3C"
        elif any(kw in item['item_name'] for kw in ["麵粉", "模具"]): category = "烘焙開銷"
        elif "高鐵" in item['item_name']: category = "交通運輸"

        new_detail = InvoiceDetail(
            invoice_id=new_invoice.id, item_name=item['item_name'],
            quantity=1, unit_price=item['unit_price'], category=category 
        )
        db.session.add(new_detail)
    db.session.commit() 
    return jsonify({"status": "success", "message": "載具同步成功！"})

# ==========================================
# 🌟 新增 API 2：接收手動記帳表單
# ==========================================
@app.route('/api/add_manual', methods=['POST'])
def add_manual():
    data = request.json # 接收網頁傳來的 JSON 資料
    
    # 幫手動記帳產生一個專屬的假發票號碼 (MANUAL-開頭)
    manual_inv_num = f"MANUAL-{random.randint(10000000, 99999999)}"
    
    new_invoice = Invoice(
        inv_num=manual_inv_num, date="20260603", 
        seller_name="手動記帳 (無載具)", total_amount=int(data['amount'])
    )
    db.session.add(new_invoice)
    db.session.commit()

    new_detail = InvoiceDetail(
        invoice_id=new_invoice.id, item_name=data['item_name'],
        quantity=1, unit_price=int(data['amount']), category=data['category']
    )
    db.session.add(new_detail)
    db.session.commit()
    
    return jsonify({"status": "success", "message": "手動記帳成功！已加入圓餅圖計算。"})

# ==========================================
# 🌟 新增 API 3：自動對獎系統
# ==========================================
@app.route('/api/check_lottery', methods=['POST'])
def check_lottery():
    data = request.json
    winning_number = data.get('winning_number', '') # 取得使用者輸入的中獎號碼

    if len(winning_number) < 3:
        return jsonify({"status": "error", "message": "請至少輸入3碼對獎號碼喔！"})

    invoices = Invoice.query.all()
    winner_count = 0

    for inv in invoices:
        # 只比對有真實格式的發票 (排除手動記帳的 MANUAL)
        if '-' in inv.inv_num and not inv.inv_num.startswith('MANUAL'):
            # 取出發票號碼的數字部分 (例如 AB-12345678 取出 12345678)
            num_part = inv.inv_num.split('-')[1]
            # 如果發票號碼的尾數等於中獎號碼，就是中獎了！
            if num_part.endswith(winning_number):
                inv.is_winner = True
                winner_count += 1
            else:
                inv.is_winner = False # 沒中獎的歸零

    db.session.commit()
    
    if winner_count > 0:
        return jsonify({"status": "success", "message": f"🎉 太神啦！共有 {winner_count} 張發票中獎！"})
    else:
        return jsonify({"status": "success", "message": "幫QQ，這次沒有發票中獎，下次再接再厲！"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)