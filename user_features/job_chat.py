import streamlit as st
import sqlite3
import google.generativeai as genai
import re
from create_user.database import track_usage

# Cấu hình API của Gemini
genai.configure(api_key=st.secrets["API_KEY"])
DB_PATH = "data/data.db"

def fetch_job_details(job_codes):
    """Lấy thông tin chi tiết của nhiều công việc từ database."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        placeholders = ",".join(["?"] * len(job_codes))  # Tạo danh sách placeholders (?, ?, ...)
        query = f"SELECT * FROM jobs WHERE job_code IN ({placeholders})"
        cursor.execute(query, job_codes)
        return cursor.fetchall()

def process_user_query(user_query):
    """Xử lý câu hỏi của người dùng và tạo prompt cho AI với nhiều mã công việc."""
    job_codes = re.findall(r"#([A-Za-z0-9]+)", user_query)  # Tìm tất cả mã công việc trong câu hỏi

    if not job_codes:
        return "Không tìm thấy mã công việc. Vui lòng nhập mã công việc (ví dụ: #AI1402) để nhận thông tin chi tiết.\n\n❓ **Câu hỏi:** " + user_query

    job_details_list = fetch_job_details(job_codes)

    if not job_details_list:
        return f"Không tìm thấy mã công việc nào trong danh sách: {', '.join(job_codes)}. Hãy kiểm tra lại.\n\n❓ **Câu hỏi:** {user_query}"

    context_texts = []
    found_jobs = set()
    
    for job_details in job_details_list:
        _, job_code, title, company, requirements, salary, job_type, date = job_details
        found_jobs.add(job_code)  # Lưu lại mã công việc đã tìm thấy
        
        context_texts.append(
            f"📝 **Mã công việc:** #{job_code}\n"
            f"📌 **Công việc:** {title}\n"
            f"🏢 **Công ty:** {company}\n"
            f"📂 **Loại công việc:** {job_type}\n"
            f"📅 **Ngày đăng:** {date}\n\n"
            f"### 📌 Yêu cầu công việc:\n{requirements}\n\n"
            f"### 💰 Quyền lợi được hưởng:\n{salary}\n"
        )

    missing_jobs = set(job_codes) - found_jobs  # Tìm các mã không có trong database
    if missing_jobs:
        context_texts.append(f"⚠️ Không tìm thấy thông tin cho các mã công việc sau: {', '.join(missing_jobs)}.")

    return "\n\n---\n\n".join(context_texts) + f"\n\n❓ **Câu hỏi:** {user_query}"

def job_chatbot():
    """Giao diện chatbot hỗ trợ tìm kiếm thông tin việc làm."""
    st.subheader("💬 Hỏi đáp cùng Chatbot")
    user_query = st.text_input("✍️ Nhập câu hỏi của bạn:")

    if user_query:
        track_usage("job_chatbot_query")  # Đếm số lượt hỏi chatbot.

        # Lấy thông tin từ database nếu có mã công việc trong câu hỏi
        job_context = process_user_query(user_query)

        # Tạo prompt với ngữ cảnh công việc
        prompt = f"""
        Bạn là một chatbot tư vấn nghề nghiệp thông minh. Hãy trả lời câu hỏi dưới đây một cách chuyên nghiệp, chính xác và ngắn gọn.

        1. Nếu câu hỏi liên quan đến **một công việc cụ thể**, hãy cung cấp thông tin chi tiết về:
           - Mô tả công việc
           - Kỹ năng cần thiết
           - Mức lương trung bình
           - Xu hướng tuyển dụng

        2. Nếu câu hỏi liên quan đến **lộ trình sự nghiệp**, hãy tư vấn các bước học tập, kinh nghiệm và chứng chỉ cần có.

        3. Nếu câu hỏi yêu cầu so sánh các công việc, hãy chỉ ra ưu, nhược điểm của từng nghề.

        4. Tránh trả lời các câu hỏi không liên quan đến việc làm.

        Dưới đây là thông tin liên quan đến câu hỏi (nếu có):

        {job_context}

        ❓ **Câu hỏi:** {user_query}
        """

        try:
            llm = genai.GenerativeModel('gemini-1.5-flash')
            response = llm.generate_content(prompt)
            st.write("### 📢 Trả lời từ Chatbot:")
            st.success(response.text)
        except Exception as e:
            st.error(f"Lỗi kết nối API: {e}")



