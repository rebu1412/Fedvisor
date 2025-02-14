import streamlit as st
import sqlite3
import google.generativeai as genai
from create_user.database import track_usage
st.set_page_config(layout="wide")

# Cấu hình API của Gemini
genai.configure(api_key=st.secrets["API_KEY"])

# Danh sách chủ đề
TOPIC_OPTIONS = ["Tất cả", "Học phí", "Tuyển sinh", "Học bổng", "Chương trình đào tạo", "Khác"]

def get_data_from_db(topic_filter):
    """Lấy dữ liệu từ database theo chủ đề đã chọn."""
    db_path = "data/data.db"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT title, content FROM admin_info WHERE topic = ?", (topic_filter,))
        data = cursor.fetchall()

    if not data:
        return None

    formatted_data = "\n\n".join([f"Title: {row[0]}\nContent: {row[1]}" for row in data])
    return formatted_data

def chatbot():
    """Giao diện chatbot với tracking"""
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("💬 Hỏi đáp cùng Chatbot")
        topic_filter = st.selectbox("🎯 Chọn chủ đề", TOPIC_OPTIONS, index=0)
        context_text = None if topic_filter == "Tất cả" else get_data_from_db(topic_filter)
        user_query = st.text_input("✍️ Nhập câu hỏi của bạn:")

        if user_query:
            track_usage("chatbot_usage")  # Đếm số lần sử dụng chatbot

            # Xây dựng prompt
            if topic_filter == "Tất cả":
                prompt = f"Bạn là một trợ lý AI hỗ trợ sinh viên. Chủ đề: {topic_filter}. Câu hỏi: {user_query}"
            elif context_text:
                prompt = f"Bạn là một trợ lý AI. Chủ đề: {topic_filter}. Dữ liệu trường: {context_text}. Câu hỏi: {user_query}"
            else:
                prompt = f"Bạn là một trợ lý AI. Chủ đề: {topic_filter}. Hiện không có dữ liệu từ trường. Câu hỏi: {user_query}"

            # Gửi yêu cầu đến AI
            try:
                llm = genai.GenerativeModel('gemini-1.5-flash')
                response = llm.generate_content(prompt)
                st.write("### 📢 Trả lời từ Chatbot:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Lỗi kết nối API: {e}")

    with col2:
        st.subheader("📌 Những chủ đề bạn có thể hỏi")
        for topic in TOPIC_OPTIONS:
            st.info(f"✅ **{topic}**")

