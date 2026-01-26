import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Cấu hình trang
st.set_page_config(page_title="Luận Giải Thần Số Học 2026", page_icon="🔮")

st.title("🔮 Phần Mềm Luận Giải Thần Số Học")
st.markdown("---")

# 1. Kết nối với Google Sheets (Lấy thông tin từ Secrets)
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Lỗi kết nối Secrets! Vui lòng kiểm tra lại bảng đen trong Settings.")
    st.stop()

# 2. Form nhập liệu
with st.form(key="input_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Họ và tên:")
        phone = st.text_input("Số điện thoại:")
    with col2:
        dob = st.date_input("Ngày tháng năm sinh:")
        gender = st.selectbox("Giới tính:", ["Nam", "Nữ", "Khác"])

    submit_button = st.form_submit_button(label="Luận Giải & Lưu Dữ Liệu")

# 3. Xử lý dữ liệu khi nhấn nút
if submit_button:
    if name and phone:
        try:
            # Đọc dữ liệu hiện tại từ Sheet
            existing_data = conn.read(worksheet="Sheet1", usecols=[0,1,2,3])
            
            # Tạo dòng dữ liệu mới
            new_data = pd.DataFrame([{
                "Họ Tên": name,
                "Số Điện Thoại": phone,
                "Ngày Sinh": str(dob),
                "Giới Tính": gender
            }])
            
            # Kết hợp dữ liệu cũ và mới
            updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            
            # Cập nhật ngược lại Google Sheet
            conn.update(worksheet="Sheet1", data=updated_df)
            
            st.balloons()
            st.success(f"Chúc mừng {name}! Dữ liệu đã được lưu thành công vào Google Sheet.")
            st.info("Hệ thống đang tính toán các chỉ số thần số học cho bạn...")
            
        except Exception as e:
            st.error(f"Lỗi khi lưu dữ liệu: {e}")
            st.warning("Mẹo: Hãy chắc chắn bạn đã chia sẻ Sheet cho Email Service Account với quyền 'Editor'.")
    else:
        st.warning("Vui lòng nhập đầy đủ Họ tên và Số điện thoại!")

st.markdown("---")
st.caption("Phát triển bởi AI Collaborator - 2026")
