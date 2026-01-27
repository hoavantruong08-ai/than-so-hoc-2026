import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH & ẨN MENU QUẢN LÝ ---
st.set_page_config(page_title="Hệ Thống Thần Số Học 2026", page_icon="🔮", layout="wide")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            [data-testid="stToolbar"] {display: none;}
            .stAppDeployButton {display: none !important;}
            iframe[title="Manage app"] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

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

# --- 3. ĐIỀU HƯỚNG MENU (Sidebar ẩn) ---
if "role" not in st.session_state:
    st.session_state["role"] = None

# Sidebar để chuyển đổi (Chỉ hiện khi đã đăng nhập Admin)
with st.sidebar:
    if st.session_state["role"] == "admin":
        st.title("⚡ Quản Trị")
        page = st.radio("Chọn chức năng:", ["Tra cứu (Khách)", "Dữ liệu nguồn (Admin)", "Lịch sử tra cứu"])
        if st.button("Đăng xuất Admin"):
            st.session_state["role"] = None
            st.rerun()
    else:
        page = "Tra cứu (Khách)"

# --- 4. TRANG TRA CỨU CHO KHÁCH ---
if page == "Tra cứu (Khách)":
    st.title("🔮 Cổng Tra Cứu Thần Số Học")
    
    # Đăng nhập khách (nếu chưa có role)
    if st.session_state["role"] is None:
        pwd = st.text_input("Nhập mật khẩu truy cập:", type="password")
        col_btn1, col_btn2 = st.columns(2)
        if col_btn1.button("Vào Tra Cứu"):
            if pwd == "khachhang2026":
                st.session_state["role"] = "user"
                st.rerun()
            elif pwd == "admin2026": # MẬT KHẨU ADMIN RIÊNG
                st.session_state["role"] = "admin"
                st.rerun()
            else:
                st.error("Sai mật khẩu!")
        st.stop()

    # Giao diện tra cứu
    conn = st.connection("gsheets", type=GSheetsConnection)
    with st.form("search_form"):
        name_in = st.text_input("Họ và Tên (viết thường):")
        dob_in = st.text_input("Mã Ngày Sinh (Ví dụ: 02091997):")
        submitted = st.form_submit_button("Tra cứu ngay")

    if submitted:
        try:
            df = conn.read(ttl=0)
            df['n_match'] = df.iloc[:, 0].apply(clean_id)
            df['d_match'] = df.iloc[:, 1].apply(clean_id)
            s_name, s_dob = clean_id(name_in), clean_id(dob_in)
            
            match = df[(df['n_match'] == s_name) & (df['d_match'] == s_dob)]
            
            if not match.empty:
                st.balloons()
                st.success(f"Chào bạn **{match.iloc[0, 0]}**!")
                c1, c2 = st.columns(2)
                scd = str(match.iloc[0, 3]).split('.')[0]
                sdm = str(match.iloc[0, 4]).split('.')[0]
                c1.metric("Số Chủ Đạo", scd)
                c2.metric("Số Định Mệnh", sdm)

                # Ghi History
                try:
                    now_vn = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
                    history_df = conn.read(worksheet="History", ttl=0)
                    new_log = pd.DataFrame([{"Thời Gian Tra Cứu": now_vn, "Họ Và Tên": match.iloc[0, 0], "Ngày Sinh": f"'{s_dob}", "Trạng Thái": "Thành công"}])
                    conn.create(worksheet="History", data=pd.concat([history_df, new_log], ignore_index=True))
                except: pass
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp.")
        except Exception as e:
            st.error(f"Lỗi: {e}")

# --- 5. TRANG QUẢN LÝ DỮ LIỆU NGUỒN (ADMIN) ---
elif page == "Dữ liệu nguồn (Admin)":
    st.title("📂 Quản Lý Dữ Liệu Nguồn (Up_Data)")
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_source = conn.read(worksheet="Up_Data", ttl=0)
    
    st.write(f"Tổng số khách hàng trong hệ thống: **{len(df_source)}**")
    
    search_admin = st.text_input("🔍 Tìm nhanh tên khách hàng:")
    if search_admin:
        df_filtered = df_source[df_source.iloc[:, 0].str.contains(search_admin, case=False, na=False)]
        st.dataframe(df_filtered, use_container_width=True)
    else:
        st.dataframe(df_source, use_container_width=True)
    
    st.info("💡 Để thêm hoặc sửa dữ liệu, bạn vui lòng thao tác trên file Google Sheets gốc.")

# --- 6. TRANG LỊCH SỬ TRA CỨU (ADMIN) ---
elif page == "Lịch sử tra cứu":
    st.title("📋 Nhật Ký Tra Cứu")
    conn = st.connection("gsheets", type=GSheetsConnection)
    df_history = conn.read(worksheet="History", ttl=0)
    
    st.metric("Tổng lượt tra cứu thành công", len(df_history))
    st.dataframe(df_history.sort_index(ascending=False), use_container_width=True)
    
    if st.button("Làm mới dữ liệu"):
        st.rerun()
