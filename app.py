import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Thần Số Học 2026", layout="wide")

# Kết nối qua Secrets (Đảm bảo Secrets của bạn đã Save thành công)
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
            # Lấy dữ liệu hiện tại - ép kiểu string để tránh lỗi
            existing_data = conn.read(ttl=0).astype(str)
            
            # Tạo dòng mới
            new_row = pd.DataFrame([{
                "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Họ Tên": str(name),
                "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                "Số Chủ Đạo": str(total),
                "Số Điện Thoại": str(phone)
            }])
            
            # Ghi vào Sheet
            updated_df = pd.concat([existing_data, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi khi lưu: {e}")

with col2:
    st.subheader("⭐ Dữ liệu từ Google Sheets")
    try:
        # Đọc dữ liệu với ttl=0 để không bị lưu cache cũ
        df = conn.read(ttl=0)
        if not df.empty:
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("Sheet đang trống, hãy nhập dòng mẫu đầu tiên vào Sheet!")
    except Exception as e:
        st.error(f"Không thể kết nối Sheet: {e}")
