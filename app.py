import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH & ẨN MENU ---
st.set_page_config(page_title="Quản Lý Thần Số Học", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
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

# --- 3. ĐIỀU HƯỚNG ---
if "role" not in st.session_state:
    st.session_state["role"] = None

with st.sidebar:
    if st.session_state["role"] == "admin":
        st.title("🛡️ ADMIN PANEL")
        menu = st.radio("Chức năng:", ["Tra cứu", "Thêm dữ liệu nguồn", "Xem danh sách & Lịch sử"])
        if st.button("Đăng xuất"):
            st.session_state["role"] = None
            st.rerun()
    else:
        menu = "Tra cứu"

# --- 4. TRANG TRA CỨU ---
if menu == "Tra cứu":
    st.title("🔮 Tra Cứu Thần Số Học")
    if st.session_state["role"] is None:
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.button("Truy cập"):
            if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
            if pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
            st.error("Sai mật khẩu!")
        st.stop()

    conn = st.connection("gsheets", type=GSheetsConnection)
    name_in = st.text_input("Họ và Tên:")
    dob_in = st.text_input("Ngày sinh (ví dụ: 02091997):")
    
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
            
            # Ghi sử (History)
            try:
                hist = conn.read(worksheet="History", ttl=0)
                new_h = pd.DataFrame([{"Thời Gian Tra Cứu": (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S"), "Họ Và Tên": match.iloc[0, 0], "Ngày Sinh": f"'{s_dob}", "Trạng Thái": "Thành công"}])
                conn.create(worksheet="History", data=pd.concat([hist, new_h], ignore_index=True))
            except: pass
        else: st.error("Không tìm thấy dữ liệu!")

# --- 5. TRANG THÊM DỮ LIỆU (UP THÔNG TIN NGUỒN) ---
elif menu == "Thêm dữ liệu nguồn":
    st.title("➕ Thêm Khách Hàng Mới")
    st.info("Dữ liệu sẽ được thêm trực tiếp vào tab Up_Data")
    
    with st.form("add_form"):
        new_name = st.text_input("Họ và Tên khách hàng:")
        new_dob = st.text_input("Mã Ngày sinh (8 số, ví dụ: 01011990):")
        new_phone = st.text_input("Số điện thoại (nếu có):")
        new_scd = st.text_input("Số Chủ Đạo:")
        new_sdm = st.text_input("Số Định Mệnh:")
        submit_add = st.form_submit_button("Cập nhật vào hệ thống")
    
    if submit_add:
        if new_name and new_dob and new_scd and new_sdm:
            try:
                conn = st.connection("gsheets", type=GSheetsConnection)
                df_origin = conn.read(worksheet="Up_Data", ttl=0)
                
                new_entry = pd.DataFrame([{
                    "Họ Tên": new_name,
                    "Ngày Sinh": f"'{new_dob}", # Dấu nháy để giữ số 0 đầu
                    "SĐT": new_phone,
                    "Số Chủ Đạo": new_scd,
                    "Số Định Mệnh": new_sdm
                }])
                
                updated_df = pd.concat([df_origin, new_entry], ignore_index=True)
                conn.create(worksheet="Up_Data", data=updated_df)
                st.success(f"Đã thêm thành công khách hàng: {new_name}")
            except Exception as e:
                st.error(f"Lỗi khi up dữ liệu: {e}")
        else:
            st.warning("Vui lòng nhập đủ các thông tin chính.")

# --- 6. XEM DANH SÁCH & LỊCH SỬ ---
elif menu == "Xem danh sách & Lịch sử":
    st.title("📊 Quản Lý Dữ Liệu")
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    tab1, tab2 = st.tabs(["Dữ liệu nguồn (Up_Data)", "Lịch sử tra cứu (History)"])
    
    with tab1:
        st.dataframe(conn.read(worksheet="Up_Data", ttl=0), use_container_width=True)
    with tab2:
        st.dataframe(conn.read(worksheet="History", ttl=0), use_container_width=True)
