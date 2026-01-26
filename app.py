import streamlit as st
import pandas as pd

# 1. Cấu hình trang
st.set_page_config(page_title="Thần Số Học Pro 2026", page_icon="✨")

# 2. Khởi tạo kho lưu trữ trong session (nếu chưa có)
if 'saved_results' not in st.session_state:
    st.session_state.saved_results = []

st.title("🔮 Hệ Thống Luận Giải Thần Số Học")
st.markdown("---")

# --- KHU VỰC 1: NHẬP THÔNG TIN ---
with st.sidebar:
    st.header("📝 Nhập Thông Tin")
    name = st.text_input("Họ và tên:")
    dob = st.date_input("Ngày tháng năm sinh:")
    btn_calc = st.button("Luận Giải Ngay")

# --- KHU VỰC 2: HIỂN THỊ KẾT QUẢ ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Kết Quả Phân Tích")
    if btn_calc:
        # Giả lập tính toán con số chủ đạo (Bạn thay logic thật vào đây)
        result_num = (dob.day + dob.month + dob.year) % 9 or 9
        
        # Hiển thị nội dung
        st.success(f"Chủ nhân: **{name}**")
        st.info(f"Con số chủ đạo của bạn là: **Số {result_num}**")
        st.write("Mô tả: Bạn là người có tố chất lãnh đạo và đầy sáng tạo...") # Thay bằng nội dung bạn muốn

        # Nút "Like" để lưu kết quả
        if st.button("❤️ Lưu vào danh sách yêu thích"):
            new_entry = {"Tên": name, "Ngày sinh": str(dob), "Số chủ đạo": result_num}
            st.session_state.saved_results.append(new_entry)
            st.toast("Đã lưu kết quả thành công!")
    else:
        st.write("Vui lòng nhập thông tin ở thanh bên và nhấn nút để xem kết quả.")

# --- KHU VỰC 3: LƯU KẾT QUẢ (LIKE) ---
with col2:
    st.subheader("⭐ Danh Sách Đã Lưu")
    if st.session_state.saved_results:
        # Chuyển danh sách thành DataFrame để hiển thị bảng cho đẹp
        df = pd.DataFrame(st.session_state.saved_results)
        st.dataframe(df, use_container_width=True)
        
        if st.button("Xóa tất cả"):
            st.session_state.saved_results = []
            st.rerun()
    else:
        st.caption("Chưa có kết quả nào được lưu.")

st.markdown("---")
st.caption("© 2026 - Ứng dụng phát triển bởi Gemini Thought Partner")
