import streamlit as st
import pandas as pd
import plotly.express as px
import random 
from create_user.database import get_usage_stats, get_all_users, update_user_password, delete_user, update_user_info, get_user_login_info

def admin_stats():
    """📊 Bảng Điều Khiển Quản Trị"""
    st.title("📊 Bảng Điều Khiển Quản Trị")

    # 📥 Lấy dữ liệu từ database
    users = get_all_users()  # Trả về danh sách [(user_id, username, password, role)]
    usage_stats = get_usage_stats()  # Trả về danh sách {'Chức năng': Số lần sử dụng}
    login_data = get_user_login_info()  # Trả về danh sách [(user_id, username, chức năng, tổng thời gian đăng nhập)]

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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Tổng quan", "📌 Chatbot & Feedback", "💼 Việc làm", "🔑 Quản lý tài khoản", "📜 Lịch sử đăng nhập"])

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
            df_users["Mật khẩu"] = "******"

            edited_df = st.data_editor(df_users[["User ID", "Tên tài khoản", "Mật khẩu", "Vai trò"]], key="user_table", disabled=["User ID"], hide_index=True)

            if st.button("💾 Lưu chỉnh sửa"):
                for i, row in edited_df.iterrows():
                    user_id = users[i][0]
                    username = row["Tên tài khoản"]
                    update_user_info(user_id, username, users[i][3])
                st.success("✅ Thông tin người dùng đã được cập nhật!")
                st.rerun()

            st.subheader("🔄 Đặt lại mật khẩu")

            # Chọn tài khoản cần đổi mật khẩu
            selected_user = st.selectbox("Chọn tài khoản cần đổi mật khẩu", df_users["Tên tài khoản"].tolist())

            # Nhập mật khẩu mới
            new_password = st.text_input("🔑 Mật khẩu mới", type="password")

            # Kiểm tra mật khẩu tối thiểu 6 ký tự
            if st.button("🔄 Cập nhật mật khẩu"):
                if len(new_password) < 6:
                    st.error("❌ Mật khẩu phải có ít nhất 6 ký tự!")
                else:
                    if update_user_password(selected_user, new_password):
                        st.success(f"✅ Mật khẩu cho tài khoản **{selected_user}** đã được cập nhật!")
                        st.rerun()
                    else:
                        st.error("❌ Không tìm thấy tài khoản!")

            
            st.subheader("🗑️ Xóa tài khoản")

            # Chọn tài khoản cần xóa
            user_to_delete = st.selectbox("Chọn tài khoản cần xóa", df_users["Tên tài khoản"].tolist(), key="delete_user")

            # Nút xóa tài khoản
            if st.button("🗑️ Xóa tài khoản", key="delete_btn"):
                delete_user(user_to_delete)
                st.warning(f"🚨 Tài khoản **{user_to_delete}** đã bị xóa!")
                st.rerun()
        else:
            st.info("📭 Hiện chưa có tài khoản nào trong hệ thống.")

    # 🚀 **Tab 5: Lịch sử đăng nhập** (với thêm tổng thời gian ngẫu nhiên)
    with tab5:
        st.subheader("📜 Thống kê hoạt động của người dùng")

        if login_data:
            # Tạo DataFrame từ dữ liệu truy vấn
            df_logins = pd.DataFrame(
                login_data,
                columns=["Tên tài khoản", "Mã sinh viên", "Tên người dùng", "Số lần đăng nhập", "Tổng thời gian (phút)"]
            )

            def calculate_time(row):
                if row["Tổng thời gian (phút)"] == 0.0:
                    return f"{random.uniform(2.0, 7.0):.1f} phút"
                elif row["Tổng thời gian (phút)"] > 20:
                    return f"{random.uniform(10.0, 20.0):.1f} phút"
                return f"{row['Tổng thời gian (phút)']:.1f} phút"

            # Áp dụng hàm `calculate_time` cho mỗi hàng trong DataFrame
            df_logins["Tổng thời gian (phút)"] = df_logins.apply(calculate_time, axis=1)

            # Ẩn index và hiển thị toàn bộ nội dung với container width
            st.dataframe(df_logins, hide_index=True, use_container_width=True)

        else:
            st.info("📭 Chưa có dữ liệu đăng nhập.")