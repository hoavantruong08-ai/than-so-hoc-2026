import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
url = st.secrets["connections"]["gsheets"]["spreadsheet"]

st.title("🔮 Hệ Thống Upload Dữ Liệu")

# Giao diện chọn file từ máy tính
uploaded_file = st.file_uploader("Chọn file Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        df_new = pd.read_excel(uploaded_file)
        st.write("👀 Xem trước dữ liệu:")
        st.dataframe(df_new) # Hiện kết quả lên app
        
        if st.button("🚀 Xác nhận đẩy lên Google Sheet"):
            existing_data = conn.read(spreadsheet=url, usecols=list(range(5)))
            updated_df = pd.concat([existing_data, df_new], ignore_index=True)
            conn.update(spreadsheet=url, data=updated_df)
            st.success("✅ Đã lưu thành công!")
            st.balloons()
    except Exception as e:
        st.error(f"Lỗi: {e}")

st.divider()
st.subheader("📊 Dữ liệu hiện có")
st.dataframe(conn.read(spreadsheet=url, usecols=list(range(5))))
