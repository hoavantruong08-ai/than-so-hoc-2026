import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 
st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

def clean_id(text):
    if not text or str(text) == "nan": return ""
    # Chuyển sang chuỗi, lấy phần nguyên trước dấu chấm
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    # Chỉ giữ lại chữ cái và số
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    
    # --- XỬ LÝ BÙ SỐ 0 ĐẦU (Nếu là mã ngày sinh 7 chữ số) ---
    if s.isdigit() and len(s) == 7:
        s = "0" + s
    return s

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
dob_in = st.text_input("Mã Ngày Sinh (Ví dụ: 02091997):")

if st.button("Tra cứu ngay"):
    if name_in and dob_in:
        try:
            df = conn.read(ttl=0)
            
            # Chuẩn hóa ID từ Sheet và ID từ khách nhập
            df['n_match'] = df.iloc[:, 0].apply(clean_id)
            df['d_match'] = df.iloc[:, 1].apply(clean_id)
            
            s_name = clean_id(name_in)
            s_dob = clean_id(dob_in)
            
            match = df[(df['n_match'] == s_name) & (df['d_match'] == s_dob)]
            
            if not match.empty:
                res_full_name = match.iloc[0, 0]
                st.success(f"Kết quả cho: **{res_full_name}**")
                
                c1, c2 = st.columns(2)
                # Lấy kết quả Số Chủ Đạo và Định Mệnh, ép về số nguyên sạch
                scd = str(match.iloc[0, 3]).split('.')[0]
                sdm = str(match.iloc[0, 4]).split('.')[0]
                
                c1.metric("Số Chủ Đạo", scd)
                c2.metric("Số Định Mệnh", sdm)

                # --- GHI LỊCH SỬ VÀO TAB HISTORY ---
                try:
                    now_vn = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
                    new_log = pd.DataFrame([{
                        "Thời Gian Tra Cứu": now_vn,
                        "Họ Và Tên": res_full_name,
                        "Ngày Sinh": f"'{s_dob}", 
                        "Trạng Thái": "Thành công"
                    }])
                    # Đọc và ghi đè tab History (Yêu cầu quyền Editor trong Share)
                    history_df = conn.read(worksheet="History", ttl=0)
                    updated_history = pd.concat([history_df, new_log], ignore_index=True)
                    conn.update(worksheet="History", data=updated_history)
                except:
                    pass
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp.")
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")
