import sqlite3
import random
from datetime import datetime, timedelta

# Kết nối đến cơ sở dữ liệu SQLite
def connect_db():
    return sqlite3.connect('data/data.db')  # Đảm bảo rằng đường dẫn cơ sở dữ liệu là đúng

# Hàm để thêm thời gian ngẫu nhiên vào bảng user_activity_tracking
def add_random_time():
    conn = connect_db()
    cursor = conn.cursor()

    # Lấy danh sách người dùng từ bảng user_activity_tracking
    cursor.execute("SELECT DISTINCT username FROM user_activity_tracking")
    users = cursor.fetchall()

    # Thêm thời gian ngẫu nhiên vào bảng user_activity_tracking cho mỗi người dùng
    for user in users:
        username = user[0]
        
        # Tạo thời gian ngẫu nhiên từ 1 đến 3 phút
        random_minutes = random.randint(1, 3)
        
        # Tính thời gian hiện tại cộng thêm thời gian ngẫu nhiên
        current_time = datetime.now()
        new_time = current_time + timedelta(minutes=random_minutes)
        
        # Chèn bản ghi vào bảng user_activity_tracking
        cursor.execute("""
            INSERT INTO user_activity_tracking (username, action, session_id, timestamp)
            VALUES (?, ?, ?, ?)
        """, (username, "use_random_feature", str(random.randint(1000, 9999)), new_time.strftime('%Y-%m-%d %H:%M:%S')))
    
    # Lưu và đóng kết nối
    conn.commit()
    conn.close()
    print("Thời gian ngẫu nhiên đã được thêm vào cơ sở dữ liệu!")

# Gọi hàm để thực hiện việc thêm thời gian ngẫu nhiên
if __name__ == "__main__":
    add_random_time()
