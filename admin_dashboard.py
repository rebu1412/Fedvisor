import streamlit as st
from create_user.database import add_admin_info, get_admin_info, update_admin_info, delete_admin_info

# Danh sách chủ đề cố định
TOPIC_OPTIONS = ["Học phí", "Tuyển sinh", "Học bổng", "Chương trình đào tạo", "Khác"]

def admin_dashboard():
    st.subheader("📌 Quản lý Thông tin Hành chính")

    # Thêm thông tin hành chính
    with st.expander("➕ Thêm Thông tin Hành chính"):
        title = st.text_input("Tiêu đề")
        content = st.text_area("Nội dung")
        topic = st.selectbox("Chủ đề", TOPIC_OPTIONS)  # Chọn chủ đề từ danh sách có sẵn

        if st.button("Lưu Thông tin Hành Chính"):
            if title and content and topic:
                add_admin_info(title, content, topic)  # Lưu luôn topic vào database
                st.success("✅ Thêm thành công!")
                st.rerun()
            else:
                st.error("⚠ Vui lòng nhập đầy đủ thông tin!")

    # Hiển thị danh sách thông tin hành chính
    st.subheader("📜 Danh sách Thông tin Hành chính")
    admin_data = get_admin_info()  # Lấy dữ liệu từ database

    for record in admin_data:
        info_id, title, content, topic, date = record  # Lấy cả topic từ database
        with st.expander(f"{title} ({date}) - {topic}"):  # Hiển thị chủ đề đã lưu
            new_title = st.text_input(f"Tiêu đề ({info_id})", title)
            new_content = st.text_area(f"Nội dung ({info_id})", content)
            new_topic = st.selectbox(f"Chủ đề ({info_id})", TOPIC_OPTIONS, index=TOPIC_OPTIONS.index(topic) if topic in TOPIC_OPTIONS else 0)

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📝 Cập nhật ({info_id})"):
                    update_admin_info(info_id, new_title, new_content, new_topic)
                    st.success("✅ Cập nhật thành công!")
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Xóa ({info_id})"):
                    delete_admin_info(info_id)
                    st.warning("⚠ Đã xóa thông tin này!")
                    st.rerun()
