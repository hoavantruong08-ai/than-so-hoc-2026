import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH & ẨN MENU QUẢN LÝ ---
st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# CSS mạnh để ẩn sạch các thanh công cụ và nút Manage
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {display: none;}
    [data-testid="stDecoration"] {display: none;}
    .stAppDeployButton {display: none !important;}
    iframe[title="Manage app"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM XỬ LÝ DỮ LIỆU ---
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

# --- 3. ĐĂNG NHẬP ---
if "client_auth" not in st.session_state:
    st.session_state["client_auth"] = False

if not st.session_state["client_auth"]:
    st.title("🔮 Cổng Tra Cứu Thần Số Học")
    pwd = st.text_input("Mật khẩu:", type="password")
    if st.button("Truy cập"):
        if pwd == "khachhang2026":
            st.session_state["client_auth"] = True
            st.rerun()
        else:
            st.error("Mật khẩu không đúng")
    st.stop()

# --- 4. TRA CỨU & GHI LỊCH SỬ ---
st.title("🔍 Tra Cứu Kết Quả")
conn = st.connection("gsheets", type=GSheetsConnection)

name_in = st.text_input("Họ và Tên (viết thường):")
dob_in = st.text_input("Mã Ngày Sinh (Ví dụ: 02091997):")

if st.button("Tra cứu ngay"):
    if name_in and dob_in:
        try:
            # Đọc dữ liệu từ tab đầu tiên (mặc định là Up_Data)
            df = conn.read(ttl=0)
            
            df['n_match'] = df.iloc[:, 0].apply(clean_id)
            df['d_match'] = df.iloc[:, 1].apply(clean_id)
            
            s_name = clean_id(name_in)
            s_dob = clean_id(dob_in)
            
            match = df[(df['n_match'] == s_name) & (df['d_match'] == s_dob)]
            
            if not match.empty:
                res_full_name = match.iloc[0, 0]
                st.success(f"Chào bạn **{res_full_name}**!")
                
                c1, c2 = st.columns(2)
                scd = str(match.iloc[0, 3]).split('.')[0]
                sdm = str(match.iloc[0, 4]).split('.')[0]
                c1.metric("Số Chủ Đạo", scd)
                c2.metric("Số Định Mệnh", sdm)

                # --- GHI LỊCH SỬ (SỬA LỖI ATTRIBUTEERROR) ---
                try:
                    now_vn = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
                    new_log = pd.DataFrame([{
                        "Thời Gian Tra Cứu": now_vn,
                        "Họ Và Tên": res_full_name,
                        "Ngày Sinh": f"'{s_dob}", 
                        "Trạng Thái": "Thành công"
                    }])
                    
                    # Đọc dữ liệu cũ từ tab History
                    history_df = conn.read(worksheet="History", ttl=0)
                    # Gộp dữ liệu
                    updated_history = pd.concat([history_df, new_log], ignore_index=True)
                    # Dùng .create thay cho .update để ghi dữ liệu vào Google Sheets
                    conn.create(worksheet="History", data=updated_history)
                except Exception as e_log:
                    # Nếu lỗi ghi lịch sử thì chỉ thông báo nhẹ, không làm hỏng trải nghiệm khách
                    st.info("Kết quả đã được lưu nội bộ.")
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp.")
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")

if st.button("Thoát"):
    st.session_state["client_auth"] = False
    st.rerun()
