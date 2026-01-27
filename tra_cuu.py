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
    s = str(text).split('.')[0] 
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
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
            # 1. Đọc dữ liệu từ tab nguồn (giả định tab 1 là Up_Data)
            df = conn.read(ttl=0)
            
            df['name_match'] = df.iloc[:, 0].apply(clean_id)
            df['dob_match'] = df.iloc[:, 1].apply(clean_id)
            
            s_name = clean_id(name_in)
            s_dob = clean_id(dob_in)
            
            match = df[(df['name_match'] == s_name) & (df['dob_match'] == s_dob)]
            
            if not match.empty:
                res_full_name = match.iloc[0, 0]
                st.success(f"Kết quả cho: **{res_full_name}**")
                
                c1, c2 = st.columns(2)
                scd = clean_id(match.iloc[0, 3]).upper()
                sdm = clean_id(match.iloc[0, 4]).upper()
                c1.metric("Số Chủ Đạo", scd)
                c2.metric("Số Định Mệnh", sdm)

                # --- PHẦN GHI LỊCH SỬ (CẬP NHẬT) ---
                try:
                    # Lấy giờ VN
                    now_vn = (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S")
                    
                    # Tạo dòng log mới
                    new_log = pd.DataFrame([{
                        "Thời Gian Tra Cứu": now_vn,
                        "Họ Và Tên": res_full_name,
                        "Ngày Sinh": f"'{s_dob}", # Thêm dấu nháy đơn để tránh Google đổi định dạng số
                        "Trạng Thái": "Thành công"
                    }])
                    
                    # Đọc sheet History riêng biệt
                    history_df = conn.read(worksheet="History", ttl=0)
                    
                    # Kết hợp dữ liệu cũ và mới
                    updated_history = pd.concat([history_df, new_log], ignore_index=True)
                    
                    # Ghi đè lại vào worksheet History
                    conn.update(worksheet="History", data=updated_history)
                except Exception as log_err:
                    st.warning("⚠️ Đã hiện kết quả nhưng không thể ghi lịch sử. Admin vui lòng kiểm tra tab 'History'.")
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp.")
        except Exception as e:
            st.error(f"Lỗi hệ thống: {e}")
