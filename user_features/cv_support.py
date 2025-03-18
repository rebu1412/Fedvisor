import streamlit as st
import base64
import google.generativeai as genai  # Thay bằng API của Gemini nếu bạn sử dụng dịch vụ này
from create_user.database import track_usage
from pdf2image import convert_from_path  # Thêm thư viện này để chuyển PDF thành ảnh
import os
import tempfile

# Cấu hình API của Gemini
genai.configure(api_key=st.secrets["API_KEY"])

# Hàm chuyển file PDF thành base64 (không sử dụng ở đây nữa, chỉ giữ lại nếu cần)
def convert_pdf_to_base64(uploaded_file):
    """Chuyển đổi file PDF thành chuỗi base64."""
    return base64.b64encode(uploaded_file.read()).decode('utf-8')

# Hàm hiển thị ảnh PDF từ file
def show_pdf_as_images(uploaded_file):
    """Chuyển đổi PDF thành ảnh và hiển thị ảnh đó."""
    # Lưu tệp PDF vào tệp tin tạm thời
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name  # Đường dẫn tệp PDF tạm thời

    # Chuyển đổi các trang PDF thành ảnh
    images = convert_from_path(temp_file_path, 300)  # Độ phân giải 300 DPI
    for i, image in enumerate(images):
        # Hiển thị từng trang dưới dạng ảnh
        st.image(image, caption=f"Trang {i + 1}", use_column_width=True)

    # Xóa tệp PDF tạm thời sau khi sử dụng
    os.remove(temp_file_path)

# Hàm chatbot hỗ trợ trả lời câu hỏi từ CV
def cv_support():
    """Giao diện hỗ trợ làm CV, cho phép tải lên file PDF CV và hỏi câu hỏi."""
    st.subheader("📄 Hỗ trợ làm CV")
    
    # Cho phép người dùng tải lên file PDF CV
    uploaded_file = st.file_uploader("🔄 Tải lên CV của bạn (PDF)", type=["pdf"])

    if uploaded_file is not None:
        # Hiển thị file PDF dưới dạng ảnh
        st.write("### 📑 CV đã được tải lên:")
        show_pdf_as_images(uploaded_file)  # Hiển thị PDF dưới dạng ảnh

        # Nhập câu hỏi về CV
        question = st.text_input("❓ Hỏi về CV của bạn:")
        
        if question:
            # Chúng ta có thể gọi API Gemini để trả lời câu hỏi từ CV (nếu cần)
            prompt = f"""
Bạn là một chuyên viên tư vấn việc làm. Dưới đây là một số chi tiết về CV của tôi:
- CV hiện tại không có văn bản trực tiếp (vì đây là ảnh của CV).
- Bạn sẽ không thể trích xuất thông tin cụ thể từ CV.

Câu hỏi của tôi liên quan đến CV là:
{question}

Hãy cung cấp câu trả lời rõ ràng, có tính hỗ trợ, dựa trên những thông tin mà bạn có thể tư duy từ các câu hỏi và thông tin chung về CV.

Trả lời:
"""
            
            try:
                # Gọi API Gemini để trả lời câu hỏi
                llm = genai.GenerativeModel('gemini-1.5-flash')  # Model Gemini bạn sử dụng
                response = llm.generate_content(prompt)
                
                st.write("### 📢 Trả lời từ Chatbot:")
                st.success(response.text)
            except Exception as e:
                st.error(f"Lỗi kết nối API Gemini: {e}")
    else:
        st.warning("Vui lòng tải lên một file PDF CV.")