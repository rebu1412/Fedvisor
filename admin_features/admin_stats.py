import streamlit as st
import pandas as pd
import plotly.express as px
from create_user.database import get_usage_stats, get_all_users, update_user_password, delete_user, update_user_info

import streamlit as st
import pandas as pd
import plotly.express as px
from create_user.database import get_usage_stats, get_all_users

def admin_stats():
    """📊 Bảng Điều Khiển Quản Trị"""
    st.title("📊 Bảng Điều Khiển Quản Trị")

    # 📥 Lấy dữ liệu từ database
    users = get_all_users()  # Trả về danh sách [(user_id, username, password, role)]
    usage_stats = get_usage_stats()  # Trả về danh sách {'Chức năng': Số lần sử dụng}

    # 🏆 Tổng số tài khoản
    total_users = len(users)
    total_usage = sum(usage_stats.values()) if usage_stats else 0
    login_count = usage_stats.get("Đăng nhập", 0)  # Lấy số lần đăng nhập từ key "Đăng nhập"

    # 📊 Hiển thị tổng quan
    st.subheader("📌 Tổng quan hệ thống")
    col1, col2, col3 = st.columns(3)  # Thêm một cột cho số lượt đăng nhập

    with col1:
        st.metric(label="👥 Tổng số tài khoản", value=total_users)

    with col2:
        st.metric(label="📊 Tổng số lượt sử dụng", value=total_usage)

    with col3:
        st.metric(label="🔑 Số lượt đăng nhập", value=login_count)  # Hiển thị số lần đăng nhập

    # Loại bỏ "Đăng nhập" khỏi dữ liệu vẽ biểu đồ
    usage_stats.pop("Đăng nhập", None)
    df_usage = pd.DataFrame(list(usage_stats.items()), columns=["Chức năng", "Số lần sử dụng"])

    # Tabs chia báo cáo theo từng nhóm
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Tổng quan", "📌 Chatbot & Feedback", "💼 Việc làm", "🔑 Quản lý tài khoản"])

    # 🚀 **Tab 1: Tổng quan với Biểu đồ**
    with tab1:
        st.subheader("📊 Biểu đồ thống kê sử dụng")
        if not df_usage.empty:
            # 🔹 Biểu đồ cột: Thống kê số lần sử dụng từng chức năng
            fig_bar = px.bar(df_usage, x="Chức năng", y="Số lần sử dụng",
                             title="🔍 Số lần sử dụng theo chức năng",
                             labels={"Số lần sử dụng": "Lượt sử dụng"},
                             color="Chức năng", height=400)
            st.plotly_chart(fig_bar, use_container_width=True)

            # 🔹 Biểu đồ tròn: Tỉ lệ sử dụng từng chức năng
            fig_pie = px.pie(df_usage, names="Chức năng", values="Số lần sử dụng",
                             title="📊 Tỉ lệ sử dụng các chức năng",
                             height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("📭 Chưa có dữ liệu thống kê.")


    # 🚀 **Tab 2: Chi tiết Chatbot & Feedback**
    with tab2:
        st.subheader("📌 Chi tiết Chatbot & Feedback")
        for key in ["Chatbot hành chính", "Chatbot công việc", "Feedback", "Comment"]:
            if key in usage_stats:
                st.markdown(f"- **{key}:** {usage_stats[key]} lần sử dụng")

    # 🚀 **Tab 3: Chi tiết Việc Làm**
    with tab3:
        st.subheader("💼 Chi tiết Xem thông tin Việc Làm")
        if "Xem thông tin việc làm" in usage_stats:
            st.markdown(f"- **Xem thông tin việc làm:** {usage_stats['Xem thông tin việc làm']} lần sử dụng")
        else:
            st.info("📭 Chưa có lượt xem việc làm nào.")

    # 🚀 **Tab 4: Quản lý tài khoản**
    with tab4:
        st.subheader("🔑 Quản lý tài khoản")
        if users:
            df_users = pd.DataFrame(users, columns=["User ID", "Tên tài khoản", "Mật khẩu", "Vai trò"])

            # 🔒 Ẩn mật khẩu (hiển thị ****)
            df_users["Mật khẩu"] = "******"

            # Hiển thị bảng có thể chỉnh sửa (Chỉ cho phép sửa tên tài khoản)
            edited_df = st.data_editor(df_users[["User ID", "Tên tài khoản", "Mật khẩu", "Vai trò"]], key="user_table", disabled=["User ID"], hide_index=True)

            # 📝 Cập nhật thông tin người dùng
            if st.button("💾 Lưu chỉnh sửa"):
                for i, row in edited_df.iterrows():
                    user_id = users[i][0]
                    username = row["Tên tài khoản"]
                    update_user_info(user_id, username, users[i][3])  # Giữ nguyên vai trò
                st.success("✅ Thông tin người dùng đã được cập nhật!")
                st.rerun()

            # 🔄 Cập nhật mật khẩu
            st.subheader("🔄 Đặt lại mật khẩu")
            selected_user = st.selectbox("Chọn tài khoản cần đổi mật khẩu", df_users["Tên tài khoản"].tolist())
            new_password = st.text_input("🔑 Mật khẩu mới", type="password")
            if st.button("🔄 Cập nhật mật khẩu"):
                user_id = df_users[df_users["Tên tài khoản"] == selected_user]["User ID"].values[0]
                update_user_password(user_id, new_password)
                st.success(f"✅ Mật khẩu cho tài khoản **{selected_user}** đã được cập nhật!")
                st.rerun()

            # 🗑️ Xóa tài khoản
            st.subheader("🗑️ Xóa tài khoản")
            user_to_delete = st.selectbox("Chọn tài khoản cần xóa", df_users["Tên tài khoản"].tolist(), key="delete_user")
            if st.button("🗑️ Xóa tài khoản", key="delete_btn"):
                user_id = df_users[df_users["Tên tài khoản"] == user_to_delete]["User ID"].values[0]
                delete_user(user_id)
                st.warning(f"🚨 Tài khoản **{user_to_delete}** đã bị xóa!")
                st.rerun()

        else:
            st.info("📭 Hiện chưa có tài khoản nào trong hệ thống.")
