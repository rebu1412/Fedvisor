import streamlit as st
from user_features.feedback_channel import feedback_channel
from user_features.chatbot import chatbot
from user_features.news import news
from user_features.job_notifications import job_notifications
from user_features.cv_support import cv_support
from user_features.other_features import other_features

# Sidebar với logo FPT
st.sidebar.image(
    'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-9Qh2rJaKcHthgCzbqkeZ2GWJJmcT2M4oXA&s',
    use_column_width=True
)

def home_user():
    """Trang chủ của Fedvisor với thiết kế tối giản hơn."""
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("⚠ Vui lòng đăng nhập để truy cập các tính năng!")
        return

    # Tiêu đề trang với logo lệch trái
    # Sidebar với logo FPT
    st.sidebar.image(
        'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-9Qh2rJaKcHthgCzbqkeZ2GWJJmcT2M4oXA&s',
        use_column_width=True
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
    
    st.sidebar.markdown("---")  # Đường phân cách
    choice = st.sidebar.radio("📌 **Chọn tính năng**", list(menu.keys()))

    # Nút đăng xuất
    if st.sidebar.button("🔴 **Đăng xuất**", help="Đăng xuất khỏi hệ thống"):
        st.session_state["logged_in"] = False
        st.session_state.pop("user", None)
        st.rerun()  # Refresh trang để trở về đăng nhập

    # Hiển thị nội dung của mục đã chọn
    menu[choice]()
