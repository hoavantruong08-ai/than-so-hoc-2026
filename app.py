import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮")

EXTENDED_DATA = {
    1: {"tag": "LÃNH ĐẠO", "summary": "Quyết đoán, độc lập."},
    2: {"tag": "SỨ GIẢ", "summary": "Hòa bình, kết nối."},
    3: {"tag": "SÁNG TẠO", "summary": "Năng động, linh hoạt."},
    4: {"tag": "KỶ LUẬT", "summary": "Thực tế, vững chãi."},
    5: {"tag": "TỰ DO", "summary": "Khám phá, trải nghiệm."},
    6: {"tag": "YÊU THƯƠNG", "summary": "Trách nhiệm, gia đình."},
    7: {"tag": "TRI THỨC", "summary": "Sâu sắc, tâm linh."},
    8: {"tag": "ĐIỀU HÀNH", "summary": "Tài chính, quyền lực."},
    9: {"tag": "NHÂN ÁI", "summary": "Bao dung, lý tưởng."},
    11: {"tag": "TRỰC GIÁC", "summary": "Tâm linh, nhạy bén."},
    22: {"tag": "KIẾN TẠO", "summary": "Tầm nhìn vĩ đại."}
}

def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

# --- 2. GIAO DIỆN ---
with st.sidebar:
    st.header("🔑 Tra cứu")
    name = st.text_input("Họ và Tên", "Nguyễn Văn A")
    dob = st.date_input("Ngày sinh", datetime(1990, 1, 1))
    phone = st.text_input("Số điện thoại", "")
    submitted = st.button("🚀 KHÁM PHÁ")

if submitted:
    # Tính số chủ đạo
    b_num = get_root_number(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    res = EXTENDED_DATA.get(b_num, EXTENDED_DATA[1])

    # --- 3. LƯU DỮ LIỆU (KHỚP DẤU SẮC) ---
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_old = conn.read(ttl=0)
        
        new_row = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": name,
            "Ngày Sinh": dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": str(b_num),
            "Số Điện Thoại": phone if phone else "N/A"
        }])
        
        df_updated = pd.concat([df_old, new_row], ignore_index=True)
        conn.update(data=df_updated)
        st.success("✅ Đã lưu thông tin vào Google Sheets!")
    except Exception as e:
        st.error(f"Lỗi: {e}")

    # Hiển thị
    st.header(f"Kết quả: {name}")
    st.metric("Số chủ đạo", b_num)
    st.subheader(res['tag'])
    st.write(res['summary'])
