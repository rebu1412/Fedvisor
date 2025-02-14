import streamlit as st
from user_features.chat_channel import chat_channel
from user_features.chatbot import chatbot
from user_features.news import news
from user_features.job_notifications import job_notifications
from user_features.cv_support import cv_support
from user_features.other_features import other_features

def home_user():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("⚠ Vui lòng đăng nhập để truy cập các tính năng!")
        return

    st.title("Trang Chủ Fedvisor")

    # Sidebar menu
    menu = {
        "Kênh Trò Chuyện": chat_channel,
        "Chatbot": chatbot,
        "Tin tức": news,
        "Thông báo Việc làm": job_notifications,
        "Hỗ trợ làm CV": cv_support,
        "Tính năng khác": other_features
    }
    
    choice = st.sidebar.radio("📌 Chọn tính năng", list(menu.keys()))

    # Thêm nút đăng xuất
    if st.sidebar.button("🔴 Đăng xuất"):
        st.session_state["logged_in"] = False
        st.session_state.pop("user", None)
        st.rerun()  # Refresh lại trang để quay về trang đăng nhập

    # Hiển thị trang đã chọn
    menu[choice]()
