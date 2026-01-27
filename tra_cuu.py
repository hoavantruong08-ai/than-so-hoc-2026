import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 
st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# Hàm làm sạch tuyệt đối: Coi tất cả là chuỗi ký tự, bỏ dấu, bỏ cách, bỏ mọi ký tự lạ
def clean_id(text):
    if not text or str(text) == "nan": return ""
    # Chuyển về dạng chuẩn để tách dấu
    text = unicodedata.normalize('NFD', str(text))
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    text = text.replace('đ', 'd').replace('Đ', 'D')
    # Chỉ giữ lại chữ cái và số (biến ngày sinh thành chuỗi số định danh)
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

name_in = st.text_input("Nhập Họ và Tên (viết liền hoặc có dấu đều được):")
dob_in = st.text_input("Nhập Mã Ngày Sinh (ví dụ: 26031990):")

if st.button("Tra cứu ngay"):
    if name_in and dob_in:
        try:
            # Đọc dữ liệu mới nhất (ttl=0)
            df = conn.read(ttl=0)
            
            # Ép kiểu toàn bộ bảng về String để xử lý như chuỗi định danh
            df = df.astype(str)
            
            # Tạo bản sao để đối soát (clean ID)
            # Cột 0: Họ Tên, Cột 1: Ngày Sinh
            df['name_id'] = df.iloc[:, 0].apply(clean_id)
            df['dob_id'] = df.iloc[:, 1].apply(clean_id)
            
            search_name = clean_id(name_in)
            search_dob = clean_id(dob_in)
            
            # Tìm kiếm dòng khớp cả 2 mã định danh
            match = df[(df['name_id'] == search_name) & (df['dob_id'] == search_dob)]
            
            if not match.empty:
                st.success(f"Kết quả cho: **{match.iloc[0, 0]}**")
                c1, c2 = st.columns(2)
                # Lấy dữ liệu ở cột D (chỉ mục 3) và E (chỉ mục 4)
                c1.metric("Số Chủ Đạo", match.iloc[0, 3])
                c2.metric("Số Định Mệnh", match.iloc[0, 4])
            else:
                st.error("❌ Không tìm thấy thông tin. Hãy kiểm tra lại dữ liệu trong Sheet!")
                with st.expander("Dữ liệu đối soát (Debug)"):
                    st.write("Mã bạn nhập:", search_name, "|", search_dob)
                    st.write("Mã trong Sheet:", df['name_id'].iloc[0], "|", df['dob_id'].iloc[0])
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")
