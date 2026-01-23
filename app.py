import streamlit as st
import os

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Thần Số Học 2026", layout="wide")

# 2. CODE CHÈN HÌNH NỀN (Tự động canh chỉnh cho đẹp)
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://img.freepik.com/free-vector/mystical-astrology-background-with-zodiac-signs_23-2148425501.jpg");
        background-attachment: fixed;
        background-size: cover;
    }
    /* Làm cho các ô nhập liệu dễ nhìn hơn trên nền ảnh */
    .stTextInput, .stDateInput, .stButton {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 10px;
        padding: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. HIỂN THỊ ẢNH THẦN TÀI TRONG SIDEBAR
with st.sidebar:
    # Thử tìm file bạn đã upload, nếu không thấy thì dùng ảnh mặc định
    if os.path.exists("Than Tai 1.ico"):
        st.image("Than Tai 1.ico", width=200)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/1491/1491204.png", width=120)
    
    st.header("🔮 THÔNG TIN CỦA BẠN")
    name = st.text_input("Nhập Họ và Tên")
    dob = st.date_input("Chọn Ngày sinh")
    gui = st.button("XEM KẾT QUẢ NGAY")

# 4. PHẦN HIỂN THỊ KẾT QUẢ
if gui and name:
    st.balloons()
    st.success(f"Chào {name}! App của bạn đã hoạt động với hình nền mới!")
