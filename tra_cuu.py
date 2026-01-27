import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 

st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# Hàm làm sạch văn bản: Bỏ dấu, bỏ khoảng trắng, về chữ thường
def ultra_clean(text):
    if not text or str(text) == "nan": return ""
    # Chuyển về dạng chuẩn NFD để tách dấu
    text = unicodedata.normalize('NFD', str(text))
    # Loại bỏ các ký tự dấu
    text = ''.join([c for c in text if unicodedata.category(c) != 'Mn'])
    # Xử lý riêng chữ đ/Đ
    text = text.replace('đ', 'd').replace('Đ', 'D')
    # Loại bỏ tất cả những gì không phải chữ và số, rồi viết thường
    return re.sub(r'[^a-zA-Z0-9]', '', text).lower()

if "client_auth" not in st.session_state:
    st.session_state["client_auth"] = False

if not st.session_state["client_auth"]:
    st.title("🔮 Cổng Tra Cứu")
    pwd = st.text_input("Mật khẩu truy cập:", type="password")
    if st.button("Truy cập"):
        if pwd == CLIENT_PASSWORD:
            st.session_state["client_auth"] = True
            st.rerun()
        else: st.error("Sai mật khẩu")
    st.stop()

# --- PHẦN TRA CỨU CHÍNH ---
st.title("🔍 Tra Cứu Thần Số Học")
conn = st.connection("gsheets", type=GSheetsConnection)

name_in = st.text_input("Nhập Họ và Tên (không cần dấu):")
dob_in = st.text_input("Nhập Ngày sinh (ví dụ: 26031990):")

if st.button("Tra cứu ngay"):
    if name_in and dob_in:
        try:
            # Ép App đọc dữ liệu mới nhất, không dùng cache
            df = conn.read(ttl=0)
            
            # Làm sạch dữ liệu trong Sheet để đối soát
            # Cột 0 là Họ Tên, Cột 1 là Ngày Sinh
            df['name_check'] = df.iloc[:, 0].apply(ultra_clean)
            df['dob_check'] = df.iloc[:, 1].apply(ultra_clean)
            
            # Làm sạch dữ liệu người dùng nhập
            search_name = ultra_clean(name_in)
            search_dob = ultra_clean(dob_in)
            
            # Thực hiện so khớp
            result = df[(df['name_check'] == search_name) & (df['dob_check'] == search_dob)]
            
            if not result.empty:
                st.success(f"Tìm thấy kết quả cho: **{result.iloc[0, 0]}**")
                col1, col2 = st.columns(2)
                # Cột 3 là Số Chủ Đạo, Cột 4 là Số Định Mệnh
                col1.metric("Số Chủ Đạo", result.iloc[0, 3])
                col2.metric("Số Định Mệnh", result.iloc[0, 4])
            else:
                st.error("❌ Không tìm thấy thông tin. Hãy kiểm tra lại dữ liệu trong Sheet!")
                # Debug ẩn để bạn tự kiểm tra
                with st.expander("Kiểm tra lỗi kỹ thuật"):
                    st.write("Dữ liệu bạn nhập đã làm sạch:", search_name, "|", search_dob)
                    st.write("Dòng đầu tiên trong Sheet đã làm sạch:", df['name_check'].iloc[0], "|", df['dob_check'].iloc[0])
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")
