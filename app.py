import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# 1. Cấu hình giao diện
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮")

# 2. Hàm tính toán số chủ đạo
def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

# 3. Sidebar nhập liệu
with st.sidebar:
    st.header("🔑 Thông tin tra cứu")
    name = st.text_input("Họ và Tên", "Nguyễn Văn A")
    dob = st.date_input("Ngày sinh", datetime(1990, 1, 1))
    phone = st.text_input("Số điện thoại", "")
    submitted = st.button("🚀 KHÁM PHÁ")

# 4. Xử lý khi nhấn nút
if submitted:
    # Tính số chủ đạo
    b_num = get_root_number(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    
    # KẾT NỐI VÀ LƯU GOOGLE SHEETS
    try:
        # Khởi tạo kết nối
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Đọc dữ liệu hiện tại
        df_old = conn.read(ttl=0)
        
        # Tạo dòng mới (Lưu ý: "Số" dùng dấu sắc khớp với Sheet)
        new_row = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": name,
            "Ngày Sinh": dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": str(b_num),
            "Số Điện Thoại": phone if phone else "N/A"
        }])
        
        # Gộp dữ liệu và cập nhật lên Sheet
        df_updated = pd.concat([df_old, new_row], ignore_index=True)
        conn.update(data=df_updated)
        st.success("✅ Đã lưu thông tin thành công!")
        
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối Sheet: {e}")

    # Hiển thị kết quả ra màn hình
    st.divider()
    st.header(f"Kết quả: {name.upper()}")
    st.metric("SỐ CHỦ ĐẠO CỦA BẠN", b_num)
    st.balloons()
