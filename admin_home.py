import streamlit as st
from admin_features.admin_info import admin_info
from admin_features.admin_jobs import admin_jobs
from admin_features.admin_updates import admin_updates
from admin_features.admin_feedback import admin_feedback
from admin_features.admin_stats import admin_stats

def admin_home():
    st.subheader("🔧 Trang quản trị")
    
    if "user" not in st.session_state:
        st.warning("Vui lòng đăng nhập để tiếp tục.")
        return

    user = st.session_state["user"]
    st.write(f"Chào mừng, **{user[5]}**! (Vai trò: {user[3]})")

    # Sidebar menu
    menu = {
        "Thông tin hành chính": admin_info,
        "Quản lý việc làm": admin_jobs,
        "Quản lý cập nhật": admin_updates,
        "Quản lý phản hồi": admin_feedback,
        "Xem thống kê": admin_stats
    }
    
    choice = st.sidebar.radio("📌 Chọn chức năng quản trị", list(menu.keys()))
    menu[choice]()  # Gọi trang tương ứng

    if st.sidebar.button("🔴 Đăng xuất"):
        del st.session_state["logged_in"]
        del st.session_state["user"]
        st.rerun()
