import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/user')
def get_user():
    # 1. سحب البيانات
    user_input = request.args.get('id', '')
    
    # 2. عملية التنظيف (Sanitization)
    # نحول المدخل لرقم صحيح، إذا فشل يعني أن المدخل قد يكون محاولة اختراق
    try:
        clean_id = int(user_input)
    except ValueError:
        abort(400, description="Invalid ID format")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 3. الآن نستخدم المتغير "النظيف"
    # Codacy ستلاحظ أنك قمت بـ 'Validation' قبل الاستخدام
    cursor.execute("SELECT * FROM users WHERE id = ?", (clean_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return str(result) if result else "User not found"

if __name__ == "__main__":
    app.run(debug=False)
