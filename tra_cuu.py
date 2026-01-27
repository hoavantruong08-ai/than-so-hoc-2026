import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 

st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# Ẩn menu để chuyên nghiệp
st.markdown("""<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    </style>""", unsafe_allow_html=True)

# Hàm loại bỏ dấu tiếng Việt và ký tự đặc biệt
def remove_accents(input_str):
    if not input_str or input_str == "nan": return ""
    s = unicodedata.normalize('NFD', input_str)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    return re.sub(r'[^a-zA-Z0-9]', '', s).lower()

if "client_auth" not in st.session_state:
    st.session_state["client_auth"] = False

if not st.session_state["client_auth"]:
    st.title("🔮 Cổng Tra Cứu Thần Số Học")
    pwd_input = st.text_input("Mật khẩu truy cập:", type="password")
    if st.button("Truy cập"):
        if pwd_input == CLIENT_PASSWORD:
            st.session_state["client_auth"] = True
            st.rerun()
        else:
            st.error("❌ Sai mật khẩu.")
    st.stop()

# --- KẾT NỐI DỮ LIỆU ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔍 Tra Cứu Thần Số Học")
with st.container():
    input_name = st.text_input("1. Nhập Họ và Tên (Ví dụ: Nguyễn Văn A):")
    input_dob = st.text_input("2. Nhập Ngày tháng năm sinh (Ví dụ: 26031990):")
    btn_search = st.button("Tra cứu ngay")

if btn_search:
    if input_name and input_dob:
        try:
            # Đọc Tab đầu tiên (Dữ liệu gốc)
            df = conn.read(ttl=0)
            
            # Lấy tiêu đề cột theo vị trí để tránh lỗi dấu tiếng Việt trong tiêu đề
            col_list = df.columns.tolist()
            name_col = col_list[0] # Cột A
            dob_col = col_list[1]  # Cột B
            scd_col = col_list[3]  # Cột D
            sdm_col = col_list[4]  # Cột E

            # CHUẨN HÓA DỮ LIỆU ĐỂ SO SÁNH (Bỏ dấu, bỏ cách, về chữ thường)
            df['name_match'] = df[name_col].astype(str).apply(remove_accents)
            df['dob_match'] = df[dob_col].astype(str).apply(remove_accents)
            
            search_name = remove_accents(input_name)
            search_dob = remove_accents(input_dob)
            
            # Tìm kiếm
            match = df[(df['name_match'] == search_name) & (df['dob_match'] == search_dob)]
            
            if not match.empty:
                res_name = match.iloc[0][name_col]
                res_scd = match.iloc[0][scd_col]
                res_sdm = match.iloc[0][sdm_col]
                
                st.success(f"Chào bạn **{res_name}**!")
                c1, c2 = st.columns(2)
                c1.metric("Số Chủ Đạo", res_scd)
                c2.metric("Số Định Mệnh", res_sdm)
                
                # Ghi lịch sử vào tab History
                try:
                    gio_vn = datetime.now() + timedelta(hours=7)
                    hist_df = conn.read(worksheet="History", ttl=0)
                    new_log = pd.DataFrame([{
                        "Thời Gian Tra Cứu": gio_vn.strftime("%d/%m/%Y %H:%M:%S"),
                        "Họ Và Tên": res_name,
                        "Ngày Sinh": input_dob,
                        "Trạng Thái": "Thành công"
                    }])
                    updated_hist = pd.concat([hist_df, new_log], ignore_index=True)
                    conn.update(worksheet="History", data=updated_hist)
                except: pass
            else:
                st.error("❌ Không tìm thấy thông tin. Vui lòng kiểm tra lại Họ tên hoặc Ngày sinh.")
        except Exception as e:
            st.error("⚠️ Lỗi kết nối dữ liệu. Vui lòng kiểm tra lại file Sheets.")
    else:
        st.warning("⚠️ Hãy nhập đủ thông tin.")
