import streamlit as st
from login.auth import register, login
from user_home import home_user
from admin_home import admin_home

menu = ["Đăng nhập", "Đăng ký"]

if st.session_state.get("logged_in", False):
    user = st.session_state["user"]
    if user[3] == "admin":  
        admin_home()  # Nếu là admin -> vào trang quản trị
    else:
        home_user()  # Nếu là sinh viên/giảng viên -> vào trang chủ bình thường
else:
    # Chia trang thành 3 cột, cột giữa lớn nhất
    col1, col2, col3 = st.columns([1, 2, 1])  # 1:2:1 tỉ lệ cột

    with col2:  # Nội dung hiển thị ở giữa
        st.subheader("🔐 Vui lòng đăng nhập hoặc đăng ký")
        choice = st.radio("Chọn thao tác:", menu, horizontal=True)

        if choice == "Đăng nhập":
            login()
        elif choice == "Đăng ký":
            register()
