import streamlit as st
from create_user.database import get_feedbacks, delete_feedback

def admin_feedback():
    st.title("🛠 Quản Lý Góp Ý & Phản Hồi")

    feedbacks = get_feedbacks()
    if not feedbacks:
        st.info("📭 Hiện chưa có phản hồi nào.")
        return

    for feedback in feedbacks:
        post_id, author, topic, content, created_at = feedback

        with st.expander(f"📌 {topic} - {created_at}"):
            st.write(f"**✍️ Người đăng:** {author}")
            st.markdown(f"📜 **Nội dung:**\n\n{content}")

            if st.button(f"🗑 Xóa phản hồi", key=f"delete_{post_id}"):
                delete_feedback(post_id)
                st.warning("⚠ Phản hồi đã bị xóa!")
                st.rerun()
