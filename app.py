import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Thần Số Học", layout="wide")

# Hàm xử lý tên để đối soát chính xác
def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8').lower()
    return re.sub(r'[^a-z0-9]', '', s)

# --- KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- PHẦN TRA CỨU CỦA KHÁCH HÀNG ---
st.title("🔮 Hệ Thống Tra Cứu Thần Số Học")

# Nhập mật khẩu để vào
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    pwd = st.text_input("Mật khẩu truy cập:", type="password")
    if st.button("Vào hệ thống"):
        if pwd == "khachhang2026" or pwd == "admin2026":
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Mật khẩu không đúng!")
    st.stop()

# Giao diện tra cứu
n_in = st.text_input("Nhập Họ và Tên:")
d_in = st.text_input("Nhập Ngày sinh (Ví dụ: 02091997):")

if st.button("Xem kết quả"):
    try:
        # Đọc dữ liệu từ Sheet
        df = conn.read(worksheet="Up_Data", ttl=0)
        
        # Xử lý ID để so khớp
        df['n_id'] = df.iloc[:, 0].apply(clean_id)
        df['d_id'] = df.iloc[:, 1].apply(str).str.strip()
        
        # Tìm kiếm
        match = df[(df['n_id'] == clean_id(n_in)) & (df['d_id'].str.contains(d_in))]
        
        if not match.empty:
            st.success(f"Chào bạn **{match.iloc[0, 0]}**!")
            c1, c2 = st.columns(2)
            c1.metric("Số Chủ Đạo", str(match.iloc[0, 3]).split('.')[0])
            c2.metric("Số Định Mệnh", str(match.iloc[0, 4]).split('.')[0])
        else:
            st.error("Không tìm thấy thông tin phù hợp!")
    except Exception as e:
        st.error(f"Lỗi kết nối dữ liệu: {e}")
