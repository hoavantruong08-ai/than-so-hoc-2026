import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# --- 2. DỮ LIỆU ---
EXTENDED_DATA = {
    1: {"icon": "🦁", "tag": "LÃNH ĐẠO", "summary": "Số 1: Độc lập và quyết đoán.", "personality": "Bạn có ý chí mạnh mẽ."},
    2: {"icon": "🤝", "tag": "SỨ GIẢ", "summary": "Số 2: Hợp tác và kết nối.", "personality": "Bạn có khả năng lắng nghe tuyệt vời."},
    3: {"icon": "🎨", "tag": "TRUYỀN CẢM HỨNG", "summary": "Số 3: Sáng tạo và niềm vui.", "personality": "Bạn giàu trí tưởng tượng."},
    4: {"icon": "🧱", "tag": "XÂY DỰNG", "summary": "Số 4: Kỷ luật và thực tế.", "personality": "Bạn làm việc có hệ thống."},
    5: {"icon": "✈️", "tag": "THÁM HIỂM", "summary": "Số 5: Tự do và trải nghiệm.", "personality": "Bạn yêu thích sự đổi mới."},
    6: {"icon": "❤️", "tag": "NUÔI DƯỠNG", "summary": "Số 6: Yêu thương và trách nhiệm.", "personality": "Bạn tận tâm với gia đình."},
    7: {"icon": "🕵️", "tag": "TRIẾT HỌC", "summary": "Số 7: Phân tích và tâm linh.", "personality": "Bạn thích đào sâu kiến thức."},
    8: {"icon": "💰", "tag": "ĐIỀU HÀNH", "summary": "Số 8: Quyền lực và tài chính.", "personality": "Bạn có tham vọng lớn."},
    9: {"icon": "🌍", "tag": "NHÂN ÁI", "summary": "Số 9: Lý tưởng và nhân đạo.", "personality": "Bạn có trái tim bao dung."},
    11: {"icon": "✨", "tag": "TRỰC GIÁC", "summary": "Số 11: Thức tỉnh tâm linh.", "personality": "Trực giác bạn rất nhạy bén."},
    22: {"icon": "🏗️", "tag": "KIẾN TẠO", "summary": "Số 22: Biến ý tưởng thành hiện thực.", "personality": "Tầm nhìn xa trông rộng."}
}

def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

# --- 3. GIAO DIỆN ---
with st.sidebar:
    st.header("🔑 Tra Cứu")
    name = st.text_input("Họ và Tên", "Nguyễn Văn A")
    dob = st.date_input("Ngày Sinh", datetime(1990, 1, 1))
    phone = st.text_input("Số Điện Thoại", "")
    btn = st.button("🚀 KHÁM PHÁ")

if btn:
    # Tính toán
    b_num = get_root_number(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    d_num = get_root_number(b_num + len(name.replace(" ", "")))
    res = EXTENDED_DATA.get(b_num, EXTENDED_DATA[1])

    # Ghi vào Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_old = conn.read(ttl=0)
        new_data = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": name,
            "Ngày Sinh": dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": str(b_num),
            "Số Điện Thoại": phone if phone else "N/A"
        }])
        df_updated = pd.concat([df_old, new_data], ignore_index=True)
        conn.update(data=df_updated)
        st.success("✅ Đã lưu dữ liệu thành công!")
    except Exception as e:
        st.error(f"Lỗi lưu Sheet: {e}")

    # Hiển thị kết quả
    st.subheader(f"🔮 Kết Quả: {name.upper()}")
    c1, c2 = st.columns(2)
    c1.metric("SỐ CHỦ ĐẠO", b_num)
    c2.metric("SỐ ĐỊNH MỆNH", d_num)
    st.markdown(f"### {res['icon']} {res['tag']}")
    st.write(res['summary'])
    st.info(res['personality'])
