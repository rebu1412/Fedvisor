import streamlit as st
from user_features.feedback_channel import feedback_channel
from user_features.chatbot import chatbot
from user_features.news import news
from user_features.job_notifications import job_notifications
from user_features.cv_support import cv_support
from user_features.other_features import other_features
from create_user.database import track_usage, track_activity

def home_user():
    """Trang chủ của Fedvisor với thiết kế tối giản hơn."""
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("⚠ Vui lòng đăng nhập!")
        return

    username = st.session_state.get("username", "unknown_user")

    # Chỉ ghi nhận khi user mới đăng nhập
    if "tracked_login" not in st.session_state or not st.session_state["tracked_login"]:
        track_activity(username, "login")
        track_usage("user_home")  # Theo dõi đăng nhập
        st.session_state["tracked_login"] = True

    # Tiêu đề trang với logo lệch trái
    st.sidebar.image(
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-9Qh2rJaKcHthgCzbqkeZ2GWJJmcT2M4oXA&s',
        use_container_width=True
    )
    
    st.markdown(
        """
        <div style='display: flex; align-items: center;'>
            <img src='https://png.pngtree.com/png-clipart/20230401/original/pngtree-smart-chatbot-cartoon-clipart-png-image_9015126.png' width='120' style='margin-right: 15px;'/>
            <h1>Fedvisor - Trợ lý học tập FPT</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar menu
    menu = {
        "💬 Chatbot": chatbot,
        "📰 Tin tức": news,
        "💼 Thông báo Việc làm": job_notifications,
        "📄 Hỗ trợ làm CV": cv_support,
        "🛠️ Tính năng khác": other_features,
        "📢 Kênh Feedback": feedback_channel,
    }

    action_mapping = {
        "💬 Chatbot": "chatbot",
        "📰 Tin tức": "news",
        "💼 Thông báo Việc làm": "job_notifications",
        "📄 Hỗ trợ làm CV": "cv_support",
        "🛠️ Tính năng khác": "other_features",
        "📢 Kênh Feedback": "feedback_channel",
    }

    st.sidebar.markdown("---")  # Đường phân cách
    choice = st.sidebar.radio("📌 **Chọn tính năng**", list(menu.keys()))

    # Ghi nhận hoạt động sử dụng tính năng
    track_activity(username, f"use_{action_mapping[choice]}")

    # Nút đăng xuất
    if st.sidebar.button("🔴 **Đăng xuất**", help="Đăng xuất khỏi hệ thống"):
        track_activity(username, "logout")  # Ghi nhận hành động logout
        st.session_state["logged_in"] = False
        st.session_state.pop("session_id", None)  # Xóa session_id
        st.session_state.pop("tracked_login", None)  # Đặt lại trạng thái login
        if "user" in st.session_state:
            st.session_state.pop("user")
        st.rerun()

    # Hiển thị nội dung của mục đã chọn
    menu[choice]()
