import streamlit as st
from admin_dashboard import admin_dashboard

def admin_home():
    st.subheader("🔧 Trang quản trị")
    if "user" in st.session_state:
        user = st.session_state["user"]
        st.write(f"Chào mừng, **{user[5]}**! (Vai trò: {user[3]})")

        st.markdown("### 📌 Quản lý thông tin hành chính")
        admin_dashboard()

        if st.button("Đăng xuất"):
            del st.session_state["logged_in"]
            del st.session_state["user"]
            st.rerun()
    else:
        st.warning("Vui lòng đăng nhập để tiếp tục.")
