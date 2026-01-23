
import streamlit as st
import os
import base64

# 1. CẤU HÌNH TRANG
st.set_page_config(page_title="Thần Số Học 2026", layout="wide")

# Hàm mã hóa ảnh để làm nền (giúp App không bị trắng xóa)
def get_base64(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return None

# 2. THIẾT LẬP HÌNH NỀN "CÁI ĐĨA ĐEN" CỦA BẠN
file_nen = "Untitled-image_1.ico" 
bin_str = get_base64(file_nen)

if bin_str:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{bin_str}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 3. HIỂN THỊ THẦN TÀI Ở GIỮA
file_than_tai = "Than Tai 1.ico"
if os.path.exists(file_than_tai):
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(file_than_tai, width=250)
        st.markdown("<h2 style='text-align: center; color: gold;'>THẦN TÀI GÕ CỬA 2026</h2>", unsafe_allow_html=True)

# 4. SIDEBAR NHẬP LIỆU
with st.sidebar:
    st.header("🔮 THÔNG TIN")
    name = st.text_input("Họ và Tên")
    dob = st.date_input("Ngày sinh")
    if st.button("XEM KẾT QUẢ"):
        st.balloons()
        st.success(f"Chào {name}! Quẻ của bạn đang được gieo...")
