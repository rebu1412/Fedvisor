import sqlite3

# Kết nối đến database
conn = sqlite3.connect("data/data.db")
cursor = conn.cursor()

# Lấy danh sách các bảng trong database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Danh sách các bảng trong database:")
for table in tables:
    table_name = table[0]
    print(f"\nBảng: {table_name}")

    # Lấy danh sách các cột trong bảng
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()

    print("  Các cột:")
    for col in columns:
        print(f"    - {col[1]} ({col[2]})")  # col[1] là tên cột, col[2] là kiểu dữ liệu

# Đóng kết nối
conn.close()
