import sqlite3

def clear_database():
    """Xóa toàn bộ dữ liệu nhưng giữ nguyên cấu trúc bảng"""
    conn = sqlite3.connect("data/data.db")
    cursor = conn.cursor()

    # Lấy danh sách tất cả các bảng trong database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]
        cursor.execute(f"DELETE FROM {table_name};")  # Xóa dữ liệu nhưng giữ bảng
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")  # Reset ID tự động tăng

    conn.commit()
    conn.close()
    print("✅ Dữ liệu trong database đã được xóa!")

# Gọi hàm xóa dữ liệu
clear_database()
