import sqlite3

def create_usage_table():
    """Tạo bảng theo dõi số lần sử dụng chức năng nếu chưa tồn tại"""
    conn = sqlite3.connect("data/data.db")  # Kết nối đến database
    cursor = conn.cursor()

    # Tạo bảng usage_tracking nếu chưa tồn tại
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usage_tracking (
            action TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    ''')

    conn.commit()  # Lưu thay đổi
    conn.close()  # Đóng kết nối

# Chạy hàm để tạo bảng
create_usage_table()
print("✅ Bảng 'usage_tracking' đã được tạo (nếu chưa tồn tại).")
