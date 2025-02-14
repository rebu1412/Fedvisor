import sqlite3

def update_news_table():
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()
    
    # Kiểm tra bảng có tồn tại hay chưa
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='news'")
    table_exists = cursor.fetchone()

    if not table_exists:
        # Tạo bảng news
        cursor.execute("""
            CREATE TABLE news (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                views INTEGER DEFAULT 0,
                status TEXT DEFAULT 'pending'
            )
        """)
        conn.commit()
        print("✔ Bảng 'news' đã được tạo.")
    else:
        print("✔ Bảng 'news' đã tồn tại.")

    conn.close()

# Gọi hàm để kiểm tra và cập nhật database
update_news_table()
