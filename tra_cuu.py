import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 
st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

def clean_id(text):
    if not text or str(text) == "nan": return ""
    text = unicodedata.normalize('NFD', str(text))
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    text = text.replace('đ', 'd').replace('Đ', 'D')
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

if "client_auth" not in st.session_state:
    st.session_state["client_auth"] = False

if not st.session_state["client_auth"]:
    st.title("🔮 Cổng Tra Cứu")
    pwd = st.text_input("Mật khẩu:", type="password")
    if st.button("Truy cập"):
        if pwd == CLIENT_PASSWORD:
            st.session_state["client_auth"] = True
            st.rerun()
    st.stop()

# --- TRA CỨU ---
st.title("🔍 Tra Cứu Thần Số Học")
conn = st.connection("gsheets", type=GSheetsConnection)

name_in = st.text_input("Họ và Tên (Mặc định viết thường):")
dob_in = st.text_input("Ngày tháng năm sinh (Viết liền không dấu cách):")

if st.button("Tra cứu ngay"):
    if name_in and dob_in:
        try:
            df = conn.read(ttl=0)
            
            # Làm sạch ID để đối soát
            df['n_id'] = df.iloc[:, 0].astype(str).apply(clean_id)
            df['d_id'] = df.iloc[:, 1].astype(str).apply(clean_id)
            
            s_name = clean_id(name_in)
            s_dob = clean_id(dob_in)
            
            match = df[(df['n_id'] == s_name) & (df['d_id'] == s_dob)]
            
            if not match.empty:
                st.success(f"Kết quả cho: **{match.iloc[0, 0]}**")
                c1, c2 = st.columns(2)
                
                # --- ĐOẠN FIX LỖI SỐ .0 ---
                # Ép kiểu dữ liệu về chuỗi, sau đó bỏ phần thập phân .0 nếu có
                scd = str(match.iloc[0, 3]).replace('.0', '')
                sdm = str(match.iloc[0, 4]).replace('.0', '')
                
                c1.metric("Số Chủ Đạo", scd)
                c2.metric("Số Định Mệnh", sdm)
                # -------------------------
                
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp.")
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")
