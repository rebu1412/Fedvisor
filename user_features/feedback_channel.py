import streamlit as st
from create_user.database import add_feedback, get_feedbacks, add_comment, get_comments, track_usage

def feedback_channel():
    st.title("💬 Kênh Góp Ý & Phản Hồi")

    if "user_id" not in st.session_state or not st.session_state["user_id"]:
        st.warning("⚠ Bạn cần đăng nhập để gửi phản hồi.")
        return

    user_id = st.session_state["user_id"]
    username = st.session_state["username"]

    # Form gửi phản hồi
    with st.form("feedback_form"):
        topic = st.text_input("📌 Chủ đề góp ý")
        content = st.text_area("✍️ Nội dung góp ý")
        submit = st.form_submit_button("Gửi Phản Hồi")

        if submit:
            if topic and content:
                add_feedback(user_id, topic, content)
                track_usage("feedback_submitted")  # Ghi nhận đăng bài
                st.success("✅ Gửi phản hồi thành công!")
                st.rerun()
            else:
                st.error("⚠ Vui lòng nhập đầy đủ thông tin!")

    st.subheader("📜 Danh sách phản hồi")

    feedbacks = get_feedbacks()
    if not feedbacks:
        st.info("📭 Chưa có phản hồi nào.")
        return

    for feedback in feedbacks:
        post_id, author, topic, content, created_at = feedback

        with st.expander(f"📌 {topic} - {created_at}"):
            st.write(f"**✍️ Người đăng:** {author}")
            st.markdown(f"📜 **Nội dung:**\n\n{content}")

            # Hiển thị bình luận
            comments = get_comments(post_id)
            for comment in comments:
                _, _, commenter, comment_content, comment_date = comment
                st.markdown(f"🗨 **{commenter}:** {comment_content} *(🕒 {comment_date})*")

            # Form thêm bình luận
            with st.form(f"comment_form_{post_id}"):
                comment_text = st.text_area("💬 Viết bình luận", key=f"comment_{post_id}")
                submit_comment = st.form_submit_button("Gửi")

                if submit_comment:
                    if comment_text:
                        add_comment(user_id, post_id, comment_text)
                        track_usage("comment_submitted")  # Ghi nhận đăng bình luận
                        st.success("✅ Bình luận đã được gửi!")
                        st.rerun()
                    else:
                        st.error("⚠ Nội dung bình luận không được để trống!")