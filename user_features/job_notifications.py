import streamlit as st
from create_user.database import get_jobs, track_usage
from user_features.job_chat import job_chatbot

def job_notifications():
    st.title("💼 Cơ hội Việc làm")
    col1, col2 = st.columns([3, 1])
    
    with col1:
        job_data = get_jobs()

        if not job_data:
            st.info("📭 Hiện chưa có việc làm nào được đăng tải.")
            return

        for record in job_data:
            job_id, title, company, requirements, salary, job_type, date, job_code = record
            expander_key = f"viewed_{job_code}"  # Chìa khóa session để kiểm tra xem đã ghi nhận chưa

            # Mặc định expander đóng
            with st.expander(f"📌 {title} #{job_code}", expanded=False):
                # Nếu chưa ghi nhận lượt xem thì mới cập nhật database
                if expander_key not in st.session_state:
                    track_usage(f"view_job_{job_code}")
                    st.session_state[expander_key] = True  # Đánh dấu đã ghi nhận

                st.markdown(f"**🏢 Công ty:** {company}")  
                st.write(f"**📅 Ngày đăng:** {date}")  
                st.write(f"**📂 Loại công việc:** {job_type}")  

                st.markdown("### 📌 Yêu cầu công việc")
                st.markdown(requirements.replace("•", "\n- "))  # Chuyển dấu "•" thành xuống dòng
                
                st.markdown("### 💰 Quyền lợi được hưởng")
                st.markdown(salary.replace("•", "\n- "))  

                st.divider()
    
    with col2:
        job_chatbot()  # Gọi chatbot vào phần cột bên phải