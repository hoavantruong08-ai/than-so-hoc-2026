import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 
st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# Hàm làm sạch ID: Ép về văn bản, bỏ dấu .0 và mọi ký tự không phải số/chữ
def clean_id(text):
    if not text or str(text) == "nan": return ""
    # Chuyển sang chuỗi, loại bỏ phần thập phân .0 nếu Google Sheets tự thêm vào
    s = str(text).split('.')[0] 
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    # Chỉ giữ lại chữ cái và số
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

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
dob_in = st.text_input("Ngày tháng năm sinh (Ví dụ: 26031990):")

if st.button("Tra cứu ngay"):
    if name_in and dob_in:
        try:
            # Luôn đọc dữ liệu mới nhất
            df = conn.read(ttl=0)
            
            # Xử lý dữ liệu đối soát
            # Ép cột Tên (0) và cột Ngày sinh (1) về dạng ID sạch
            df['name_match'] = df.iloc[:, 0].apply(clean_id)
            df['dob_match'] = df.iloc[:, 1].apply(clean_id)
            
            s_name = clean_id(name_in)
            s_dob = clean_id(dob_in)
            
            match = df[(df['name_match'] == s_name) & (df['dob_match'] == s_dob)]
            
            if not match.empty:
                st.success(f"Kết quả cho: **{match.iloc[0, 0]}**")
                c1, c2 = st.columns(2)
                
                # Hiển thị kết quả Số Chủ Đạo (cột 3) và Số Định Mệnh (cột 4)
                # Dùng clean_id để xóa luôn dấu .0 ở kết quả hiển thị cho đẹp
                scd = clean_id(match.iloc[0, 3]).upper()
                sdm = clean_id(match.iloc[0, 4]).upper()
                
                c1.metric("Số Chủ Đạo", scd)
                c2.metric("Số Định Mệnh", sdm)
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp.")
                with st.expander("Kiểm tra mã đối soát"):
                    st.write("Mã bạn nhập:", s_name, "|", s_dob)
                    st.write("Mã trong Sheet:", df['name_match'].iloc[0], "|", df['dob_match'].iloc[0])
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")
