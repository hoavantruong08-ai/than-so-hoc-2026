import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Cấu hình trang
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# 2. Kết nối Google Sheets
# Dán chính xác link file Google Sheets của bạn vào đây
url = "https://docs.google.com/spreadsheets/d/1zlkgqXFkF2QesVgbA5osCFgl6dnny8IXr_jiZHzU1-c/edit#gid=0"
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
        # Thuật toán tính Số chủ đạo chuẩn (Cộng dồn các chữ số)
        def tinh_so_chu_dao(ngay_sinh):
            s = ngay_sinh.strftime("%d%m%Y")
            tong = sum(int(i) for i in s)
            while tong > 11 and tong != 22:
                tong = sum(int(digit) for digit in str(tong))
            return tong

        result_num = tinh_so_chu_dao(dob)
        
        # Hiển thị kết quả
        st.success(f"Khách hàng: **{name}**")
        st.info(f"Con số chủ đạo: **Số {result_num}**")
        
        # Nút Like để lưu lên Cloud
        if st.button("❤️ Lưu kết quả chính xác"):
            try:
                # Đọc dữ liệu cũ để tránh mất data
                existing_data = conn.read(spreadsheet=url)
                
                # Tạo dòng mới (Khớp 100% với tên cột trong ảnh của bạn)
                new_row = pd.DataFrame([{
                    "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Họ Tên": name,
                    "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                    "Số Chủ Đạo": result_num,
                    "Số Điện Thoại": phone
                }])
                
                # Cập nhật lên Google Sheets
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                conn.update(spreadsheet=url, data=updated_df)
                st.toast("Đã lưu vào Google Sheets thành công!", icon="✅")
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}. Hãy đảm bảo Sheet đã được Share 'Anyone with the link can edit'.")
    else:
        st.write("Vui lòng điền thông tin và nhấn nút.")

with col2:
    st.subheader("⭐ Danh Sách Đã Lưu")
    try:
        # Luôn đọc bản mới nhất từ Cloud để hiển thị
        data = conn.read(spreadsheet=url)
        st.dataframe(data, use_container_width=True, hide_index=True)
    except:
        st.info("Chưa có dữ liệu nào được lưu.")

st.markdown("---")
st.caption("© 2026 - App được hỗ trợ bởi Gemini Thought Partner")
