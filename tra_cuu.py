import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CẤU HÌNH MẬT KHẨU KHÁCH HÀNG ---
CLIENT_PASSWORD = "khachhang2026"  # <--- THAY ĐỔI MẬT KHẨU TRA CỨU TẠI ĐÂY

st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# --- KIỂM TRA ĐĂNG NHẬP KHÁCH HÀNG ---
if "client_auth" not in st.session_state:
    st.session_state["client_auth"] = False

if not st.session_state["client_auth"]:
    st.title("🔮 Cổng Tra Cứu Thần Số Học")
    st.info("Vui lòng nhập mật khẩu truy cập được cung cấp để bắt đầu tra cứu.")
    
    pwd_input = st.text_input("Mật khẩu truy cập:", type="password")
    if st.button("Truy cập"):
        if pwd_input == CLIENT_PASSWORD:
            st.session_state["client_auth"] = True
            st.rerun()
        else:
            st.error("❌ Mật khẩu không chính xác. Vui lòng liên hệ hỗ trợ.")
    st.stop()

# --- NỘI DUNG SAU KHI ĐĂNG NHẬP ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔍 Tra Cứu Kết Quả Thần Số Học")
st.write("Chào mừng bạn! Hãy nhập thông tin bên dưới để xem kết quả.")

with st.sidebar:
    if st.button("Thoát hệ thống"):
        st.session_state["client_auth"] = False
        st.rerun()

with st.container():
    search_query = st.text_input("Nhập Số điện thoại của bạn:")
    btn_search = st.button("Tra cứu ngay")

if btn_search:
    if search_query:
        df = conn.read(ttl=0)
        # Chuyển đổi SĐT về dạng chuỗi để tìm kiếm khớp hoàn toàn
        df['Số Điện Thoại'] = df['Số Điện Thoại'].astype(str).str.replace(".0", "", regex=False).str.strip()
        search_query = search_query.strip()
        
        result = df[df['Số Điện Thoại'] == search_query]
        
        if not result.empty:
            st.success(f"Chào bạn **{result.iloc[0]['Họ Tên']}**! Đây là kết quả của bạn:")
            
            # Hiển thị kết quả dạng Card
            st.markdown(f"""
            <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                <h2 style="margin:0;">Số Chủ Đạo: <span style="color: #ff4b4b;">{result.iloc[0]['Số Chủ Đạo']}</span></h2>
                <p style="font-size: 18px;">Ngày sinh: {result.iloc[0]['Ngày Sinh']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.info("💡 **Lời khuyên:** Hãy phát huy thế mạnh của con số này trong hành trình sắp tới của bạn!")
        else:
            st.error("Chưa tìm thấy dữ liệu cho số điện thoại này. Vui lòng kiểm tra lại hoặc liên hệ Admin.")
    else:
        st.warning("Vui lòng nhập số điện thoại để tra cứu.")
