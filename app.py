import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học Toàn Diện 2026", page_icon="🔮", layout="wide")

# CSS tạo giao diện chuyên nghiệp
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #8e44ad; }
    .advice-box { background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin-bottom: 20px; }
    .welcome-text { text-align: center; color: #8e44ad; font-weight: bold; font-size: 1.1em; padding: 10px; background: #f9f0ff; border-radius: 10px; }
    .stDateInput div { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DỮ LIỆU MẪU (EXTENDED_DATA) ---
EXTENDED_DATA = {
    1: {"icon": "🦁", "tag": "NHÀ LÃNH ĐẠO TIÊN PHONG", "summary": "Số 1 đại diện cho sự khởi đầu, độc lập và quyết đoán.", "personality": "Bạn có ý chí mạnh mẽ, thích tự quyết định con đường mình đi.", "month_tips": "Tháng này hãy tập trung vào các dự án cá nhân mới."},
    2: {"icon": "🤝", "tag": "SỨ GIẢ HÒA BÌNH", "summary": "Số 2 là con số của sự hợp tác, nhạy cảm và ngoại giao.", "personality": "Bạn có khả năng lắng nghe tuyệt vời và luôn mong muốn sự hài hòa.", "month_tips": "Lắng nghe trực giác của bạn nhiều hơn trong các mối quan hệ."},
    3: {"icon": "🎨", "tag": "NGƯỜI TRUYỀN CẢM HỨNG", "summary": "Số 3 tượng trưng cho sự sáng tạo, niềm vui và giao tiếp.", "personality": "Bạn là người hướng ngoại, giàu trí tưởng tượng và có khiếu hài hước.", "month_tips": "Hãy tự tin chia sẻ ý tưởng của bạn với mọi người xung quanh."},
    4: {"icon": "🧱", "tag": "NGƯỜI XÂY DỰNG NỀN TẢNG", "summary": "Số 4 đại diện cho sự ổn định, kỷ luật và thực tế.", "personality": "Bạn làm việc có hệ thống, đáng tin cậy và rất coi trọng sự trung thực.", "month_tips": "Đã đến lúc lập kế hoạch tài chính chi tiết cho năm nay."},
    5: {"icon": "✈️", "tag": "NHÀ THÁM HIỂM TỰ DO", "summary": "Số 5 là con số của sự thay đổi, thích nghi và trải nghiệm.", "personality": "Bạn yêu thích sự tự do, thích khám phá và không ngại thử thách mới.", "month_tips": "Những chuyến đi mang lại cơ hội bất ngờ sẽ đến vào giữa tháng."},
    6: {"icon": "❤️", "tag": "NGƯỜI NUÔI DƯỠNG TẬN TÂM", "summary": "Số 6 tượng trưng cho tình yêu thương, gia đình và trách nhiệm.", "personality": "Bạn là người ấm áp, luôn chăm sóc và bảo vệ những người mình yêu quý.", "month_tips": "Dành nhiều thời gian hơn cho gia đình để tái tạo năng lượng."},
    7: {"icon": "🕵️", "tag": "NHÀ TRIẾT HỌC SÂU SẮC", "summary": "Số 7 đại diện cho sự phân tích, học hỏi và tâm linh.", "personality": "Bạn thích đào sâu kiến thức, thích sự yên tĩnh để suy ngẫm về cuộc sống.", "month_tips": "Một khóa học hoặc cuốn sách mới sẽ giúp bạn khai mở tư duy."},
    8: {"icon": "💰", "tag": "NHÀ ĐIỀU HÀNH CHIẾN LƯỢC", "summary": "Số 8 là con số của quyền lực, tiền bạc và sự cân bằng.", "personality": "Bạn có tham vọng lớn, khả năng kinh doanh và luôn hướng tới kết quả.", "month_tips": "Quyết định đầu tư đúng đắn sẽ mang lại nguồn thu tốt."},
    9: {"icon": "🌍", "tag": "NGƯỜI NHÂN ÁI BAO DUNG", "summary": "Số 9 đại diện cho sự hoàn tất, nhân đạo và lý tưởng.", "personality": "Bạn có trái tim nhân hậu, luôn muốn giúp đỡ cộng đồng và thế giới.", "month_tips": "Hãy học cách buông bỏ quá khứ để đón nhận những khởi đầu mới."},
    11: {"icon": "✨", "tag": "BẬC THẦY TRỰC GIÁC", "summary": "Số 11 là con số tâm linh mạnh mẽ, sự thức tỉnh và tầm nhìn.", "personality": "Bạn có trực giác cực kỳ nhạy bén và mang trong mình sứ mệnh truyền tin.", "month_tips": "Thực hành thiền định sẽ giúp bạn cân bằng lại cảm xúc."},
    22: {"icon": "🏗️", "tag": "BẬC THẦY KIẾN TẠO", "summary": "Số 22 là con số kiến tạo nên những công trình vĩ đại.", "personality": "Bạn có khả năng biến những ý tưởng không tưởng thành hiện thực thực tế.", "month_tips": "Đừng ngại bắt tay vào những dự án có quy mô lớn."},
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
    d_num = get_root_number(b_num + len(name.replace(" ", "")))
    return b_num, d_num

# --- 4. GIAO DIỆN NHẬP LIỆU ---
with st.sidebar:
    st.header("🔑 Thông Tin Tra Cứu")
    input_name = st.text_input("Nhập Họ và Tên", value="Nguyễn Văn A")
    input_dob = st.date_input("Chọn Ngày Sinh", value=datetime(1990, 1, 1), format="DD/MM/YYYY")
    input_phone = st.text_input("Số Điện Thoại (Để lưu thông tin)", value="")
    st.markdown("---")
    submitted = st.button("🚀 KHÁM PHÁ ĐỊNH MỆNH")

# --- 5. XỬ LÝ DỮ LIỆU VÀ LƯU SHEET ---
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
            "Số Chủ Đạo": b_num,
            "Số Điện Thoại": input_phone if input_phone else "Không có"
        }])
        df_updated = pd.concat([df_old, new_row], ignore_index=True)
        conn.update(data=df_updated)
        st.toast("✅ Đã lưu thông tin của bạn vào sổ mệnh!")
    except Exception as e:
        st.info("Hệ thống đang hoạt động ở chế độ xem nhanh.")

    # --- HIỂN THỊ KẾT QUẢ ---
    st.markdown(f"## 🔮 BẢN ĐỒ VẬN MỆNH CHI TIẾT 2026")
    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.metric("SỐ CHỦ ĐẠO", b_num)
        st.metric("SỐ ĐỊNH MỆNH", d_num)
        st.markdown(f"### {res['icon']} {res['tag']}")
        st.info(res['summary'])
        st.markdown(f"<div class='advice-box'><b>📬 Lời khuyên tháng:</b> {res['month_tips']}</div>", unsafe_allow_html=True)

    with col2:
        st.subheader("📊 Biểu Đồ Nhịp Sinh Học & Vận Thế 2026")
        chart_data = pd.DataFrame({"Năng Lượng": [4, 6, 8, 5, 9, 7, 4, 8, 6, 9, 3, 7]}, index=[f"T{i}" for i in range(1, 13)])
        st.line_chart(chart_data, color="#f39c12")
        
        with st.expander("📝 CHI TIẾT NHÂN CÁCH", expanded=True):
            st.markdown(res['personality'])

else:
    st.markdown("<div class='welcome-text'>✨ Hệ thống đã sẵn sàng! Điền thông tin bên trái và nhấn nút 'Khám Phá'.</div>", unsafe_allow_html=True)
