import sqlite3
from datetime import datetime

def connect_db():
    """Kết nối đến cơ sở dữ liệu SQLite."""
    return sqlite3.connect("data/data.db")

def insert_user_activity(user_id, action_type, query=None, response=None):
    """Thêm dữ liệu vào bảng user_activity."""
    conn = connect_db()
    cursor = conn.cursor()

    try:
        # Kiểm tra xem action_type có hợp lệ không
        valid_actions = ('search', 'click', 'view', 'chat')
        if action_type not in valid_actions:
            raise ValueError(f"⚠ Hành động không hợp lệ: {action_type}. Chỉ chấp nhận {valid_actions}")

        # Thêm dữ liệu vào bảng user_activity
        cursor.execute("""
            INSERT INTO user_activity (user_id, action_type, query, response, timestamp) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, action_type, query, response, datetime.now()))

        conn.commit()
        print("✅ Dữ liệu đã được thêm thành công vào user_activity!")
    
    except sqlite3.IntegrityError as e:
        print(f"⚠ Lỗi ràng buộc dữ liệu: {e}")
    except Exception as e:
        print(f"❌ Lỗi không xác định: {e}")
    
    finally:
        conn.close()

# Ví dụ sử dụng
insert_user_activity(user_id=1, action_type="search", query="Tìm kiếm chatbot", response="Thông tin chatbot")
