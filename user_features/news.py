import streamlit as st
from create_user.database import get_approved_news

def news():
    st.title("📰 Tin tức mới nhất")

    # Lấy dữ liệu tin tức từ database
    news_data = get_approved_news()

    if not news_data:
        st.info("📭 Hiện chưa có tin tức nào được đăng.")
        return

    # Tạo bố cục 2 cột
    col1, col2 = st.columns([3, 1])

    with col2:  # Cột nhỏ hơn chứa ô tìm kiếm và bộ lọc
        search_query = st.text_input("🔍 Tìm kiếm tiêu đề", "")
        category_filter = st.selectbox("📂 Lọc theo chủ đề", ["Tất cả"] + list(set(record[3] for record in news_data)))

    # Lọc tin tức theo tìm kiếm hoặc chủ đề
    filtered_news = []
    for record in news_data:
        _, author, title, category, content, created_at, _, _ = record

        # Kiểm tra tiêu đề chứa từ khóa tìm kiếm
        match_search = search_query.lower() in title.lower() if search_query else True

        # Kiểm tra chủ đề có khớp bộ lọc
        match_category = (category_filter == "Tất cả") or (category_filter == category)

        if match_search and match_category:
            filtered_news.append(record)

    # Hiển thị kết quả sau khi lọc
    if not filtered_news:
        st.warning("🚫 Không tìm thấy tin tức nào phù hợp với bộ lọc!")
        return

    with col1:  # Cột chính hiển thị nội dung tin tức
        for record in filtered_news:
            _, author, title, category, content, created_at, _, _ = record

            with st.expander(f"📌 {title} ({category}) - {created_at}"):
                st.markdown(f"### 📰 **{title}**")  # Tăng kích thước tiêu đề
                st.write(f"**✍️ Người đăng:** {author}")
                st.write(f"**📅 Ngày đăng:** {created_at}")
                st.markdown(f"📜 **Nội dung:**\n\n{content}")
                st.divider()
