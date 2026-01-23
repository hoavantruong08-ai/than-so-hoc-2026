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
    .advice-box { background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin-bottom: 20px; }
    .welcome-text { text-align: center; color: #8e44ad; font-weight: bold; font-size: 1.1em; padding: 10px; background: #f9f0ff; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DỮ LIỆU MẪU ---
EXTENDED_DATA = {
    1: {"icon": "🦁", "tag": "NHÀ LÃNH ĐẠO TIÊN PHONG", "summary": "Số 1 đại diện cho sự khởi đầu, độc lập và quyết đoán.", "personality": "Bạn có ý chí mạnh mẽ, thích tự quyết định con đường mình đi.", "month_tips": "Tháng này hãy tập trung vào các dự án cá nhân mới."},
    2: {"icon": "🤝", "tag": "SỨ GIẢ HÒA BÌNH", "summary": "Số 2 là con số của sự hợp tác, nhạy cảm và ngoại giao.", "personality": "Bạn có khả năng lắng nghe tuyệt vời.", "month_tips": "Lắng nghe trực giác của bạn nhiều hơn."},
    3: {"icon": "🎨", "tag": "NGƯỜI TRUYỀN CẢM HỨNG", "summary": "Số 3 tượng trưng cho sự sáng tạo và giao tiếp.", "personality": "Bạn là người hướng ngoại, giàu trí tưởng tượng.", "month_tips": "Hãy tự tin chia sẻ ý tưởng của bạn."},
    4: {"icon": "🧱", "tag": "NGƯỜI XÂY DỰNG NỀN TẢNG", "summary": "Số 4 đại diện cho sự ổn định và thực tế.", "personality": "Bạn làm việc có hệ thống và đáng tin cậy.", "month_tips": "Lập kế hoạch tài chính chi tiết."},
    5: {"icon": "✈️", "tag": "NHÀ THÁM HIỂM TỰ DO", "summary": "Số 5 là con số của sự thay đổi và trải nghiệm.", "personality": "Bạn yêu thích sự tự do và khám phá.", "month_tips": "Những chuyến đi bất ngờ sẽ mang lại cơ hội."},
    6: {"icon": "❤️", "tag": "NGƯỜI NUÔI DƯỠNG TẬN TÂM", "summary": "Số 6 tượng trưng cho tình yêu thương và gia đình.", "personality": "Bạn ấm áp và luôn chăm sóc người khác.", "month_tips": "Dành thời gian cho gia đình."},
    7: {"icon": "🕵️", "tag": "NHÀ TRIẾT HỌC SÂU SẮC", "summary": "Số 7 đại diện cho sự phân tích và tâm linh.", "personality": "Bạn thích đào sâu kiến thức và sự yên tĩnh.", "month_tips": "Một cuốn sách mới sẽ giúp khai mở tư duy."},
    8: {"icon": "💰", "tag": "NHÀ ĐIỀU HÀNH CHIẾN LƯỢC", "summary": "Số 8 là con số của quyền lực và sự cân bằng.", "personality": "Bạn có tham vọng lớn và khả năng kinh doanh.", "month_tips": "Quyết định đầu tư đúng đắn mang lại nguồn thu tốt."},
    9: {"icon": "🌍", "tag": "NGƯỜI NHÂN ÁI BAO DUNG", "summary": "Số 9 đại diện cho sự hoàn tất và lý tưởng.", "personality": "Bạn có trái tim nhân hậu, muốn giúp đỡ cộng đồng.", "month_tips": "Hãy học cách buông bỏ quá khứ."},
    11: {"icon": "✨", "tag": "BẬC THẦY TRỰC GIÁC", "summary": "Số 11 là con số tâm linh mạnh mẽ.", "personality": "Bạn có trực giác nhạy bén.", "month_tips": "Thực hành thiền định giúp cân bằng."},
    22: {"icon": "🏗️", "tag": "BẬC THẦY KIẾN TẠO", "summary": "Số 22 kiến tạo nên những công trình vĩ đại.", "personality": "Bạn biến ý tưởng không tưởng thành hiện thực.", "month_tips": "Đừng ngại dự án quy mô lớn."},
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
    st.markdown("---")
    submitted = st.button("🚀 KHÁM PHÁ ĐỊNH MỆNH")

# --- 5. XỬ LÝ LƯU GOOGLE SHEETS & HIỂN THỊ ---
if submitted:
    b_num, d_num = calculate_all(input_name, input_dob)
    res = EXTENDED_DATA.get(b_num, EXTENDED_DATA[1])
    
    # Lệnh lưu dữ liệu (Kết nối với Secrets bạn đã cài)
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_old = conn.read(ttl=0)
        new_row = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": input_name,
            "Ngày Sinh": input_dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": b_num,
            "Số Điện Thoại": "Đã tra cứu"
        }])
        df_updated = pd.concat([df_old, new_row], ignore_index=True)
        conn.update(data=df_updated)
        st.toast("✅ Đã lưu vào Google Sheets thành công!")
    except:
        pass

    # Hiển thị kết quả ra màn hình
    st.markdown(f"## 🔮 BẢN ĐỒ VẬN MỆNH: {input_name.upper()}")
    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.metric("SỐ CHỦ ĐẠO", b_num)
        st.metric("SỐ ĐỊNH MỆNH", d_num)
        st.markdown(f"### {res['icon']} {res['tag']}")
        st.info(res['summary'])
    with col2:
        with st.expander("📝 CHI TIẾT NHÂN CÁCH", expanded=True):
            st.write(res['personality'])
        st.success(f"💡 **Lời khuyên:** {res['month_tips']}")
else:
    st.markdown("<div class='welcome-text'>✨ Hệ thống đã sẵn sàng! Nhấn nút 'Khám Phá' để xem kết quả và lưu dữ liệu.</div>", unsafe_allow_html=True)
