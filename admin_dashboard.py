import streamlit as st
from create_user.database import add_admin_info, get_admin_info, update_admin_info, delete_admin_info

def admin_dashboard():
    st.subheader("📌 Quản lý Thông tin Hành chính")

    # Thêm thông tin hành chính
    with st.expander("➕ Thêm Thông tin Hành chính"):
        title = st.text_input("Tiêu đề")
        content = st.text_area("Nội dung")

        # Thêm thông tin hành chính (Không cần nhập ID)
        if st.button("Lưu Thông tin Hành Chính"):
            if title and content:
                add_admin_info(title, content)  # Gọi hàm mà không truyền info_id
                st.success("✅ Thêm thành công!")
                st.rerun()
            else:
                st.error("⚠ Vui lòng nhập đầy đủ tiêu đề và nội dung!")


    # Hiển thị danh sách thông tin hành chính
    st.subheader("📜 Danh sách Thông tin Hành chính")
    admin_data = get_admin_info()

    for record in admin_data:
        info_id, title, content, date = record
        with st.expander(f"{title} ({date})"):
            new_title = st.text_input(f"Tiêu đề ({info_id})", title)
            new_content = st.text_area(f"Nội dung ({info_id})", content)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📝 Cập nhật ({info_id})"):
                    if st.confirm(f"Bạn có chắc muốn cập nhật thông tin '{title}'?"):
                        update_admin_info(info_id, new_title, new_content)
                        st.success("✅ Cập nhật thành công!")
                        st.rerun()
            with col2:
                if st.button(f"🗑️ Xóa ({info_id})"):
                    if st.confirm(f"⚠ Bạn có chắc muốn xóa '{title}'? Hành động này không thể hoàn tác!"):
                        delete_admin_info(info_id)
                        st.warning("⚠ Đã xóa thông tin này!")
                        st.rerun()
