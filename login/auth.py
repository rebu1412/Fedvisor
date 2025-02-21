import streamlit as st
from create_user.database import create_user, check_login


import re
import streamlit as st
from create_user.database import create_user, check_username_exists

def register():
    st.subheader("Đăng ký tài khoản mới")

    username = st.text_input("Tên tài khoản")
    password = st.text_input("Mật khẩu", type="password")
    role = st.selectbox("Vai trò", ["student", "lecturer"])
    user_code = st.text_input("Mã sinh viên")
    name = st.text_input("Họ và tên")
    
    majors = [
        "Digital Marketing", "Quản trị khách sạn", "An toàn thông tin", 
        "Kỹ thuật phần mềm", "Trí tuệ nhân tạo", "IOT", "Thiết kế đồ họa", 
        "Ngôn ngữ Anh", "Ngôn ngữ Nhật", "Ngôn ngữ Hàn Quốc", "Khác"
    ]
    major = st.selectbox("Ngành học", majors)

    if st.button("Đăng ký"):
        # Kiểm tra tên tài khoản đã tồn tại
        if check_username_exists(username):
            st.error("Tên tài khoản đã tồn tại. Vui lòng chọn tên khác.")
            return

        # Kiểm tra độ dài mật khẩu
        if len(password) < 6:
            st.error("Mật khẩu phải có ít nhất 6 ký tự.")
            return

        # Kiểm tra định dạng mã người dùng (2 chữ + 6 số)
        user_code = user_code.upper()
        if not re.match(r"^[A-Z]{2}\d{6}$", user_code):
            st.error("Mã người dùng phải có đúng 2 chữ cái đầu + 6 số (VD: HE171326).")
            return

        # Kiểm tra điền đầy đủ thông tin
        if username and password and user_code and name:
            if create_user(username, password, role, user_code, name, major):
                st.success("Đăng ký thành công! Hãy đăng nhập.")
            else:
                st.error("Đã xảy ra lỗi khi đăng ký.")
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


