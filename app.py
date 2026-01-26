import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Kết nối tự động qua Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔮 Hệ Thống Thần Số Học 2026")

with st.sidebar:
    st.header("📝 Nhập Thông Tin")
    name = st.text_input("Họ và tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày sinh:")
    btn_calc = st.button("Luận Giải & Lưu")

if btn_calc and name:
    # Tính số chủ đạo
    total = sum(int(i) for i in dob.strftime("%d%m%Y"))
    while total > 11 and total != 22:
        total = sum(int(digit) for digit in str(total))
    
    st.success(f"Khách hàng: {name} - Số chủ đạo: {total}")
    
    try:
        # Đọc và Lưu
        df = conn.read(ttl=0).astype(str)
        new_row = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": name,
            "Ngày Sinh": dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": str(total),
            "Số Điện Thoại": phone
        }])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
        st.balloons()
        st.rerun()
    except Exception as e:
        st.error(f"Lỗi: {e}")

st.divider()
st.subheader("⭐ Dữ liệu từ Google Sheets")
try:
    data = conn.read(ttl=0)
    st.dataframe(data, use_container_width=True)
except:
    st.info("Đang chờ dữ liệu...")
