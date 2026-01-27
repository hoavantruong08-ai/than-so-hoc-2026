import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 

st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# Ẩn menu để khách không xóa app
st.markdown("""<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display: none !important;}
    </style>""", unsafe_allow_html=True)

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
    input_name = st.text_input("1. Nhập Họ và Tên (viết thường hoặc hoa):")
    input_dob = st.text_input("2. Nhập Ngày tháng năm sinh (ví dụ: 26031990):")
    btn_search = st.button("Tra cứu ngay")

if btn_search:
    if input_name and input_dob:
        try:
            # Đọc dữ liệu từ tab Up_Data
            # Sử dụng header=0 để lấy dòng đầu tiên làm tiêu đề
            df = conn.read(worksheet="Up_Data", ttl=0)
            
            # CHUẨN HÓA DỮ LIỆU ĐỂ SO SÁNH
            # Lấy cột đầu tiên (Họ Tên) và cột thứ hai (Ngày Sinh) theo vị trí để tránh lỗi dấu tiếng Việt
            name_col = df.columns[0]
            dob_col = df.columns[1]
            scd_col = df.columns[3] # Cột D (Số Chủ Đạo)
            sdm_col = df.columns[4] # Cột E (Số Định Mệnh)

            df['name_clean'] = df[name_col].astype(str).str.strip().str.lower()
            df['dob_clean'] = df[dob_col].astype(str).str.replace(" ", "").str.strip()
            
            query_name = input_name.strip().lower()
            query_dob = input_dob.replace(" ", "").strip()
            
            # Tìm kiếm
            match = df[(df['name_clean'] == query_name) & (df['dob_clean'] == query_dob)]
            
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
                        "Ngày Sinh": query_dob,
                        "Trạng Thái": "Thành công"
                    }])
                    updated_hist = pd.concat([hist_df, new_log], ignore_index=True)
                    conn.update(worksheet="History", data=updated_hist)
                except:
                    pass
            else:
                st.error("❌ Không tìm thấy thông tin. Bạn vui lòng kiểm tra lại Họ tên và Ngày sinh.")
        except Exception as e:
            st.error("⚠️ Lỗi kết nối: Bạn hãy kiểm tra lại cấu hình Secrets hoặc tên Tab 'Up_Data'.")
    else:
        st.warning("⚠️ Hãy nhập đủ thông tin.")

if st.button("Thoát"):
    st.session_state["client_auth"] = False
    st.rerun()
