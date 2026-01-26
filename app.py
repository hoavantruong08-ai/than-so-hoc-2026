import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Cấu hình trang (Tên app hiển thị trên trình duyệt)
st.set_page_config(page_title="Thần Số Học Pro 2026", page_icon="🔮", layout="wide")

# 2. Kết nối Google Sheets 
# Thay link dưới đây bằng link file Google Sheets của bạn
url = "https://docs.google.com/spreadsheets/d/1zlkgqXFkF2QesVgbA5osCFgl6dnny8IXr_jiZHzU1-c/edit#gid=0"
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔮 Hệ Thống Luận Giải Thần Số Học")
st.markdown("---")

# --- SIDEBAR: KHU VỰC NHẬP THÔNG TIN ---
with st.sidebar:
    st.header("📝 Nhập Thông Tin")
    name = st.text_input("Họ và tên:")
    phone = st.text_input("Số điện thoại:")
    dob = st.date_input("Ngày tháng năm sinh:", min_value=datetime(1900, 1, 1))
    
    btn_calc = st.button("Luận Giải Ngay")

# --- MAIN: HIỂN THỊ KẾT QUẢ & LƯU TRỮ ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🔍 Kết Quả Phân Tích")
    if btn_calc and name:
        # Thuật toán tính Số chủ đạo (Cộng dồn ngày sinh)
        total = dob.day + dob.month + dob.year
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        result_num = total
        
        # Hiển thị kết quả đẹp mắt
        st.success(f"Khách hàng: **{name}**")
        st.info(f"Con số chủ đạo của bạn là: **Số {result_num}**")
        st.write(f"📞 SĐT: {phone}")
        
        # NÚT LƯU LÊN ĐÁM MÂY (LIKE)
        if st.button("❤️ Lưu vào Danh Sách Đã Lưu"):
            try:
                # Đọc dữ liệu cũ
                existing_data = conn.read(spreadsheet=url)
                
                # Tạo dòng dữ liệu mới khớp với các cột trong ảnh của bạn
                new_entry = pd.DataFrame([{
                    "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Họ Tên": name,
                    "Ngày Sinh": str(dob),
                    "Số Chủ Đạo": result_num,
                    "Số Điện Thoại": phone
                }])
                
                # Ghi đè cập nhật
                updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                conn.update(spreadsheet=url, data=updated_df)
                st.toast("Đã lưu vào Google Sheets thành công!", icon="✅")
            except Exception as e:
                st.error(f"Lỗi khi lưu: {e}")
    else:
        st.write("Vui lòng nhập đầy đủ thông tin bên trái để xem kết quả.")

with col2:
    st.subheader("⭐ Danh Sách Đã Lưu")
    # Hiển thị bảng dữ liệu từ Google Sheets
    try:
        data = conn.read(spreadsheet=url)
        st.dataframe(data, use_container_width=True, hide_index=True)
    except:
        st.info("Hiện tại chưa có dữ liệu nào được lưu.")

st.markdown("---")
st.caption("© 2026 - Ứng dụng phát triển bởi Gemini Thought Partner")
