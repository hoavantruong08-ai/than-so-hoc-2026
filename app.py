import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮")

def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

# --- 2. GIAO DIỆN ---
with st.sidebar:
    st.header("🔑 Thông tin tra cứu")
    name = st.text_input("Họ và Tên", "Nguyễn Văn A")
    dob = st.date_input("Ngày sinh", datetime(1990, 1, 1))
    phone = st.text_input("Số điện thoại", "")
    submitted = st.button("🚀 KHÁM PHÁ")

# --- 3. XỬ LÝ DỮ LIỆU ---
if submitted:
    # Tính toán
    b_num = get_root_number(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    
    try:
        # Kết nối Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Đọc dữ liệu hiện có
        df_old = conn.read(ttl=0)
        
        # Tạo dòng mới (Cột E dùng dấu sắc chuẩn: "Số Điện Thoại")
        new_row = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": name,
            "Ngày Sinh": dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": str(b_num),
            "Số Điện Thoại": phone if phone else "N/A"
        }])
        
        # Cập nhật lên Google Sheets
        df_updated = pd.concat([df_old, new_row], ignore_index=True)
        conn.update(data=df_updated)
        st.success("✅ Tuyệt vời! Dữ liệu đã được ghi vào Sổ Mệnh.")
        
    except Exception as e:
        st.error(f"⚠️ Lỗi kết nối (Hãy kiểm tra quyền Editor của Sheet): {e}")

    # Hiển thị kết quả ra màn hình
    st.divider()
    st.header(f"Kết quả cho: {name.upper()}")
    st.metric("SỐ CHỦ ĐẠO", b_num)
    st.balloons()
