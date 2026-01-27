import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import unicodedata
import re

# --- KẾT NỐI (DÙNG GSPREAD) ---
def get_client():
    try:
        # Lấy thông tin từ mục [connections][gsheets] trong Secrets
        info = st.secrets["connections"]["gsheets"]
        scope = ['https://www.googleapis.com/auth/spreadsheets']
        creds = Credentials.from_service_account_info(info, scopes=scope)
        return gspread.authorize(creds)
    except Exception as e:
        st.error(f"Lỗi cấu hình Secrets: {e}")
        return None

def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode('utf-8').lower()
    return re.sub(r'[^a-z0-9]', '', s)

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Hệ Thống Thần Số", layout="wide")

if "role" not in st.session_state: st.session_state["role"] = None

# --- ĐIỀU HƯỚNG ---
with st.sidebar:
    if st.session_state["role"] == "admin":
        menu = st.radio("Menu:", ["Tra cứu", "Cập nhật dữ liệu", "Lịch sử"])
        if st.button("Đăng xuất"): st.session_state["role"] = None; st.rerun()
    else: menu = "Tra cứu"

client = get_client()
if client:
    try:
        # spreadsheet_id phải có trong Secrets
        sh = client.open_by_key(st.secrets["connections"]["gsheets"]["spreadsheet_id"])
        
        if menu == "Tra cứu":
            st.title("🔍 Tra Cứu")
            if st.session_state["role"] is None:
                pwd = st.text_input("Mật khẩu:", type="password")
                if st.button("Vào"):
                    if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
                    if pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
                st.stop()
            
            ws = sh.worksheet("Up_Data")
            df = pd.DataFrame(ws.get_all_records())
            n, d = st.text_input("Tên:"), st.text_input("Ngày sinh:")
            if st.button("Xem"):
                # So khớp dữ liệu
                df['n_id'] = df.iloc[:,0].apply(clean_id)
                df['d_id'] = df.iloc[:,1].apply(str).str.strip()
                match = df[(df['n_id'] == clean_id(n)) & (df['d_id'].str.contains(d))]
                if not match.empty:
                    st.success(f"Kết quả: {match.iloc[0,0]}")
                    st.write(f"Số chủ đạo: {match.iloc[0,3]}")
                else: st.error("Không tìm thấy!")

        elif menu == "Cập nhật dữ liệu":
            st.title("➕ Thêm khách hàng")
            ws_up = sh.worksheet("Up_Data")
            with st.form("add"):
                name = st.text_input("Họ tên:")
                dob = st.text_input("Ngày sinh (8 số):")
                phone = st.text_input("SĐT:")
                scd = st.text_input("SCD:")
                sdm = st.text_input("SDM:")
                if st.form_submit_button("Lưu lên Sheets"):
                    if name and dob:
                        ws_up.append_row([name, f"'{dob}", phone, scd, sdm], value_input_option='USER_ENTERED')
                        st.success("Đã thêm thành công!")
                    else: st.warning("Thiếu tên hoặc ngày sinh!")

    except Exception as e:
        st.error(f"Lỗi truy cập bảng tính: {e}")
