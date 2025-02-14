import streamlit as st
import sqlite3
import google.generativeai as genai

st.set_page_config(layout="wide")

# Cấu hình API của Gemini
genai.configure(api_key= st.secrets["API_KEY"])


# Danh sách chủ đề (Giữ lại "Tất cả" và "Khác")
TOPIC_OPTIONS = ["Tất cả", "Học phí", "Tuyển sinh", "Học bổng", "Chương trình đào tạo", "Khác"]

def get_data_from_db(topic_filter):
    """Lấy dữ liệu từ database theo chủ đề đã chọn."""
    db_path = "data/data.db"

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT title, content FROM admin_info WHERE topic = ?", (topic_filter,))
        data = cursor.fetchall()

    if not data:
        return None  # Trả về None để xử lý logic riêng

    # Định dạng dữ liệu để gửi vào prompt
    formatted_data = "\n\n".join([
        f"Title: {row[0]}\nContent: {row[1]}"
        for row in data
    ])

    return formatted_data

def chatbot():
    """Giao diện chatbot trong Fedvisor với khả năng chọn topic."""

    # Chia giao diện thành 2 cột
    col1, col2 = st.columns([3, 1])

    with col1:
        st.subheader("💬 Hỏi đáp cùng Chatbot")

        # Chọn chủ đề
        topic_filter = st.selectbox("🎯 Chọn chủ đề", TOPIC_OPTIONS, index=0)

        # Xử lý dữ liệu theo chủ đề đã chọn
        if topic_filter == "Tất cả":
            context_text = None  # Không lấy dữ liệu từ database, chỉ tìm trên Internet
        else:
            context_text = get_data_from_db(topic_filter)

        # Ô nhập câu hỏi
        user_query = st.text_input("✍️ Nhập câu hỏi của bạn:")

        if user_query:
            # Tạo prompt tùy thuộc vào việc có dữ liệu trong database hay không
            if topic_filter == "Tất cả":
                prompt = (
                    "Bạn là một trợ lý AI chuyên hỗ trợ sinh viên.\n\n"
                    "📌 **Chủ đề được chọn: Tất cả**\n\n"
                    "Hiện tại, tôi sẽ không sử dụng dữ liệu từ nhà trường mà sẽ tìm kiếm trên Internet.\n"
                    "Vui lòng cung cấp thông tin phù hợp và ghi rõ đây là **thông tin tham khảo từ nguồn bên ngoài**.\n\n"
                    "Nếu không thể tìm thấy thông tin, hãy trả lời: 'Xin lỗi, tôi chưa có thông tin về câu hỏi này.'\n\n"
                    f"❓ **Câu hỏi của người dùng:** {user_query}"
                )
            elif context_text:
                prompt = (
                    "Bạn là một trợ lý AI chuyên hỗ trợ sinh viên.\n\n"
                    f"📌 **Chủ đề được chọn: {topic_filter}**\n\n"
                    "Dưới đây là danh sách các thông tin chính thống từ nhà trường liên quan đến chủ đề này:\n\n"
                    f"{context_text}\n\n"
                    "🎯 **Hướng dẫn trả lời:**\n"
                    "1. Nếu câu hỏi của người dùng nằm trong danh sách trên, hãy trích xuất thông tin phù hợp và ghi rõ đây là **thông tin chính thống từ nhà trường**.\n"
                    "2. Nếu câu hỏi không có trong danh sách trên, hãy tìm kiếm trên Internet và ghi rõ đây là **thông tin tham khảo từ nguồn bên ngoài**.\n"
                    "3. Nếu không thể tìm thấy câu trả lời từ bất kỳ nguồn nào, hãy trả lời: 'Xin lỗi, tôi chưa có thông tin về câu hỏi này. Vui lòng liên hệ phòng hành chính để được hỗ trợ chi tiết.'\n\n"
                    f"❓ **Câu hỏi của người dùng:** {user_query}"
                )
            else:
                prompt = (
                    "Bạn là một trợ lý AI chuyên hỗ trợ sinh viên.\n\n"
                    f"📌 **Chủ đề được chọn: {topic_filter}**\n\n"
                    "Hiện tại, không có dữ liệu chính thống từ nhà trường cho chủ đề này.\n"
                    "Vui lòng tìm kiếm trên Internet để cung cấp thông tin phù hợp và ghi rõ đây là **thông tin tham khảo từ nguồn bên ngoài**.\n\n"
                    "Nếu không thể tìm thấy thông tin, hãy trả lời: 'Xin lỗi, tôi chưa có thông tin về câu hỏi này.'\n\n"
                    f"❓ **Câu hỏi của người dùng:** {user_query}"
                )

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
        st.info("✅ **Học phí** – Mức học phí, cách đóng, hạn đóng")
        st.info("✅ **Tuyển sinh** – Điều kiện nhập học, xét tuyển")
        st.info("✅ **Học bổng** – Các chương trình học bổng, điều kiện")
        st.info("✅ **Chương trình đào tạo** – Môn học, ngành đào tạo")
        st.info("✅ **Khác** – Các vấn đề liên quan khác")
        st.info("✅ **Tất cả** – Tìm kiếm trên Internet mà không dùng dữ liệu nhà trường")
