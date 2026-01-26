import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Cấu hình trang
st.set_page_config(page_title="Thần Số Học Pro 2026", layout="wide")

# 2. Kết nối bằng cấu hình từ Secrets
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔮 Hệ Thống Luận Giải Thần Số Học")

# --- NHẬP LIỆU ---
with st.sidebar:
    st.header("📝 Nhập Thông Tin")
    name = st.text_input("Họ và tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày tháng năm sinh:")
    btn_calc = st.button("Luận Giải Ngay")

# --- HIỂN THỊ & LƯU ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Kết Quả Phân Tích")
    if btn_calc and name:
        # Tính số chủ đạo đơn giản
        total = sum(int(i) for i in dob.strftime("%d%m%Y"))
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        
        st.success(f"Khách hàng: **{name}**")
        st.info(f"Số chủ đạo: **{total}**")
        
        if st.button("❤️ Lưu lên Cloud"):
            try:
                # Đọc dữ liệu cũ
                existing_data = conn.read()
                # Tạo dòng mới
                new_data = pd.DataFrame([{
                    "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Họ Tên": name,
                    "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                    "Số Chủ Đạo": str(total),
                    "Số Điện Thoại": phone
                }])
                # Cập nhật lên Sheet
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.toast("Đã lưu thành công!", icon="✅")
                st.rerun()
            except Exception as e:
                st.error(f"Lỗi: {e}")

with col2:
    st.subheader("⭐ Danh Sách Đã Lưu")
    try:
        data = conn.read(ttl=0)
        st.dataframe(data, use_container_width=True, hide_index=True)
    except:
        st.write("Đang chờ dữ liệu...")
