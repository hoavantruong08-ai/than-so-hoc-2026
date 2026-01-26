import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Thần Số Học 2026")

# Kết nối tự động qua Secrets (Không dán link vào đây)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔮 Hệ Thống Thần Số Học")

# Nhập liệu
name = st.text_input("Họ tên:")
phone = st.text_input("Số điện thoại:")
dob = st.date_input("Ngày sinh:")

if st.button("Tính & Lưu"):
    if name and phone:
        # Tính số chủ đạo
        total = sum(int(i) for i in dob.strftime("%d%m%Y"))
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
            
        try:
            # Đọc dữ liệu cũ
            df = conn.read(ttl=0).astype(str)
            # Tạo dòng mới
            new_row = pd.DataFrame([{
                "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Họ Tên": name,
                "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                "Số Chủ Đạo": str(total),
                "Số Điện Thoại": phone
            }])
            # Ghi đè lên Sheet
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success(f"Đã lưu thành công cho {name}!")
            st.balloons()
        except Exception as e:
            st.error(f"Lỗi kết nối: {e}")
    else:
        st.warning("Vui lòng điền đủ thông tin!")

# Hiển thị bảng dữ liệu
st.divider()
try:
    data = conn.read(ttl=0)
    st.dataframe(data, use_container_width=True)
except:
    st.write("Đang chờ dữ liệu...")
