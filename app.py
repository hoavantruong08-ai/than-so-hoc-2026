import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Thần Số Học Pro", layout="wide")

# Kết nối tự động qua Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔮 Hệ Thống Thần Số Học")

with st.sidebar:
    st.header("📝 Nhập Thông Tin")
    name = st.text_input("Họ và tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày sinh:")
    btn_calc = st.button("Luận Giải & Lưu")

col1, col2 = st.columns(2)

with col1:
    if btn_calc and name:
        # Tính số chủ đạo đơn giản
        total = sum(int(i) for i in dob.strftime("%d%m%Y"))
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        
        st.success(f"Khách hàng: {name} - Số chủ đạo: {total}")
        
        try:
            # Lấy dữ liệu hiện tại
            existing_data = conn.read(ttl=0)
            # Tạo dòng mới
            new_row = pd.DataFrame([{
                "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Họ Tên": name,
                "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                "Số Chủ Đạo": str(total),
                "Số Điện Thoại": phone
            }])
            # Ghi vào Sheet
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.balloons() # Hiệu ứng chúc mừng khi lưu thành công
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi kết nối Sheet: {e}")

with col2:
    st.subheader("⭐ Dữ liệu từ Google Sheets")
    try:
        df = conn.read(ttl=0)
        st.dataframe(df, use_container_width=True)
    except:
        st.info("Chưa có dữ liệu hoặc lỗi kết nối.")
