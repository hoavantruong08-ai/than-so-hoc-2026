import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Thần Số Học Tổng Hợp", layout="wide")

# Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
url = st.secrets["connections"]["gsheets"]["spreadsheet"]

st.title("🔮 Hệ Thống Thần Số Học & Quản Lý File")

# Chia làm 2 cột
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1. Nhập liệu trực tiếp")
    name = st.text_input("Họ tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày sinh:", min_value=datetime(1900, 1, 1))

    if st.button("Tính & Lưu"):
        if name and phone:
            # Tính số chủ đạo
            total = sum(int(digit) for digit in dob.strftime("%d%m%Y"))
            while total > 11 and total not in [22]:
                total = sum(int(digit) for digit in str(total))
            
            new_data = pd.DataFrame([{
                "Thời Gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Họ Tên": name,
                "Ngày Sinh": dob.strftime("%Y-%m-%d"),
                "Số Chủ Đạo": total,
                "Số Điện Thoại": phone
            }])
            
            existing_data = conn.read(spreadsheet=url, usecols=list(range(5)))
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(spreadsheet=url, data=updated_df)
            st.success(f"Đã lưu! Số chủ đạo: {total}")
            st.balloons()

with col2:
    st.header("2. Upload từ Excel")
    uploaded_file = st.file_uploader("Chọn file .xlsx từ máy tính", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            df_upload = pd.read_excel(uploaded_file)
            st.write("Xem trước dữ liệu:")
            st.dataframe(df_upload)
            
            if st.button("Xác nhận Upload"):
                existing_data = conn.read(spreadsheet=url, usecols=list(range(5)))
                final_df = pd.concat([existing_data, df_upload], ignore_index=True)
                conn.update(spreadsheet=url, data=final_df)
                st.success("✅ Đã đẩy dữ liệu lên thành công!")
                st.balloons()
        except Exception as e:
            st.error(f"Lỗi: {e}")

st.divider()
st.subheader("📊 Toàn bộ dữ liệu trên Google Sheet")
st.dataframe(conn.read(spreadsheet=url, usecols=list(range(5))))
