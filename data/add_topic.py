import sqlite3

def add_column_if_not_exists(db_path, table_name, column_name, column_type):
    """Thêm cột mới vào bảng nếu cột chưa tồn tại."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Kiểm tra xem cột đã tồn tại chưa
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        
        if column_name not in columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            conn.commit()
            print(f"Đã thêm cột '{column_name}' vào bảng '{table_name}'.")
        else:
            print(f"Cột '{column_name}' đã tồn tại.")

# Gọi hàm để thêm cột `topic`
db_path = "data/data.db"
add_column_if_not_exists(db_path, "admin_info", "topic", "TEXT")