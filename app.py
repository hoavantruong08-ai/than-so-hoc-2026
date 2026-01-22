import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học Toàn Diện 2026", page_icon="🔮", layout="wide")

# CSS tạo giao diện chuyên nghiệp
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #8e44ad; }
    .advice-box { background-color: #f0f7ff; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; margin-bottom: 20px; }
    .welcome-text { text-align: center; color: #8e44ad; font-weight: bold; font-size: 1.1em; padding: 10px; background: #f9f0ff; border-radius: 10px; margin-bottom: 20px; }
    /* Tùy chỉnh hiển thị date input */
    .stDateInput div { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HÀM TÍNH TOÁN ---
def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def calculate_all(name, dob):
    d_sum = get_root_number(dob.day)
    m_sum = get_root_number(dob.month)
    y_sum = get_root_number(sum(int(d) for d in str(dob.year)))
    b_num = get_root_number(d_sum + m_sum + y_sum)
    d_num = get_root_number(b_num + len(name))
    return b_num, d_num

# --- 3. KHO DỮ LIỆU ĐẦY ĐỦ (EXTENDED_DATA) ---
EXTENDED_DATA = {
    1: {
        "tag": "NHÀ TIÊN PHONG ĐỘC LẬP", "icon": "🥇", "color": "#FFD700",
        "wave": [80, 100, 70, 90, 60, 50, 80, 100, 70, 90, 85, 95],
        "summary": "Số 1 đại diện cho sự khởi đầu, lòng can đảm và ý chí dẫn đầu tuyệt vời.",
        "personality": "- **Ưu điểm:** Khả năng lãnh đạo bẩm sinh, quyết đoán.\n- **Nhược điểm:** Cái tôi cao, đôi khi độc đoán.",
        "career": "Năm 2026 là lúc bứt phá mạnh mẽ. Phù hợp làm quản lý, khởi nghiệp. Đỉnh cao: Tháng 2 & 8.",
        "love": "Cần người thấu hiểu khát vọng cá nhân. Tránh tranh giành quyền kiểm soát.",
        "month_tips": "T2: Thời điểm vàng cho các dự án mới."
    },
    2: {
        "tag": "NGƯỜI KẾT NỐI HÒA BÌNH", "icon": "🤝", "color": "#00CECB",
        "wave": [40, 60, 80, 100, 80, 60, 40, 50, 70, 90, 80, 60],
        "summary": "Số 2 là con số của sự cân bằng, trực giác và khả năng ngoại giao.",
        "personality": "- **Ưu điểm:** Nhạy cảm, biết lắng nghe.\n- **Nhược điểm:** Dễ tổn thương, hay do dự.",
        "career": "Thành công thông qua hợp tác. Hãy tìm kiếm đối tác chiến lược.",
        "love": "Sự dịu dàng là vũ khí. Hãy chia sẻ cảm xúc nhiều hơn để gắn kết.",
        "month_tips": "T4: Năng lượng kết nối cực mạnh, tốt cho đàm phán."
    },
    3: {
        "tag": "BẬC THẦY TRUYỀN CẢM HỨNG", "icon": "🎭", "color": "#FF5E5B",
        "wave": [70, 90, 100, 80, 60, 80, 90, 70, 100, 80, 60, 90],
        "summary": "Số 3 tượng trưng cho sự sáng tạo, niềm vui và sức mạnh ngôn từ.",
        "personality": "- **Ưu điểm:** Lạc quan, giao tiếp xuất sắc.\n- **Nhược điểm:** Dễ xao nhãng, thiếu kiên trì.",
        "career": "Vận may đến từ các mối quan hệ. Nghệ thuật, viết lách mang lại thu nhập đột phá.",
        "love": "Bạn là thỏi nam châm thu hút. Hãy chọn người có thể cùng bạn chia sẻ niềm vui.",
        "month_tips": "T3 & T9: Khả năng sáng tạo bùng nổ đỉnh điểm."
    },
    4: {
        "tag": "NHÀ KIẾN THIẾT KIÊN ĐỊNH", "icon": "🏗️", "color": "#2c3e50",
        "wave": [50, 60, 70, 85, 95, 100, 80, 70, 60, 55, 65, 75],
        "summary": "Số 4 đại diện cho sự vững chãi, kỷ luật và thực tế.",
        "personality": "- **Ưu điểm:** Thực tế, tỉ mỉ, đáng tin cậy.\n- **Nhược điểm:** Cứng nhắc, đôi khi quá bảo thủ.",
        "career": "Năm củng cố nền móng. Các ngành kỹ thuật, tài chính, quản lý sẽ rất thuận lợi.",
        "love": "Cần sự ổn định và cam kết lâu dài. Hãy thể hiện tình yêu bằng hành động.",
        "month_tips": "T6: Tập trung vào các mục tiêu tài chính dài hạn."
    },
    5: {
        "tag": "NHÀ THÁM HIỂM TỰ DO", "icon": "✈️", "color": "#FFAD05",
        "wave": [90, 70, 100, 80, 90, 100, 75, 60, 90, 80, 100, 90],
        "summary": "Số 5 là con số của sự thay đổi, thích nghi và trải nghiệm.",
        "personality": "- **Ưu điểm:** Linh hoạt, giàu năng lượng.\n- **Nhược điểm:** Ham vui, khó tập trung mục tiêu.",
        "career": "Vận hành tốt trong môi trường biến động. Thích hợp làm du lịch, Marketing.",
        "love": "Cần sự mới mẻ và không gian riêng. Tránh sự gò bó quá mức.",
        "month_tips": "T5 & T11: Những chuyến đi mang lại cơ hội bất ngờ."
    },
    6: {
        "tag": "NGƯỜI NUÔI DƯỠNG ẤM ÁP", "icon": "🏡", "color": "#7FB069",
        "wave": [30, 50, 70, 90, 100, 80, 60, 50, 80, 95, 100, 50],
        "summary": "Số 6 tượng trưng cho trách nhiệm, gia đình và tình yêu thương.",
        "personality": "- **Ưu điểm:** Giàu lòng trắc ẩn, trách nhiệm cao.\n- **Nhược điểm:** Hay ôm đồm, lo lắng thái quá.",
        "career": "Thành công trong các ngành giáo dục, y tế, chăm sóc khách hàng.",
        "love": "Gia đình là ưu tiên số 1. Năm tuyệt vời để hàn gắn và xây tổ ấm.",
        "month_tips": "T10: Dành trọn thời gian cho người thân yêu."
    },
    7: {
        "tag": "CHIẾN LƯỢC GIA TRÍ TUỆ", "icon": "🧠", "color": "#6C5CE7",
        "wave": [20, 40, 30, 60, 80, 50, 90, 100, 70, 40, 30, 20],
        "summary": "Số 7 là con số của tri thức, chiều sâu và sự thấu suốt tâm linh.",
        "personality": "- **Ưu điểm:** Khả năng phân tích sắc bén, trực giác mạnh.\n- **Nhược điểm:** Khép kín, đôi khi hay xa cách.",
        "career": "Năm của học tập và nghiên cứu. Trí tuệ tăng trưởng vượt bậc trong năm 2026.",
        "love": "Cần sự đồng điệu về tư duy và tâm hồn hơn là vật chất.",
        "month_tips": "T8: Đỉnh cao trí tuệ, hãy tin vào trực giác."
    },
    8: {
        "tag": "NHÀ ĐIỀU HÀNH CHIẾN LƯỢC", "icon": "💰", "color": "#D4AF37",
        "wave": [60, 70, 80, 90, 100, 80, 60, 50, 40, 30, 50, 80],
        "summary": "Số 8 là con số của vật chất, quyền lực và sự cân bằng.",
        "personality": "- **Ưu điểm:** Tham vọng, quản trị tài chính giỏi.\n- **Nhược điểm:** Thực dụng, dễ khô khan.",
        "career": "Năm thu hoạch lớn về tài chính. Tiền bạc sẽ đổ về nếu làm việc công bằng.",
        "love": "Hãy bỏ 'áo sếp' khi về nhà. Gia đình cần sự ấm áp hơn mệnh lệnh.",
        "month_tips": "T5: Vận tài lộc cực phát, hãy nắm bắt ngay."
    },
    9: {
        "tag": "NGƯỜI NHÂN ÁI BAO DUNG", "icon": "❤️", "color": "#EF476F",
        "wave": [10, 30, 50, 70, 90, 100, 80, 60, 40, 20, 50, 100],
        "summary": "Số 9 đại diện cho sự hoàn tất, lý tưởng và lòng nhân ái.",
        "personality": "- **Ưu điểm:** Bao dung, lý tưởng sống cao đẹp.\n- **Nhược điểm:** Dễ mơ mộng, đôi khi thiếu thực tế.",
        "career": "Phù hợp các hoạt động cộng đồng, nhân đạo hoặc giáo dục tầm vóc lớn.",
        "love": "Tình yêu mang tính hy sinh và cống hiến. Hãy khép lại những tổn thương cũ.",
        "month_tips": "T12: Kết thúc một chu kỳ cũ để đón nhận vận may mới."
    }
}

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🔮 BẢN ĐỒ VẬN MỆNH CHI TIẾT 2026")

with st.sidebar:
    st.header("🔑 Thông Tin Tra Cứu")
    input_name = st.text_input("Nhập Họ và Tên", value="Lưu Xuân Quảng")
    
    # SỬA ĐỊNH DẠNG NGÀY THÁNG TẠI ĐÂY
    input_dob = st.date_input(
        "Chọn Ngày Sinh (Ngày/Tháng/Năm)", 
        value=datetime(1983, 1, 1), 
        min_value=datetime(1950, 1, 1),
        max_value=datetime(2026, 12, 31),
        format="DD/MM/YYYY"  # Định dạng chuẩn Việt Nam
    )
    st.markdown("---")
    submitted = st.button("🚀 KHÁM PHÁ ĐỊNH MỆNH")

# Tự động tính toán
b_num, d_num = calculate_all(input_name, input_dob)
res = EXTENDED_DATA.get(b_num, EXTENDED_DATA[1])

if not submitted:
    st.markdown("<div class='welcome-text'>✨ Hệ thống đã sẵn sàng! Đây là kết quả xem nhanh theo dữ liệu mẫu. Nhấn nút 'Khám Phá' để xem hiệu ứng! ✨</div>", unsafe_allow_html=True)

# --- HIỂN THỊ KẾT QUẢ ---
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.metric("SỐ CHỦ ĐẠO", b_num)
    st.metric("SỐ ĐỊNH MỆNH", d_num)
    st.markdown(f"### {res['icon']} {res['tag']}")
    st.info(res['summary'])
    st.markdown(f"<div class='advice-box'><b>📅 Lời khuyên tháng:</b> {res['month_tips']}</div>", unsafe_allow_html=True)

with col2:
    st.subheader("📈 Biểu Đồ Nhịp Sinh Học & Vận Thế 2026")
    chart_data = pd.DataFrame(res["wave"], index=[f"T{i}" for i in range(1,13)], columns=["Năng lượng"])
    st.line_chart(chart_data, color=res["color"])

    with st.expander("🎭 CHI TIẾT NHÂN CÁCH", expanded=True):
        st.markdown(res['personality'])
    with st.expander("💼 SỰ NGHIỆP & TÀI CHÍNH"):
        st.write(res['career'])
    with st.expander("💖 DỰ BÁO TÌNH DUYÊN"):
        st.write(res['love'])

# --- CHIA SẺ ---
st.markdown("---")
st.markdown("<h4 style='text-align: center;'>📢 Chia sẻ kết quả cho bạn bè</h4>", unsafe_allow_html=True)
share_url = "https://xem-than-so-hoc-2026.streamlit.app"
c1, c2 = st.columns(2)
with c1:
    st.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank"><button style="width:100%; background:#1877F2; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">Chia sẻ Facebook</button></a>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<a href="https://zalo.me/s/share/?url={share_url}" target="_blank"><button style="width:100%; background:#0068FF; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">Chia sẻ Zalo</button></a>', unsafe_allow_html=True)

if submitted:
    st.balloons()

