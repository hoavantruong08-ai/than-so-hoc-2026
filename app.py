import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH & CSS ---
st.set_page_config(page_title="Hệ Thống Thần Số Học", page_icon="🔮", layout="wide")

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

# --- 2. HÀM XỬ LÝ ---
def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    if s.isdigit() and len(s) == 7: s = "0" + s
    return s

# Hàm ghi dữ liệu siêu bền (Thử tất cả các hàm có thể có của thư viện)
def super_save(conn, worksheet_name, data_df):
    try:
        # Cách 1: Dùng update (Phổ biến nhất)
        conn.update(worksheet=worksheet_name, data=data_df)
    except Exception:
        try:
            # Cách 2: Dùng create (Dành cho bản mới)
            conn.create(worksheet=worksheet_name, data=data_df)
        except Exception as e:
            st.error(f"⚠️ Lỗi kỹ thuật Google Sheets: {e}")
            st.info("Mẹo: Hãy đảm bảo bạn đã Share quyền 'Editor' cho file Sheet.")

# --- 3. PHÂN QUYỀN ---
if "role" not in st.session_state:
    st.session_state["role"] = None

with st.sidebar:
    if st.session_state["role"] == "admin":
        st.header("⚡ QUẢN TRỊ")
        menu = st.radio("Chức năng:", ["Tra cứu", "Quản lý Up_Data", "Nhật ký History"])
        if st.button("Đăng xuất Admin"):
            st.session_state["role"] = None
            st.rerun()
    else:
        menu = "Tra cứu"

# --- 4. TRANG TRA CỨU ---
if menu == "Tra cứu":
    st.title("🔍 Tra Cứu Kết Quả")
    if st.session_state["role"] is None:
        pwd = st.text_input("Nhập mật khẩu:", type="password")
        if st.button("Vào hệ thống"):
            if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
            if pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
            st.error("Sai mật khẩu!")
        st.stop()

    conn = st.connection("gsheets", type=GSheetsConnection)
    n_in = st.text_input("Họ và Tên:")
    d_in = st.text_input("Mã Ngày sinh (8 số):")
    
    if st.button("Tra cứu ngay"):
        df = conn.read(worksheet="Up_Data", ttl=0)
        df['n_id'] = df.iloc[:, 0].apply(clean_id)
        df['d_id'] = df.iloc[:, 1].apply(clean_id)
        match = df[(df['n_id'] == clean_id(n_in)) & (df['d_id'] == clean_id(d_in))]
        
        if not match.empty:
            st.success(f"Chào bạn **{match.iloc[0, 0]}**!")
            c1, c2 = st.columns(2)
            c1.metric("Số Chủ Đạo", str(match.iloc[0, 3]).split('.')[0])
            c2.metric("Số Định Mệnh", str(match.iloc[0, 4]).split('.')[0])
            try:
                hist_df = conn.read(worksheet="History", ttl=0)
                new_log = pd.DataFrame([{"Thời Gian Tra Cứu": (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S"), "Họ Và Tên": match.iloc[0, 0], "Ngày Sinh": f"'{clean_id(d_in)}", "Trạng Thái": "Thành công"}])
                super_save(conn, "History", pd.concat([hist_df, new_log], ignore_index=True))
            except: pass
        else: st.error("Không tìm thấy dữ liệu!")

# --- 5. TRANG QUẢN LÝ ---
elif menu == "Quản lý Up_Data":
    st.title("📂 Cập Nhật Dữ Liệu Nguồn")
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    with st.expander("➕ Thêm khách hàng mới", expanded=True):
        with st.form("admin_add_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Họ Tên:")
            dob = c2.text_input("Ngày sinh (8 số):")
            phone = c1.text_input("SĐT:")
            scd = c2.text_input("Số Chủ Đạo:")
            sdm = st.text_input("Số Định Mệnh:")
            btn = st.form_submit_button("Lưu lên Google Sheets")
            
        if btn:
            if name and dob:
                df_old = conn.read(worksheet="Up_Data", ttl=0)
                new_row = pd.DataFrame([{"Họ Tên": str(name), "Ngày Sinh": f"'{str(dob)}", "SĐT": str(phone), "Số Chủ Đạo": str(scd), "Số Định Mệnh": str(sdm)}])
                super_save(conn, "Up_Data", pd.concat([df_old, new_row], ignore_index=True))
                st.success(f"Đã lưu thành công: {name}")
                st.rerun()

    st.subheader("Danh sách hiện có")
    st.dataframe(conn.read(worksheet="Up_Data", ttl=0), use_container_width=True)

# --- 6. NHẬT KÝ ---
elif menu == "Nhật ký History":
    st.title("📋 Lịch Sử Tra Cứu")
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.dataframe(conn.read(worksheet="History", ttl=0).sort_index(ascending=False), use_container_width=True)
