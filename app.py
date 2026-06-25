from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import random
import string
from datetime import datetime, timedelta
import csv
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_super_secret_key_for_flask'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    monthly_budget = db.Column(db.Integer, default=20000) 
    invoices = db.relationship('Invoice', backref='owner', lazy=True)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    inv_num = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.String(8), nullable=False)
    seller_name = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Integer, nullable=False)
    is_winner = db.Column(db.Boolean, default=False)
    details = db.relationship('InvoiceDetail', backref='invoice', lazy=True, cascade="all, delete-orphan")

class InvoiceDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(20), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')
        username = request.form.get('username')
        password = request.form.get('password')

        if action == 'register':
            if User.query.filter_by(username=username).first():
                flash('帳號已存在！請換一個名稱。', 'danger')
            else:
                new_user = User(username=username, password_hash=generate_password_hash(password))
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for('index'))
        elif action == 'login':
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash('帳號或密碼錯誤！', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    search_kw = request.args.get('search', '')
    search_month = request.args.get('month', '')
    week_offset = request.args.get('week_offset', '') 
    
    query = Invoice.query.filter_by(user_id=current_user.id)
    target_week_text = ""
    
    if week_offset != "":
        try:
            offset_weeks = int(week_offset)
            today = datetime.now()
            this_monday = today - timedelta(days=today.weekday())
            target_monday = this_monday - timedelta(weeks=offset_weeks)
            target_sunday = target_monday + timedelta(days=6)
            
            start_date_str = target_monday.strftime("%Y%m%d")
            end_date_str = target_sunday.strftime("%Y%m%d")
            
            query = query.filter(Invoice.date >= start_date_str, Invoice.date <= end_date_str)
            target_week_text = f"{target_monday.strftime('%m/%d')} ~ {target_sunday.strftime('%m/%d')}"
        except ValueError:
            pass
    elif search_month:
        if len(search_month) == 8: query = query.filter(Invoice.date == search_month)
        else: query = query.filter(Invoice.date.startswith(search_month))
        
    if search_kw:
        query = query.outerjoin(InvoiceDetail).filter(
            (Invoice.seller_name.like(f"%{search_kw}%")) | (InvoiceDetail.item_name.like(f"%{search_kw}%"))
        ).distinct()
        
    all_invoices = query.order_by(Invoice.id.desc()).all()
    
    chart_data = {}
    for inv in all_invoices:
        for detail in inv.details:
            chart_data[detail.category] = chart_data.get(detail.category, 0) + (detail.unit_price * detail.quantity)
    
    current_month = datetime.now().strftime("%Y%m")
    all_for_budget = Invoice.query.filter_by(user_id=current_user.id).all()
    month_invoices = [inv for inv in all_for_budget if inv.date.startswith(current_month)]
    current_month_total = sum(inv.total_amount for inv in month_invoices)
    
    today = datetime.now()
    this_monday = today - timedelta(days=today.weekday())
    active_offset = 0
    if week_offset != "":
        try: active_offset = int(week_offset)
        except ValueError: pass
        
    t_monday = this_monday - timedelta(weeks=active_offset)
    t_sunday = t_monday + timedelta(days=6)
    week_invoices = [inv for inv in all_for_budget if t_monday.strftime("%Y%m%d") <= inv.date <= t_sunday.strftime("%Y%m%d")]
    current_week_total = sum(inv.total_amount for inv in week_invoices)
    
    monthly_budget = current_user.monthly_budget if current_user.monthly_budget else 20000
    weekly_budget = monthly_budget // 4

    return render_template('index.html', invoices=all_invoices, chart_data=chart_data, current_user=current_user,
                           current_month_total=current_month_total, monthly_budget=monthly_budget,
                           current_week_total=current_week_total, weekly_budget=weekly_budget,
                           search_kw=search_kw, search_month=search_month, week_offset=week_offset, target_week_text=target_week_text)

@app.route('/api/set_budget', methods=['POST'])
@login_required
def set_budget():
    data = request.json
    new_budget = data.get('budget')
    if new_budget and int(new_budget) > 0:
        current_user.monthly_budget = int(new_budget)
        db.session.commit()
        return jsonify({"status": "success", "message": "預算額度已更新！"})
    return jsonify({"status": "error", "message": "無效的金額！"}), 400

@app.route('/api/trend_data')
@login_required
def trend_data():
    invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(Invoice.date).all()
    trends = {}
    for inv in invoices:
        f_date = f"{inv.date[:4]}/{inv.date[4:6]}/{inv.date[6:]}"
        trends[f_date] = trends.get(f_date, 0) + inv.total_amount
    return jsonify({"dates": list(trends.keys()), "amounts": list(trends.values())})

@app.route('/api/export_csv')
@login_required
def export_csv():
    invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(Invoice.date.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['發票號碼', '消費日期', '商家名稱', '總金額', '是否中獎'])
    for inv in invoices:
        winner_status = '是' if inv.is_winner else '否'
        formatted_date = f"{inv.date[:4]}/{inv.date[4:6]}/{inv.date[6:]}"
        writer.writerow([inv.inv_num, formatted_date, inv.seller_name, inv.total_amount, winner_status])
    output.seek(0)
    return Response('\ufeff' + output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=my_expenses.csv"})

@app.route('/api/sync_mock', methods=['GET'])
@login_required
def sync_mock_data():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=8))
    random_inv_num = f"{letters}-{numbers}"

    item_pool = [
        {"item_name": "星巴克 冰美式", "unit_price": 110},
        {"item_name": "麥當勞 大麥克套餐", "unit_price": 140},
        {"item_name": "統一超商 奮起湖便當", "unit_price": 89},
        {"item_name": "UNIQLO U系列短T", "unit_price": 590},
        {"item_name": "威秀影城 電影票", "unit_price": 320},
        {"item_name": "台灣高鐵 單程票", "unit_price": 1490}
    ]
    purchased_items = random.sample(item_pool, k=random.randint(1, 2))
    total_amount = sum(item['unit_price'] for item in purchased_items)
    
    mock_date = f"202606{random.randint(1,9):02d}"
    store_names = ["統一超商", "全家便利商店", "麥當勞", "台灣高鐵", "威秀影城", "UNIQLO"]
    random_seller = random.choice(store_names)

    new_invoice = Invoice(user_id=current_user.id, inv_num=random_inv_num, date=mock_date, seller_name=random_seller, total_amount=total_amount)
    db.session.add(new_invoice)
    db.session.commit()

    for item in purchased_items:
        category = "自訂其他" 
        if any(kw in item['item_name'] for kw in ["星巴克"]): category = "早餐"
        elif any(kw in item['item_name'] for kw in ["便當", "麥當勞"]): category = "午餐"
        elif any(kw in item['item_name'] for kw in ["UNIQLO"]): category = "服飾購物"
        elif any(kw in item['item_name'] for kw in ["電影票"]): category = "休閒娛樂"
        elif "高鐵" in item['item_name']: category = "交通行車"

        new_detail = InvoiceDetail(invoice_id=new_invoice.id, item_name=item['item_name'], quantity=1, unit_price=item['unit_price'], category=category)
        db.session.add(new_detail)
    db.session.commit() 
    return jsonify({"status": "success", "message": "雲端發票資料同步成功！"})

# 🌟 核心修正：接收前端傳來的自訂日期
@app.route('/api/add_manual', methods=['POST'])
@login_required
def add_manual():
    data = request.json
    manual_inv_num = f"MANUAL-{random.randint(10000000, 99999999)}"
    date_str = data.get('date', datetime.now().strftime("%Y%m%d"))
    
    new_invoice = Invoice(user_id=current_user.id, inv_num=manual_inv_num, date=date_str, seller_name="手動記帳", total_amount=int(data['amount']))
    db.session.add(new_invoice)
    db.session.commit()

    new_detail = InvoiceDetail(invoice_id=new_invoice.id, item_name=data['item_name'], quantity=1, unit_price=int(data['amount']), category=data['category'])
    db.session.add(new_detail)
    db.session.commit()
    return jsonify({"status": "success", "message": "手動記帳成功！已同步至儀表板。"})

@app.route('/api/delete_invoice/<int:inv_id>', methods=['POST'])
@login_required
def delete_invoice(inv_id):
    inv = Invoice.query.get_or_404(inv_id)
    if inv.user_id != current_user.id:
        return jsonify({"status": "error", "message": "無權限執行此操作"}), 403
    
    db.session.delete(inv)
    db.session.commit()
    return jsonify({"status": "success", "message": "該筆帳務已成功刪除！"})

@app.route('/api/edit_invoice/<int:inv_id>', methods=['POST'])
@login_required
def edit_invoice(inv_id):
    inv = Invoice.query.get_or_404(inv_id)
    if inv.user_id != current_user.id:
        return jsonify({"status": "error", "message": "無權限執行此操作"}), 403
    
    data = request.json
    new_name = data.get('item_name')
    new_amount = int(data.get('amount'))

    inv.total_amount = new_amount
    if inv.details:
        first_detail = inv.details[0]
        first_detail.item_name = new_name
        first_detail.unit_price = new_amount
        first_detail.quantity = 1
        for d in inv.details[1:]:
            db.session.delete(d)
    else:
        new_detail = InvoiceDetail(invoice_id=inv.id, item_name=new_name, quantity=1, unit_price=new_amount, category="自訂其他")
        db.session.add(new_detail)

    db.session.commit()
    return jsonify({"status": "success", "message": "帳務已成功更新！"})

@app.route('/api/check_lottery', methods=['POST'])
@login_required
def check_lottery():
    data = request.json
    winning_number = data.get('winning_number', '')
    if len(winning_number) < 3: return jsonify({"status": "error", "message": "請至少輸入3碼對獎號碼喔！"})
    invoices = Invoice.query.filter_by(user_id=current_user.id).all()
    winner_count = 0
    for inv in invoices:
        if '-' in inv.inv_num and not inv.inv_num.startswith('MANUAL'):
            num_part = inv.inv_num.split('-')[1]
            if num_part.endswith(winning_number):
                inv.is_winner = True
                winner_count += 1
            else: inv.is_winner = False
    db.session.commit()
    if winner_count > 0: return jsonify({"status": "success", "message": f"🎉 太神啦！共有 {winner_count} 張發票中獎！"})
    else: return jsonify({"status": "success", "message": "這次沒有發票中獎，下次再接再厲！"})

if __name__ == '__main__':
    app.run(debug=True)