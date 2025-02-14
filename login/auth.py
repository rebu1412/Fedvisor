import streamlit as st
from create_user.database import create_user, check_login


def register():
    st.subheader("Đăng ký tài khoản mới")
    username = st.text_input("Tên tài khoản")
    password = st.text_input("Mật khẩu", type="password")
    role = st.selectbox("Vai trò", ["student", "lecturer"])
    user_code = st.text_input("Mã người dùng")
    name = st.text_input("Họ và tên")
    email = st.text_input("Email")
    major = st.text_input("Ngành học")

    if st.button("Đăng ký"):
        if username and password and user_code and name:
            if create_user(username, password, role, user_code, name, email, major):
                st.success("Đăng ký thành công! Hãy đăng nhập.")
            else:
                st.error("Tên tài khoản đã tồn tại.")
        else:
            st.error("Vui lòng điền đầy đủ thông tin.")

def login():
    st.subheader("Đăng nhập")
    username = st.text_input("Tên tài khoản")
    password = st.text_input("Mật khẩu", type="password")

    if st.button("Đăng nhập"):
        user = check_login(username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = user[0]  # Lưu user_id
            st.session_state["username"] = user[1]  # Lưu tên tài khoản
            st.session_state["role"] = user[2]  # Lưu vai trò
            st.session_state["user"] = user  # Lưu toàn bộ thông tin user
            st.success(f"🎉 Chào mừng {user[1]}!")
            st.rerun()
        else:
            st.error("Tên tài khoản hoặc mật khẩu không đúng.")


