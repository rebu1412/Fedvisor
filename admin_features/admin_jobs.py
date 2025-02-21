import streamlit as st
from create_user.database import add_job, get_jobs, update_job, delete_job

JOB_TYPES = ["full-time", "internship"]

def admin_jobs():
    st.subheader("📌 Quản lý Thông tin Việc Làm")

    # Thêm Việc làm mới
    with st.expander("➕ Thêm Việc làm mới"):
        job_code = st.text_input("🔢 Mã công việc (VD: EX1797)")
        title = st.text_input("📝 Tên công việc")
        company = st.text_input("🏢 Công ty")
        requirements = st.text_area("📌 Yêu cầu công việc")
        salary = st.text_area("💰 Đãi ngộ")
        job_type = st.selectbox("📂 Loại công việc", JOB_TYPES)

        if st.button("✅ Lưu Việc làm"):
            if job_code and title and company and requirements and job_type:
                add_job(title, company, requirements, salary, job_type, job_code)
                st.success(f"✅ Công việc {title} #{job_code} đã được thêm thành công!")
                st.rerun()
            else:
                st.error("⚠ Vui lòng nhập đầy đủ thông tin!")

    # Hiển thị danh sách việc làm
    st.subheader("📜 Danh sách Việc làm")
    job_data = get_jobs()

    for record in job_data:
        job_id, title, company, requirements, salary, job_type, date, job_code = record
        with st.expander(f"{title} #{job_code} - {company} ({date}) [{job_type}]"):
            new_job_code = st.text_input(f"🔢 Mã công việc ({job_id})", job_code)
            new_title = st.text_input(f"📝 Tên công việc ({job_id})", title)
            new_company = st.text_input(f"🏢 Công ty ({job_id})", company)
            new_requirements = st.text_area(f"📌 Yêu cầu ({job_id})", requirements)
            new_salary = st.text_area(f"💰 Đãi ngộ ({job_id})", salary)
            new_job_type = st.selectbox(f"📂 Loại công việc ({job_id})", JOB_TYPES, index=JOB_TYPES.index(job_type))

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"📝 Cập nhật ({job_id})"):
                    update_job(job_id, new_title, new_company, new_requirements, new_salary, new_job_type, new_job_code)
                    st.success(f"✅ Cập nhật thành công! {new_title} #{new_job_code}")
                    st.rerun()
            with col2:
                if st.button(f"🗑️ Xóa ({job_id})"):
                    delete_job(job_id)
                    st.warning(f"⚠ Đã xóa công việc {title} #{job_code}!")
                    st.rerun()
