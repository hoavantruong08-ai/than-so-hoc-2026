import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime, timedelta

# --- CẤU HÌNH ---
CLIENT_PASSWORD = "khachhang2026" 

st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# 1. ẨN MENU QUẢN LÝ
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            #stDecoration {display:none;}
            [data-testid="stSidebarNav"] {display: none;}
            .stAppDeployButton {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- KIỂM TRA ĐĂNG NHẬP ---
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
    input_name = st.text_input("1. Nhập Họ và Tên (viết thường hoặc hoa đều được):")
    input_dob = st.text_input("2. Nhập Ngày tháng năm sinh (viết liền, ví dụ: 26031990):")
    btn_search = st.button("Tra cứu ngay")

if btn_search:
    if input_name and input_dob:
        try:
            # 1. Đọc dữ liệu từ tab Up_Data (Chứa dữ liệu gốc)
            df = conn.read(worksheet="Up_Data", ttl=0)
            
            # Chuẩn hóa dữ liệu để tìm kiếm
            # Xử lý Họ tên: Bỏ khoảng trắng, đưa về chữ thường
            df['Họ Tên Tìm'] = df['Họ Tên'].astype(str).str.strip().str.lower()
            name_query = input_name.strip().lower()
            
            # Xử lý Ngày sinh: Bỏ khoảng trắng, đưa về dạng chuỗi viết liền
            df['Ngày Sinh Tìm'] = df['Ngày Sinh'].astype(str).str.strip()
            dob_query = input_dob.strip()
            
            # Tìm kiếm khớp cả Họ tên và Ngày sinh
            result = df[(df['Họ Tên Tìm'] == name_query) & (df['Ngày Sinh Tìm'] == dob_query)]
            
            if not result.empty:
                ho_ten_goc = result.iloc[0]['Họ Tên']
                so_chu_dao = result.iloc[0]['Số Chủ Đạo']
                so_dinh_menh = result.iloc[0]['Số Định Mệnh']
                
                st.success(f"Chào bạn **{ho_ten_goc}**! Kết quả của bạn là:")
                
                # Hiển thị kết quả đẹp mắt
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
                        <p style="margin:0;">Số Chủ Đạo</p>
                        <h1 style="color: #ff4b4b; margin:0;">{so_chu_dao}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
                        <p style="margin:0;">Số Định Mệnh</p>
                        <h1 style="color: #1c83e1; margin:0;">{so_dinh_menh}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.info("💡 Chuyên gia sẽ sớm gửi bản phân tích chi tiết cho bạn dựa trên hai con số này.")

                # --- 2. GHI LỊCH SỬ VÀO TAB HISTORY ---
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
                st.error("❌ Không tìm thấy dữ liệu. Vui lòng kiểm tra lại Họ tên hoặc Ngày sinh.")
        except Exception as e:
            st.error("Lỗi kết nối dữ liệu.")
    else:
        st.warning("⚠️ Vui lòng nhập đầy đủ Họ tên và Ngày sinh.")

if st.button("Thoát"):
    st.session_state["client_auth"] = False
    st.rerun()
