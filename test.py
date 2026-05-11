import os
import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

# سحب المفتاح من متغيرات البيئة
API_KEY = os.getenv("MY_APP_API_KEY")

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    
    if not user_id:
        abort(400, description="Missing user ID")

    # تعريف الاستعلام بشكل آمن
    query = "SELECT * FROM users WHERE id = ?"
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # استخدام الطباعة العادية آمن
    print(f"Searching for user {user_id}")
    
    # تنفيذ الاستعلام مع التمرير الآمن للمتغيرات
    cursor.execute(query, (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    return str(result) if result else "User not found"

if __name__ == "__main__":
    app.run(debug=False)
