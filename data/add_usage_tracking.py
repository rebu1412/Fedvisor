import sqlite3

def create_table():
    conn = sqlite3.connect("database.db")  # Kết nối đến database (hoặc tạo mới nếu chưa có)
    cursor = conn.cursor()
    
    # Tạo bảng user_usage_tracking nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_usage_tracking (
            user_id INTEGER,
            action TEXT,
            count INTEGER,
            PRIMARY KEY (user_id, action),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()  # Lưu thay đổi
    conn.close()  # Đóng kết nối

# Gọi hàm để tạo bảng
create_table()