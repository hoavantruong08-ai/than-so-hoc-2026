import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học Toàn Diện 2026", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #8e44ad; }
    .welcome-text { text-align: center; color: #8e44ad; font-weight: bold; font-size: 1.2em; padding: 20px; background: #f9f0ff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. KHO DỮ LIỆU ---
EXTENDED_DATA = {
    1: {"icon": "🦁", "tag": "NHÀ LÃNH ĐẠO", "summary": "Số 1 đại diện cho sự khởi đầu và độc lập.", "personality": "Bạn có ý chí mạnh mẽ.", "month_tips": "Tập trung vào dự án mới."},
    2: {"icon": "🤝", "tag": "SỨ GIẢ HÒA BÌNH", "summary": "Số 2 là sự hợp tác và ngoại giao.", "personality": "Bạn lắng nghe tuyệt vời.", "month_tips": "Lắng nghe trực giác."},
    3: {"icon": "🎨", "tag": "NGƯỜI TRUYỀN CẢM HỨNG", "summary": "Số 3 là sự sáng tạo và niềm vui.", "personality": "Bạn giàu trí tưởng tượng.", "month_tips": "Chia sẻ ý tưởng."},
    4: {"icon": "🧱", "tag": "NGƯỜI XÂY DỰNG", "summary": "Số 4 là sự ổn định và kỷ luật.", "personality": "Bạn làm việc hệ thống.", "month_tips": "Lập kế hoạch chi tiết."},
    5: {"icon": "✈️", "tag": "NHÀ THÁM HIỂM", "summary": "Số 5 là sự thay đổi và tự do.", "personality": "Bạn thích khám phá.", "month_tips": "Đón nhận thử thách."},
    6: {"icon": "❤️", "tag": "NGƯỜI NUÔI DƯỠNG", "summary": "Số 6 là tình yêu và trách nhiệm.", "personality": "Bạn ấm áp, tận tâm.", "month_tips": "Dành thời gian cho gia đình."},
    7: {"icon": "🕵️", "tag": "NHÀ TRIẾT HỌC", "summary": "Số 7 là sự học hỏi và tâm linh.", "personality": "Bạn thích đào sâu kiến thức.", "month_tips": "Dành thời gian chiêm nghiệm."},
    8: {"icon": "💰", "tag": "NHÀ ĐIỀU HÀNH", "summary": "Số 8 là quyền lực và cân bằng.", "personality": "Bạn có tham vọng lớn.", "month_tips": "Đầu tư đúng đắn."},
    9: {"icon": "🌍", "tag": "NGƯỜI NHÂN ÁI", "summary": "Số 9 là nhân đạo và lý tưởng.", "personality": "Bạn có trái tim bao dung.", "month_tips": "Học cách buông bỏ."},
    11: {"icon": "✨", "tag": "BẬC THẦY TRỰC GIÁC", "summary": "Số 11 là sự thức tỉnh tâm linh.", "personality": "Trực giác bạn rất nhạy.", "month_tips": "Thực hành thiền định."},
    22: {"icon": "🏗️", "tag": "BẬC THẦY KIẾN TẠO", "summary": "Số 22 biến ý tưởng thành hiện thực.", "personality": "Tầm nhìn xa trông rộng.", "month_tips": "Bắt tay vào dự án lớn."}
}

# --- 3. HÀM TÍNH TOÁN ---
def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def calculate_all(name, dob):
    d_sum = get_root_number(dob.day)
    m_sum = get_root_number(dob.month)
    y_sum = get_root_number(sum(int(d) for d in str(dob.year)))
    b_num = get_root_number(d_sum + m_sum + y_sum)
    d_num = get_root_number(get_root_number(b_num) + get_root_number(len(name.replace(" ", ""))))
    return b_num, d_num

# --- 4. GIAO DIỆN ---
with st.sidebar:
    st.header("🔑 Thông Tin Tra Cứu")
    input_name = st.text_input("Nhập Họ và Tên", value="Nguyễn Văn A")
    input_dob = st.date_input("Chọn Ngày Sinh", value=datetime(1990, 1, 1), format="DD/MM/YYYY")
    input_phone = st.text_input("Số Điện Thoại", value="")
    st.markdown("---")
    submitted = st.button("🚀 KHÁM PHÁ ĐỊNH MỆNH")

# --- 5. XỬ LÝ LƯU SHEET & HIỂN THỊ ---
if submitted:
    b_num, d_num = calculate_all(input_name, input_dob)
    res = EXTENDED_DATA.get(b_num, EXTENDED_DATA[1])
    
    # Ghi dữ liệu vào Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_old = conn.read(ttl=0)
        new_row = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": input_name,
            "Ngày Sinh": input_dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": str(b_num),
            "Số Điện Thoại": input_phone if input_phone else "Ẩn"
        }])
        df_updated = pd.concat([df_old, new_row], ignore_index=True)
        conn.update(data=df_updated)
        st.toast("✅ Đã lưu dữ liệu thành công!")
    except Exception as e:
        st.error(f"Lỗi lưu Sheet: {e}")

    # Hiển thị
    st.markdown(f"## 🔮 KẾT QUẢ TRA CỨU: {input_name.upper()}")
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.metric("SỐ CHỦ ĐẠO", b_num)
        st.metric("SỐ ĐỊNH MỆNH", d_num)
        st.markdown(f"### {res['icon']} {res['tag']}")
    with col2:
        st.info(res['summary'])
        with st.expander("📝 XEM CHI TIẾT NHÂN CÁCH", expanded=True):
            st.write(res['personality'])
else:
    st.markdown("<div class='welcome-text'>✨ Hệ thống đã sẵn sàng!<br>Điền thông tin bên trái và nhấn nút 'Khám Phá'.</div>", unsafe_allow_html=True)
