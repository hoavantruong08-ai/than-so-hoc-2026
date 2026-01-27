import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH & CSS ---
st.set_page_config(page_title="Quản Lý Thần Số Học", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {display: none;}
    .stAppDeployButton {display: none !important;}
    iframe[title="Manage app"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM HỖ TRỢ ---
def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    if s.isdigit() and len(s) == 7:
        s = "0" + s
    return s

# --- 3. PHÂN QUYỀN TRUY CẬP ---
if "role" not in st.session_state:
    st.session_state["role"] = None

with st.sidebar:
    if st.session_state["role"] == "admin":
        st.header("⚡ ADMIN MENU")
        menu = st.radio("Chức năng:", ["Tra cứu khách", "Quản lý dữ liệu (Up_Data)", "Xem nhật ký (History)"])
        if st.button("Đăng xuất Admin"):
            st.session_state["role"] = None
            st.rerun()
    else:
        st.write("Vui lòng đăng nhập Admin để hiện thêm menu.")
        menu = "Tra cứu khách"

# --- 4. TRANG TRA CỨU (USER & ADMIN) ---
if menu == "Tra cứu khách":
    st.title("🔍 Tra Cứu Kết Quả")
    if st.session_state["role"] is None:
        pwd = st.text_input("Mật khẩu truy cập:", type="password")
        if st.button("Truy cập"):
            if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
            if pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
            st.error("Mật khẩu không đúng!")
        st.stop()

    conn = st.connection("gsheets", type=GSheetsConnection)
    with st.container():
        name_in = st.text_input("Nhập Họ và Tên:")
        dob_in = st.text_input("Nhập Ngày sinh (Ví dụ: 02091997):")
        
    if st.button("Tra cứu ngay"):
        df = conn.read(worksheet="Up_Data", ttl=0)
        df['n_id'] = df.iloc[:, 0].apply(clean_id)
        df['d_id'] = df.iloc[:, 1].apply(clean_id)
        s_name, s_dob = clean_id(name_in), clean_id(dob_in)
        
        match = df[(df['n_id'] == s_name) & (df['d_id'] == s_dob)]
        
        if not match.empty:
            st.success(f"Chào bạn **{match.iloc[0, 0]}**!")
            c1, c2 = st.columns(2)
            scd = str(match.iloc[0, 3]).split('.')[0]
            sdm = str(match.iloc[0, 4]).split('.')[0]
            c1.metric("Số Chủ Đạo", scd)
            c2.metric("Số Định Mệnh", sdm)
            
            # Ghi History an toàn
            try:
                hist_df = conn.read(worksheet="History", ttl=0)
                now_vn = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
                new_log = pd.DataFrame([{"Thời Gian Tra Cứu": now_vn, "Họ Và Tên": match.iloc[0, 0], "Ngày Sinh": f"'{s_dob}", "Trạng Thái": "Thành công"}])
                # Sử dụng create để cập nhật bảng
                conn.create(worksheet="History", data=pd.concat([hist_df, new_log], ignore_index=True))
            except: pass
        else:
            st.error("Không tìm thấy thông tin!")

# --- 5. TRANG QUẢN LÝ DỮ LIỆU NGUỒN (ADMIN ONLY) ---
elif menu == "Quản lý dữ liệu (Up_Data)":
    st.title("📂 Quản Lý Dữ Liệu Nguồn")
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Form thêm khách hàng mới
    with st.expander("➕ Thêm khách hàng mới", expanded=True):
        with st.form("add_client"):
            col1, col2 = st.columns(2)
            n_name = col1.text_input("Họ và Tên:")
            n_dob = col2.text_input("Ngày sinh (Mã 8 số):")
            n_phone = col1.text_input("SĐT (tùy chọn):")
            n_scd = col2.text_input("Số Chủ Đạo:")
            n_sdm = st.text_input("Số Định Mệnh:")
            btn_add = st.form_submit_button("Lưu vào Google Sheets")
            
        if btn_add:
            if n_name and n_dob:
                df_source = conn.read(worksheet="Up_Data", ttl=0)
                new_row = pd.DataFrame([{"Họ Tên": n_name, "Ngày Sinh": f"'{n_dob}", "SĐT": n_phone, "Số Chủ Đạo": n_scd, "Số Định Mệnh": n_sdm}])
                updated_df = pd.concat([df_source, new_row], ignore_index=True)
                conn.create(worksheet="Up_Data", data=updated_df)
                st.success(f"Đã thêm thành công {n_name}!")
                st.rerun()

    # Hiển thị và Tìm kiếm
    st.subheader("Danh sách hiện tại")
    df_view = conn.read(worksheet="Up_Data", ttl=0)
    search = st.text_input("Tìm kiếm tên trong danh sách:")
    if search:
        df_view = df_view[df_view.iloc[:, 0].str.contains(search, case=False, na=False)]
    st.dataframe(df_view, use_container_width=True)

# --- 6. XEM NHẬT KÝ ---
elif menu == "Xem nhật ký (History)":
    st.title("📋 Nhật Ký Tra Cứu")
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_hist = conn.read(worksheet="History", ttl=0)
    st.dataframe(df_hist.sort_index(ascending=False), use_container_width=True)
