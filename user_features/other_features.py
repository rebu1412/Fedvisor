import streamlit as st

# Function to display the upcoming features
def other_features():
    features = [
        {
            'title': 'Học nhóm trực tuyến',
            'description': 'Tính năng học nhóm trực tuyến sẽ giúp bạn kết nối với các sinh viên khác trong cùng lĩnh vực học tập. Tham gia các nhóm học tập chuyên biệt để trao đổi kiến thức, hỗ trợ giải đáp thắc mắc và cải thiện kết quả học tập của mình. Đừng bỏ lỡ cơ hội kết nối với những người có cùng chí hướng và tạo ra một cộng đồng học tập mạnh mẽ.',
            'usage': 'Để sử dụng, bạn chỉ cần đăng nhập vào tài khoản Fedvisor và tìm nhóm học theo môn học của mình. Bạn có thể tham gia các nhóm này để thảo luận và học tập cùng nhau.',
            'date': 'Dự kiến ra mắt: Tháng 6, 2025'
        },
        {
            'title': 'Nhắc nhở thông minh',
            'description': 'Với tính năng nhắc nhở thông minh, bạn sẽ không bao giờ bỏ lỡ những mốc quan trọng trong học tập và sự nghiệp. Từ hạn đăng ký môn học, hạn nộp bài, đến các buổi phỏng vấn việc làm, Fedvisor sẽ tự động nhắc nhở bạn đúng lúc, giúp bạn luôn chủ động và không bị thiếu sót.',
            'usage': 'Fedvisor sẽ gửi thông báo nhắc nhở qua email hoặc thông qua ứng dụng mỗi khi có mốc thời gian quan trọng sắp đến. Bạn có thể tuỳ chỉnh các mốc thời gian cần nhắc nhở trong phần cài đặt tài khoản.',
            'date': 'Dự kiến ra mắt: Tháng 7, 2025'
        },
        {
            'title': 'Phát triển kỹ năng mềm',
            'description': 'Cải thiện kỹ năng giao tiếp, làm việc nhóm và giải quyết vấn đề là một phần không thể thiếu trong quá trình phát triển nghề nghiệp. Fedvisor sẽ cung cấp các khóa học và thử thách nhỏ để giúp bạn phát triển kỹ năng mềm ngay trong quá trình học tập, chuẩn bị cho tương lai nghề nghiệp của mình.',
            'usage': 'Để sử dụng tính năng này, bạn có thể đăng nhập vào Fedvisor, chọn mục "Kỹ năng mềm" và tham gia các khóa học hoặc thử thách. Các bài học sẽ được thiết kế theo từng mức độ và bạn có thể chọn lựa theo nhu cầu của mình.',
            'date': 'Dự kiến ra mắt: Tháng 8, 2025'
        }
    ]

    # Streamlit UI for displaying features
    st.title("Các tính năng mới sắp ra mắt của Fedvisor")

    for feature in features:
        st.subheader(feature['title'])
        st.markdown(f"**Mô tả tính năng:** {feature['description']}")
        st.markdown(f"**Hướng dẫn sử dụng:** {feature['usage']}")
        st.markdown(f"**Thời gian dự kiến ra mắt:** {feature['date']}")
        st.write("---")