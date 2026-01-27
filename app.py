import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re

# --- CẤU HÌNH ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# Ẩn các thanh công cụ của Streamlit
st.markdown("""<style>#MainMenu, footer, header, .stDeployButton {visibility: hidden;} [data-testid="stToolbar"] {display: none;}</style>""", unsafe_allow_html=True)

def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn']).replace('đ', 'd').replace('Đ', 'D')
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    if s.isdigit() and len(s) == 7: s = "0" + s
    return s

# --- PHÂN QUYỀN ---
if "role" not in st.session_state: st.session_state["role"] = None

with st.sidebar:
    if st.session_state["role"] == "admin":
        st.header("⚡ ADMIN MENU")
        page = st.radio("Chức năng:", ["Tra cứu", "Danh sách Up_Data", "Nhật ký History"])
        if st.button("Đăng xuất"):
            st.session_state["role"] = None
            st.rerun()
    else:
        page = "Tra cứu"

# --- LOGIC TRANG ---
conn = st.connection("gsheets", type=GSheetsConnection)

if page == "Tra cứu":
    st.title("🔍 Tra Cứu Kết Quả")
    if st.session_state["role"] is None:
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.button("Truy cập"):
            if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
            if pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
            st.error("Sai mật khẩu!")
        st.stop()

    name_in = st.text_input("Nhập Họ và Tên:")
    dob_in = st.text_input("Nhập Ngày sinh (Ví dụ: 02091997):")
    
    if st.button("Xem kết quả"):
        df = conn.read(worksheet="Up_Data", ttl=0)
        df['n_id'] = df.iloc[:, 0].apply(clean_id)
        df['d_id'] = df.iloc[:, 1].apply(clean_id)
        match = df[(df['n_id'] == clean_id(name_in)) & (df['d_id'] == clean_id(dob_in))]
        
        if not match.empty:
            st.success(f"Chào bạn **{match.iloc[0, 0]}**!")
            c1, c2 = st.columns(2)
            c1.metric("Số Chủ Đạo", str(match.iloc[0, 3]).split('.')[0])
            c2.metric("Số Định Mệnh", str(match.iloc[0, 4]).split('.')[0])
        else:
            st.error("Không tìm thấy thông tin phù hợp!")

elif page == "Danh sách Up_Data":
    st.title("📂 Dữ Liệu Nguồn (Xem)")
    st.info("💡 Để thêm khách hàng, hãy nhập trực tiếp vào file Google Sheets.")
    st.dataframe(conn.read(worksheet="Up_Data", ttl=0), use_container_width=True)

elif page == "Nhật ký History":
    st.title("📋 Lịch Sử Tra Cứu")
    st.dataframe(conn.read(worksheet="History", ttl=0), use_container_width=True)
