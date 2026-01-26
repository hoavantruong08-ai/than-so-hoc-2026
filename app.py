import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="Thần Số Học 2026")

# Kết nối
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔮 Hệ Thống Thần Số Học")

# Nhập liệu đơn giản
with st.form("form_nhap"):
    name = st.text_input("Họ tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày sinh")
    submit = st.form_submit_button("Tính & Lưu")

if submit:
    if name and phone:
        # Tính số chủ đạo logic thuần
        d = dob.strftime("%d%m%Y")
        total = sum(int(i) for i in d)
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        
        try:
            # Lấy data và thêm dòng mới bằng list (không dùng pandas)
            data = conn.read(ttl=0)
            new_row = [
                datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                name,
                dob.strftime("%d/%m/%Y"),
                str(total),
                phone
            ]
            data.loc[len(data)] = new_row
            conn.update(data=data)
            st.success(f"Đã lưu thành công! Số chủ đạo: {total}")
            st.balloons()
        except Exception as e:
            st.error(f"Lỗi: {e}")
    else:
        st.warning("Vui lòng nhập đủ tên và số điện thoại!")

# Hiển thị bảng
st.divider()
try:
    df = conn.read(ttl=0)
    st.dataframe(df, use_container_width=True)
except:
    st.info("Đang chờ dữ liệu...")
