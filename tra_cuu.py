import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH & ẨN MENU QUẢN LÝ ---
st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# Đoạn mã CSS này sẽ ẩn: Menu (3 gạch), Nút Deploy, và Thanh Manager của Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            [data-testid="stToolbar"] {display: none;}
            [data-testid="stDecoration"] {display: none;}
            [data-testid="stStatusWidget"] {display: none;}
            #stConnectionStatus {display: none;}
            .stAppDeployButton {display: none !important;}
            /* Ẩn thanh quản lý dưới cùng của Streamlit Cloud */
            iframe[title="Manage app"] {display: none !important;}
            div[data-testid="stHeader"] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- 2. CÁC HÀM XỬ LÝ DỮ LIỆU ---
CLIENT_PASSWORD = "khachhang2026" 

def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    # Bù số 0 đầu nếu mã ngày sinh bị thiếu (ví dụ 02091997 chỉ còn 2091997)
    if s.isdigit() and len(s) == 7:
        s = "0" + s
    return s

# --- 3. KIỂM TRA ĐĂNG NHẬP ---
if "client_auth" not in st.session_state:
    st.session_state["client_auth"] = False

if not st.session_state["client_auth"]:
    st.title("🔮 Cổng Tra Cứu Thần Số Học")
    pwd = st.text_input("Mật khẩu:", type="password")
    if st.button("Truy cập"):
        if pwd == CLIENT_PASSWORD:
            st.session_state["client_auth"] = True
            st.rerun()
        else:
            st.error("Mật khẩu không đúng")
    st.stop()

# --- 4. GIAO DIỆN TRA CỨU ---
st.title("🔍 Tra Cứu Kết Quả")
conn = st.connection("gsheets", type=GSheetsConnection)

name_in = st.text_input("Họ và Tên (Mặc định viết thường):")
dob_in = st.text_input("Ngày tháng năm sinh (Ví dụ: 02091997):")

if st.button("Tra cứu ngay"):
    if name_in and dob_in:
        try:
            df = conn.read(ttl=0)
            df['n_match'] = df.iloc[:, 0].apply(clean_id)
            df['d_match'] = df.iloc[:, 1].apply(clean_id)
            
            s_name = clean_id(name_in)
            s_dob = clean_id(dob_in)
            
            match = df[(df['n_match'] == s_name) & (df['dob_match'] == s_dob)]
            
            if not match.empty:
                res_full_name = match.iloc[0, 0]
                st.success(f"Chào bạn **{res_full_name}**!")
                
                c1, c2 = st.columns(2)
                scd = str(match.iloc[0, 3]).split('.')[0]
                sdm = str(match.iloc[0, 4]).split('.')[0]
                
                c1.metric("Số Chủ Đạo", scd)
                c2.metric("Số Định Mệnh", sdm)

                # Ghi lịch sử
                try:
                    now_vn = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
                    new_log = pd.DataFrame([{
                        "Thời Gian Tra Cứu": now_vn,
                        "Họ Và Tên": res_full_name,
                        "Ngày Sinh": f"'{s_dob}", 
                        "Trạng Thái": "Thành công"
                    }])
                    history_df = conn.read(worksheet="History", ttl=0)
                    updated_history = pd.concat([history_df, new_log], ignore_index=True)
                    conn.update(worksheet="History", data=updated_history)
                except:
                    pass
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp.")
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")

if st.button("Thoát hệ thống"):
    st.session_state["client_auth"] = False
    st.rerun()
