import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH MẬT KHẨU KHÁCH HÀNG ---
CLIENT_PASSWORD = "khachhang2026" 

# 1. CẤU HÌNH TRANG VÀ ẨN MENU QUẢN LÝ
st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            #stDecoration {display:none;}
            [data-testid="stSidebarNav"] {display: none;}
            .stAppDeployButton {display: none !important;}
            iframe[title="manage-app"] {display: none !important;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- KIỂM TRA ĐĂNG NHẬP KHÁCH HÀNG ---
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

# --- NỘI DUNG SAU KHI ĐĂNG NHẬP ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔍 Tra Cứu Kết Quả Thần Số Học")
st.write("Vui lòng nhập chính xác thông tin để xem kết quả.")

with st.container():
    input_name = st.text_input("1. Nhập Họ và Tên của bạn:")
    input_phone = st.text_input("2. Nhập Số điện thoại của bạn:")
    btn_search = st.button("Tra cứu ngay")

if btn_search:
    if input_name and input_phone:
        try:
            # Đọc dữ liệu từ Sheet chính (giả sử sheet đầu tiên)
            df = conn.read(ttl=0)
            
            # Chuẩn hóa dữ liệu tìm kiếm
            df['Họ Tên Tìm Kiếm'] = df['Họ Tên'].astype(str).str.strip().str.lower()
            name_query = input_name.strip().lower()
            df['SĐT Tìm Kiếm'] = df['Số Điện Thoại'].astype(str).str.replace(".0", "", regex=False).str.strip()
            phone_query = input_phone.strip()
            
            # Tìm kiếm
            result = df[(df['Họ Tên Tìm Kiếm'] == name_query) & (df['SĐT Tìm Kiếm'] == phone_query)]
            
            if not result.empty:
                ho_ten_goc = result.iloc[0]['Họ Tên']
                so_chu_dao = result.iloc[0]['Số Chủ Đạo']
                ngay_sinh = result.iloc[0]['Ngày Sinh']
                
                st.success(f"Chào bạn **{ho_ten_goc}**! Đây là kết quả của bạn:")
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                    <h2 style="margin:0;">Số Chủ Đạo: <span style="color: #ff4b4b;">{so_chu_dao}</span></h2>
                    <p style="font-size: 18px;">Ngày sinh: {ngay_sinh}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # --- PHẦN GHI LỊCH SỬ TRA CỨU ---
                try:
                    # Tạo dòng dữ liệu lịch sử mới
                    history_entry = pd.DataFrame([{
                        "Thời Gian Tra Cứu": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "Họ Tên": ho_ten_goc,
                        "Số Điện Thoại": f"'{phone_query}",
                        "Số Chủ Đạo": so_chu_dao,
                        "Trạng Thái": "Thành công"
                    }])
                    
                    # Đọc Sheet Lịch sử (nếu chưa có sẽ tự tạo bảng mới)
                    # Lưu ý: Bạn nên tạo sẵn một Tab tên là 'History' trong file Google Sheets
                    df_history = conn.read(worksheet="History", ttl=0)
                    updated_history = pd.concat([df_history, history_entry], ignore_index=True)
                    conn.update(worksheet="History", data=updated_history)
                except:
                    # Nếu chưa có sheet 'History', hệ thống sẽ vẫn chạy nhưng không lưu được lịch sử
                    pass
                
                st.info("💡 **Lời khuyên:** Hãy phát huy thế mạnh của con số này trong hành trình sắp tới!")
            else:
                st.error("❌ Không tìm thấy thông tin phù hợp. Vui lòng kiểm tra lại Họ tên hoặc SĐT.")
        except Exception as e:
            st.error("Lỗi kết nối dữ liệu. Vui lòng báo Admin.")
    else:
        st.warning("⚠️ Vui lòng điền đầy đủ cả Họ tên và Số điện thoại.")

if st.button("Thoát hệ thống"):
    st.session_state["client_auth"] = False
    st.rerun()
