import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/user')
def get_user():
    # سحب المعرف وتحويله لنص صريح لضمان النوع
    raw_id = request.args.get('id', '')
    
    if not raw_id:
        abort(400)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # استخدام المتغير مباشرة داخل الاستعلام المجهز
    # تأكد أن الأقواس والفاصلة (raw_id,) مكتوبة بالضبط كذا
    cursor.execute("SELECT * FROM users WHERE id = ?", (raw_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return str(result) if result else "Not Found"

if __name__ == "__main__":
    app.run(debug=False)
