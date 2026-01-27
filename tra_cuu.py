import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 

st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            .stAppDeployButton {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if "client_auth" not in st.session_state:
    st.session_state["client_auth"] = False

if not st.session_state["client_auth"]:
    st.title("🔮 Cổng Tra Cứu Thần Số Học")
    pwd_input = st.text_input("Nhập mật khẩu truy cập:", type="password")
    if st.button("Truy cập"):
        if pwd_input == CLIENT_PASSWORD:
            st.session_state["client_auth"] = True
            st.rerun()
        else:
            st.error("❌ Mật khẩu không chính xác.")
    st.stop()

# --- NỘI DUNG TRA CỨU ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔍 Tra Cứu Thần Số Học")
st.write("Vui lòng nhập thông tin để xem Số Chủ Đạo và Số Định Mệnh.")

with st.container():
    input_name = st.text_input("1. Nhập Họ và Tên:")
    input_dob = st.text_input("2. Nhập Ngày tháng năm sinh (ví dụ: 26031990):")
    btn_search = st.button("Tra cứu ngay")

if btn_search:
    if input_name and input_dob:
        try:
            # Đọc dữ liệu từ tab Up_Data
            df = conn.read(worksheet="Up_Data", ttl=0)
            
            # Chuẩn hóa tìm kiếm
            df['Họ Tên Tìm'] = df['Họ Tên'].astype(str).str.strip().str.lower()
            name_query = input_name.strip().lower()
            df['Ngày Sinh Tìm'] = df['Ngày Sinh'].astype(str).str.replace(" ", "").str.strip()
            dob_query = input_dob.replace(" ", "").strip()
            
            result = df[(df['Họ Tên Tìm'] == name_query) & (df['Ngày Sinh Tìm'] == dob_query)]
            
            if not result.empty:
                ho_ten_goc = result.iloc[0]['Họ Tên']
                so_chu_dao = result.iloc[0]['Số Chủ Đạo']
                so_dinh_menh = result.iloc[0]['Số Định Mệnh']
                
                st.success(f"Chào bạn **{ho_ten_goc}**! Kết quả của bạn là:")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Số Chủ Đạo", so_chu_dao)
                with col2:
                    st.metric("Số Định Mệnh", so_dinh_menh)
                
                # Ghi lịch sử (Dùng try-except để nếu lỗi sheet History thì vẫn hiện kết quả)
                try:
                    gio_vn = datetime.now() + timedelta(hours=7)
                    history_entry = pd.DataFrame([{
                        "Thời Gian Tra Cứu": gio_vn.strftime("%d/%m/%Y %H:%M:%S"),
                        "Họ Và Tên": ho_ten_goc,
                        "Ngày Sinh": dob_query,
                        "Trạng Thái": "Thành công"
                    }])
                    df_history = conn.read(worksheet="History", ttl=0)
                    updated_history = pd.concat([df_history, history_entry], ignore_index=True)
                    conn.update(worksheet="History", data=updated_history)
                except:
                    pass
            else:
                st.error("❌ Không tìm thấy dữ liệu phù hợp trong danh sách.")
        except Exception as e:
            st.error(f"Lỗi kết nối: Vui lòng kiểm tra lại tab 'Up_Data' trong Google Sheets.")
    else:
        st.warning("⚠️ Vui lòng nhập đầy đủ thông tin.")

if st.button("Thoát"):
    st.session_state["client_auth"] = False
    st.rerun()
