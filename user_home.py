import streamlit as st

def home_user():
    st.subheader("🎓 Trang chủ - Người dùng")
    if "user" in st.session_state:
        user = st.session_state["user"]
        st.write(f"Chào mừng, **{user[5]}**! (Vai trò: {user[3]})")

        if st.button("Đăng xuất"):
            del st.session_state["logged_in"]
            del st.session_state["user"]
            st.rerun()
    else:
        st.warning("Vui lòng đăng nhập để tiếp tục.")
