import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import unicodedata
import os

# 1. CẤU HÌNH GIAO DIỆN
st.set_page_config(page_title="Thần Số Học 2026", layout="wide")

# 2. HIỂN THỊ ẢNH THẦN TÀI (Sử dụng file bạn đã upload)
# Lưu ý: Tên file phải khớp chính xác với file bạn đã upload
FILE_ANH = "Than Tai 1.ico" 

with st.sidebar:
    if os.path.exists(FILE_ANH):
        st.image(FILE_ANH, width=200)
    else:
        # Nếu chưa nhận file, dùng tạm ảnh thầy bói mặc định để app không lỗi
        st.image("https://cdn-icons-png.flaticon.com/512/1491/1491204.png", width=120)
    
    st.header("🔮 NHẬP THÔNG TIN")
    name = st.text_input("Họ và Tên")
    dob = st.date_input("Ngày sinh", datetime(1995, 1, 1))
    btn = st.button("XEM KẾT QUẢ")

# 3. LOGIC TÍNH TOÁN (Hệ Pythagoras)
def rut_gon(n):
    while n > 9 and n not in [11, 22, 33]: n = sum(int(d) for d in str(n))
    return n

if btn and name:
    # Tính số chủ đạo từ ngày sinh
    so_cd = rut_gon(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    
    st.balloons()
    st.markdown(f"""
        <div style="background: white; color: #1c1e21; padding: 30px; border-radius: 20px; border-left: 10px solid #7d5fff;">
            <h1 style="color: #7d5fff;">Số Chủ Đạo của bạn là: {so_cd}</h1>
            <p style="font-size: 1.2em;">Chúc mừng bạn! Năng lượng của con số {so_cd} sẽ dẫn lối bạn trong năm 2026.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Lưu vào Google Sheets (Nếu bạn đã kết nối)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        # Lệnh lưu dữ liệu của bạn ở đây...
    except:
        pass
