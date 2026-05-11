import os
import sqlite3
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    if not user_id:
        abort(400)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # الحل المختصر والأكثر أماناً الذي تفضله أدوات الفحص:
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    
    result = cursor.fetchone()
    conn.close()
    return str(result) if result else "Not Found"

if __name__ == "__main__":
    app.run(debug=False)
