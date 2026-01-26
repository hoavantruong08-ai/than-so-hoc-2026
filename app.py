import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Thần Số Học - Quản Lý", layout="wide")

# 1. Kết nối Google Sheets (Dùng cấu hình Secrets bạn đã lưu thành công)
conn = st.connection("gsheets", type=GSheetsConnection)
url = st.secrets["connections"]["gsheets"]["spreadsheet"]

st.title("🔮 Hệ Thống Thần Số Học & Upload Dữ Liệu")

# --- PHẦN 1: TẢI FILE EXCEL LÊN ---
st.header("📤 Bước 1: Tải file Excel từ máy tính")
uploaded_file = st.file_uploader("Chọn file Up_Load - Excel.xlsx", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Đọc file Excel (mặc định sheet đầu tiên)
        df_new = pd.read_excel(uploaded_file)
        
        # Hiển thị kết quả lên cửa sổ app để kiểm tra
        st.subheader("👀 Xem trước dữ liệu từ máy tính của bạn:")
        st.dataframe(df_new)
        
        if st.button("🚀 Xác nhận đẩy lên Google Sheet"):
            # Đọc dữ liệu cũ đang có trên Google Sheet
            existing_data = conn.read(spreadsheet=url, usecols=list(range(5)))
            
            # Gộp dữ liệu cũ và mới (nối đuôi)
            updated_df = pd.concat([existing_data, df_new], ignore_index=True)
            
            # Lưu ngược lại lên Google Sheet
            conn.update(spreadsheet=url, data=updated_df)
            st.success("✅ Đã đẩy dữ liệu thành công! Hãy xem bảng tổng hợp bên dưới.")
            st.balloons()
            
    except Exception as e:
        st.error(f"Lỗi đọc file: {e}. Hãy đảm bảo file Excel có 5 cột đúng tên.")

st.divider()

# --- PHẦN 2: HIỂN THỊ BẢNG TỔNG HỢP ---
st.header("📊 Bước 2: Bảng dữ liệu tổng hợp (Google Sheet)")
try:
    # Đọc lại toàn bộ dữ liệu để hiển thị
    total_data = conn.read(spreadsheet=url, usecols=list(range(5)))
    st.dataframe(total_data.sort_index(ascending=False))
except:
    st.info("Chưa có dữ liệu nào được lưu.")
