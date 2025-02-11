import streamlit as st
from login.auth import register, login
from user_home import home_user
from admin_home import admin_home

st.title("Fedvisor - Nền tảng học tập")

menu = ["Đăng nhập", "Đăng ký"]
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    user = st.session_state["user"]
    if user[3] == "admin":  
        admin_home()  # Nếu là admin -> vào trang quản trị
    else:
        home_user()  # Nếu là sinh viên/giảng viên -> vào trang chủ bình thường
else:
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Đăng nhập":
        login()
    elif choice == "Đăng ký":
        register()
