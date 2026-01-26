import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Cấu hình trang
st.set_page_config(page_title="Thần Số Học Pro 2026", page_icon="🔮", layout="wide")

# 2. ĐƯỜNG LINK ĐÃ ĐƯỢC TỐI ƯU (Dòng 10)
url = "https://docs.google.com/spreadsheets/d/1zIkgqXFkF2QesVgbA5osCFgl6dnnY8lXr_JiZHzU1-c/edit#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔮 Hệ Thống Luận Giải Thần Số Học")
st.markdown("---")

# --- SIDEBAR: NHẬP LIỆU ---
with st.sidebar:
    st.header("📝 Nhập Thông Tin")
    name = st.text_input("Họ và tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày tháng năm sinh:", min_value=datetime(1900, 1, 1))
    btn_calc = st.button("Luận Giải Ngay")

# --- MAIN: KẾT QUẢ & LƯU TRỮ ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Kết Quả Phân Tích")
    if btn_calc and name:
        # Thuật toán tính Số chủ đạo chuẩn
        s = dob.strftime("%d%m%Y")
        total = sum(int(i) for i in s)
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        
        st.success(f"Khách hàng: **{name}**")
        st.info(f"Con số chủ đạo: **Số {total}**")
        
        # Nút Lưu - Đã thêm cơ chế ép buộc ghi dữ liệu
        if st.button("❤️ Lưu kết quả này"):
            try:
                # Đọc dữ liệu cũ (không dùng cache để đảm bảo dữ liệu mới nhất)
                df_old = conn.read(spreadsheet=url, ttl=0)
                
                # Tạo dòng mới (Khớp chính xác tên cột trong Sheets của bạn)
                new_row = pd.DataFrame([{
                    "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Họ Tên": name,
                    "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                    "Số Chủ Đạo": str(total),
                    "Số Điện Thoại": str(phone)
                }])
                
                # Ghi đè cập nhật
                df_final = pd.concat([df_old, new_row], ignore_index=True)
                conn.update(spreadsheet=url, data=df_final)
                
                st.toast("Đã lưu vào Google Sheets!", icon="✅")
                st.rerun() 
            except Exception as e:
                st.error(f"Lỗi: {e}")
    else:
        st.write("Vui lòng nhập thông tin bên trái.")

with col2:
    st.subheader("⭐ Danh Sách Đã Lưu")
    try:
        data = conn.read(spreadsheet=url, ttl=0)
        st.dataframe(data, use_container_width=True, hide_index=True)
    except:
        st.info("Chưa có dữ liệu.")
