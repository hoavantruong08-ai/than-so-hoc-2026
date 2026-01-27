import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
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
            # Đọc Tab đầu tiên (Up_Data)
            df = conn.read(ttl=0)
            
            # 1. Xác định cột dựa trên vị trí (để tránh lỗi tên cột có dấu)
            # Cột 0: Họ Tên | Cột 1: Ngày Sinh | Cột 3: Số Chủ Đạo | Cột 4: Số Định Mệnh
            col_list = df.columns.tolist()
            name_col = col_list[0]
            dob_col = col_list[1]
            scd_col = col_list[3]
            sdm_col = col_list[4]

            # 2. CHUẨN HÓA DỮ LIỆU CỰC MẠNH
            # Tên: bỏ dấu cách, đưa về chữ thường
            df['n_clean'] = df[name_col].astype(str).str.strip().str.lower()
            # Ngày sinh: loại bỏ hoàn toàn dấu chấm, gạch ngang, khoảng trắng và .0 (nếu là số)
            df['d_clean'] = df[dob_col].astype(str).str.replace(r'[\s\.\-\/]', '', regex=True).str.replace('.0', '', regex=False).str.strip()
            
            q_name = input_name.strip().lower()
            q_dob = input_dob.replace(" ", "").strip()
            
            # 3. Tìm kiếm
            match = df[(df['n_clean'] == q_name) & (df['d_clean'] == q_dob)]
            
            if not match.empty:
                res_name = match.iloc[0][name_col]
                res_scd = match.iloc[0][scd_col]
                res_sdm = match.iloc[0][sdm_col]
                
                st.success(f"Chào bạn **{res_name}**!")
                c1, c2 = st.columns(2)
                c1.metric("Số Chủ Đạo", res_scd)
                c2.metric("Số Định Mệnh", res_sdm)
                
                # Ghi nhật ký vào tab History
                try:
                    gio_vn = datetime.now() + timedelta(hours=7)
                    hist_df = conn.read(worksheet="History", ttl=0)
                    new_log = pd.DataFrame([{
                        "Thời Gian Tra Cứu": gio_vn.strftime("%d/%m/%Y %H:%M:%S"),
                        "Họ Và Tên": res_name,
                        "Ngày Sinh": q_dob,
                        "Trạng Thái": "Thành công"
                    }])
                    updated_hist = pd.concat([hist_df, new_log], ignore_index=True)
                    conn.update(worksheet="History", data=updated_hist)
                except:
                    pass
            else:
                st.error("❌ Không tìm thấy thông tin. Bạn hãy kiểm tra lại Họ tên hoặc Ngày sinh (phải khớp chính xác với bảng dữ liệu).")
        except Exception as e:
            st.error("⚠️ Lỗi hệ thống. Vui lòng báo Admin kiểm tra file Google Sheets.")
    else:
        st.warning("⚠️ Hãy nhập đủ thông tin.")

if st.button("Thoát"):
    st.session_state["client_auth"] = False
    st.rerun()
