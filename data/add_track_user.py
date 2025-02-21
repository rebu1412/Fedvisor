import sqlite3

def update_activity_tracking_table():
    """Tạo bảng theo dõi hoạt động người dùng với username thay vì user_id"""
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()

    # Xóa bảng cũ nếu có (chỉ chạy khi cần)
    cursor.execute("DROP TABLE IF EXISTS user_activity_tracking")

    # Tạo bảng mới với username thay vì user_id
    cursor.execute("""
        CREATE TABLE user_activity_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,  -- Dùng username thay vì user_id
            action TEXT,
            session_id TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Bảng `user_activity_tracking` đã được cập nhật!")

# Chạy cập nhật
update_activity_tracking_table()
