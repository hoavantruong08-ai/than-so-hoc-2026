import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re

# --- CẤU HÌNH ---
st.set_page_config(page_title="Thần Số Học", layout="wide")

# Hàm làm sạch dữ liệu để đối soát
def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8').lower()
    return re.sub(r'[^a-z0-9]', '', s)

if "role" not in st.session_state: st.session_state["role"] = None

# --- KẾT NỐI ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- ĐIỀU HƯỚNG ---
with st.sidebar:
    if st.session_state["role"] == "admin":
        menu = st.radio("Menu:", ["Tra cứu", "Up dữ liệu nguồn"])
        if st.button("Đăng xuất"): 
            st.session_state["role"] = None
            st.rerun()
    else: menu = "Tra cứu"

if menu == "Tra cứu":
    st.title("🔍 Tra Cứu")
    if st.session_state["role"] is None:
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.button("Vào"):
            if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
            if pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
        st.stop()

    # Đọc dữ liệu (Khách luôn xem được)
    df = conn.read(worksheet="Up_Data", ttl=0)
    n = st.text_input("Họ Tên:")
    d = st.text_input("Ngày sinh (8 số):")
    
    if st.button("Xem kết quả"):
        df['n_id'] = df.iloc[:,0].apply(clean_id)
        df['d_id'] = df.iloc[:,1].apply(str).str.strip()
        match = df[(df['n_id'] == clean_id(n)) & (df['d_id'].str.contains(d))]
        if not match.empty:
            st.success(f"Chào bạn {match.iloc[0,0]}!")
            st.write(f"Số chủ đạo: {match.iloc[0,3]}")
        else: st.error("Không tìm thấy!")

elif menu == "Up dữ liệu nguồn":
    st.title("➕ Thêm khách hàng")
    df_old = conn.read(worksheet="Up_Data", ttl=0)
    
    with st.form("update_form"):
        name = st.text_input("Họ tên:")
        dob = st.text_input("Ngày sinh (8 số):")
        scd = st.text_input("Số chủ đạo:")
        if st.form_submit_button("Lưu lên Sheets"):
            if name and dob:
                new_data = pd.DataFrame([{"Họ Tên": name, "Ngày Sinh": f"'{dob}", "Số Chủ Đạo": scd}])
                df_final = pd.concat([df_old, new_data], ignore_index=True)
                # Dùng hàm create để ghi đè toàn bộ bảng (Cách an toàn nhất của thư viện này)
                conn.create(worksheet="Up_Data", data=df_final)
                st.success("Đã cập nhật! Hãy đợi vài giây để hệ thống đồng bộ.")
                st.rerun()
