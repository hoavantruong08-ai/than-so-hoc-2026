import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình tối giản
st.set_page_config(page_title="Thần Số Học 2026", layout="centered")

# Kết nối
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("Lỗi kết nối Google Sheets. Kiểm tra lại Secrets!")

def tinh_so(dob_raw):
    s = "".join(filter(str.isdigit, str(dob_raw)))
    if not s: return "0"
    total = sum(int(i) for i in s)
    while total > 11 and total != 22:
        total = sum(int(digit) for digit in str(total))
    return str(total)

st.title("🔮 Hệ Thống Thần Số Học")

# Chia khu vực rõ ràng
menu = st.sidebar.selectbox("Chức năng", ["Nhập liệu", "Upload danh sách CSV"])

if menu == "Nhập liệu":
    with st.form("nhap_tay"):
        name = st.text_input("Họ tên")
        phone = st.text_input("Số điện thoại")
        dob = st.date_input("Ngày sinh")
        if st.form_submit_button("Lưu"):
            if name and phone:
                so_cd = tinh_so(dob)
                df_old = conn.read(ttl=0).astype(str)
                new_row = pd.DataFrame([{
                    "Thời Gian": datetime.now().strftime("%d/%m/%Y"),
                    "Họ Tên": name,
                    "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                    "Số Chủ Đạo": so_cd,
                    "Số Điện Thoại": phone
                }])
                conn.update(data=pd.concat([df_old, new_row], ignore_index=True))
                st.success(f"Đã lưu thành công! Số chủ đạo: {so_cd}")

else:
    st.subheader("Upload file CSV")
    st.info("Để không bị lỗi, hãy dùng file định dạng .csv (Save as CSV trong Excel)")
    up_file = st.file_uploader("Chọn file CSV", type="csv")
    
    if up_file:
        df = pd.read_csv(up_file)
        st.write("Dữ liệu xem trước:", df.head(3))
        
        if st.button("Đẩy lên hệ thống"):
            # Tự thêm cột nếu thiếu
            if "Ngày Sinh" in df.columns:
                df["Số Chủ Đạo"] = df["Ngày Sinh"].apply(tinh_so)
                df["Thời Gian"] = datetime.now().strftime("%d/%m/%Y")
                
                old = conn.read(ttl=0).astype(str)
                conn.update(data=pd.concat([old, df.astype(str)], ignore_index=True))
                st.success("Đã đồng bộ thành công!")
            else:
                st.error("File cần có cột 'Ngày Sinh' để tính toán!")

st.divider()
st.subheader("Bảng dữ liệu tổng")
if st.button("Lấy dữ liệu mới nhất"):
    st.cache_data.clear()

try:
    data = conn.read(ttl=0)
    st.dataframe(data, use_container_width=True)
except:
    st.write("Đang tải dữ liệu...")
