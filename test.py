import streamlit as st

# Kiểm tra nội dung và định dạng của dữ liệu trong session_state['user']
def check_user_format():
    if "user" not in st.session_state:
        st.session_state["user"] = {"user_id": "", "role": "student"}  # Dữ liệu mặc định nếu chưa có
    
    user_data = st.session_state["user"]  # Lấy dữ liệu user từ session_state
    
    # Kiểm tra và in kiểu dữ liệu của user_data
    st.write("Kiểu dữ liệu của session_state['user']: ", type(user_data))  # In kiểu dữ liệu
    
    # Kiểm tra nếu là dictionary
    if isinstance(user_data, dict):
        st.write("session_state['user'] là một dictionary.")
    else:
        st.write("session_state['user'] không phải là một dictionary.")
    
    # Kiểm tra nếu là tuple
    if isinstance(user_data, tuple):
        st.write("session_state['user'] là một tuple.")
    else:
        st.write("session_state['user'] không phải là một tuple.")
    
# Gọi hàm để kiểm tra
check_user_format()