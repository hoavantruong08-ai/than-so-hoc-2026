import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hệ Thống Thần Số Học", layout="wide")
st.title("🔮 Hệ Thống Thần Số Học & Quản Lý Dữ Liệu")

# Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- PHẦN 1: TÍNH TOÁN VÀ LƯU TỪNG NGƯỜI ---
st.header("1. Nhập liệu cá nhân")
col1, col2 = st.columns([1, 2])

with col1:
    name = st.text_input("Họ tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày sinh:", min_value=datetime(1900, 1, 1))

    if st.button("Tính & Lưu"):
        if name and phone:
            # Tính số chủ đạo (tổng ngày + tháng + năm)
            total = sum(int(digit) for digit in dob.strftime("%d%m%Y"))
            while total > 11 and total not in [22]:
                total = sum(int(digit) for digit in str(total))
            
            # Chuẩn bị dữ liệu mới
            new_data = pd.DataFrame([{
                "Thời Gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Họ Tên": name,
                "Ngày Sinh": dob.strftime("%Y-%m-%d"),
                "Số Chủ Đạo": total,
                "Số Điện Thoại": phone
            }])
            
            # Đọc dữ liệu cũ và gộp
            existing_data = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], usecols=list(range(5)))
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], data=updated_df)
            
            st.success(f"Đã lưu thành công! Số chủ đạo của bạn là: {total}")
            st.balloons()
        else:
            st.error("Vui lòng nhập đủ tên và số điện thoại!")

# --- PHẦN 2: UPLOAD FILE EXCEL TỪ MÁY TÍNH ---
st.divider()
st.header("2. 📤 Tải dữ liệu hàng loạt từ Excel")
st.info("Lưu ý: File Excel cần có các cột: Thời Gian, Họ Tên, Ngày Sinh, Số Chủ Đạo, Số Điện Thoại")

uploaded_file = st.file_uploader("Chọn file Excel từ máy tính của bạn", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_upload = pd.read_excel(uploaded_file)
        st.write("Xem trước dữ liệu từ file của bạn:")
        st.dataframe(df_upload)
        
        if st.button("Xác nhận đẩy lên Google Sheet"):
            existing_data = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], usecols=list(range(5)))
            # Nối file excel vừa chọn vào sau dữ liệu cũ
            final_df = pd.concat([existing_data, df_upload], ignore_index=True)
            conn.update(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], data=final_df)
            st.success("✅ Toàn bộ dữ liệu từ Excel đã được đẩy lên Google Sheet!")
            st.balloons()
    except Exception as e:
        st.error(f"Lỗi: {e}")

# --- PHẦN 3: HIỂN THỊ DỮ LIỆU ---
with col2:
    st.subheader("Dữ liệu hiện tại trên hệ thống")
    data = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], usecols=list(range(5)))
    st.dataframe(data.sort_index(ascending=False))
