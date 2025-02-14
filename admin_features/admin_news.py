import streamlit as st
from create_user.database import add_news, get_news, update_news, delete_news

CATEGORIES = ["Thông báo", "Sự kiện", "Học tập", "Tuyển dụng"]

def admin_news():
    st.subheader("📰 Quản lý Tin tức")

    # Thêm Tin tức mới
    with st.expander("➕ Thêm Tin tức mới"):
        author = st.text_input("✍️ Người đăng (VD: Admin, Phòng Đào tạo)")
        title = st.text_input("📝 Tiêu đề Tin tức")
        category = st.selectbox("📂 Chủ đề", CATEGORIES)
        content = st.text_area("📜 Nội dung tin tức")

        if st.button("✅ Đăng Tin tức"):
            if author and title and category and content:
                add_news(author, title, category, content)
                st.success(f"✅ Đã đăng tin: {title}")
                st.rerun()
            else:
                st.error("⚠ Vui lòng nhập đầy đủ thông tin!")

    # Hiển thị danh sách tin tức
    st.subheader("📌 Danh sách Tin tức")
    news_data = get_news()

    for record in news_data:
        news_id, author, title, category, content, created_at, views, status = record

        with st.expander(f"{title} - {category} ({created_at})"):
            new_author = st.text_input(f"✍️ Người đăng ({news_id})", author)
            new_title = st.text_input(f"📝 Tiêu đề ({news_id})", title)
            new_category = st.selectbox(f"📂 Chủ đề ({news_id})", CATEGORIES, index=CATEGORIES.index(category))
            new_content = st.text_area(f"📜 Nội dung ({news_id})", content)
            new_status = st.selectbox(f"📌 Trạng thái ({news_id})", ["pending", "approved", "rejected"], index=["pending", "approved", "rejected"].index(status))

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📝 Cập nhật ({news_id})"):
                    update_news(news_id, new_author, new_title, new_category, new_content, new_status)
                    st.success(f"✅ Cập nhật thành công! {new_title}")
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Xóa ({news_id})"):
                    delete_news(news_id)
                    st.warning(f"⚠ Đã xóa tin tức: {title}")
                    st.rerun()
