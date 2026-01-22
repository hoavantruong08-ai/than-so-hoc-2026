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
        "personality": "- **Ưu điểm:** Bạn có khả năng lãnh đạo bẩm sinh, quyết đoán và luôn tiến về phía trước. Bạn không sợ khó khăn và luôn muốn tự tay tạo dựng cơ đồ.\n- **Nhược điểm:** Đôi khi quá tự tin dẫn đến độc đoán, cái tôi lớn khiến bạn khó lắng nghe lời khuyên từ người khác.",
        "career": "Năm 2026 là lúc bạn bứt phá. Phù hợp khởi nghiệp, làm quản lý hoặc nhận các dự án mới. Đỉnh cao: Tháng 2 và Tháng 8.",
        "love": "Cần một người đồng hành thấu hiểu khát vọng cá nhân của bạn. Tránh tranh cãi ai là người làm chủ trong nhà.",
        "month_tips": "T2: Thời điểm vàng để bắt đầu một kế hoạch mới đã ấp ủ lâu nay."
    },
    2: {
        "tag": "NGƯỜI KẾT NỐI HÒA BÌNH", "icon": "🤝", "color": "#00CECB",
        "wave": [40, 60, 80, 100, 80, 60, 40, 50, 70, 90, 80, 60],
        "summary": "Số 2 là con số của sự cân bằng, trực giác và khả năng ngoại giao tài tình.",
        "personality": "- **Ưu điểm:** Nhạy cảm, biết lắng nghe và luôn tìm kiếm giải pháp hòa bình. Bạn là chất keo gắn kết mọi tập thể.\n- **Nhược điểm:** Dễ bị tổn thương bởi nhận xét của người khác, đôi khi quá do dự không dám quyết định.",
        "career": "Thành công thông qua hợp tác. Đây không phải năm để hành động đơn độc. Hãy tìm kiếm đối tác chiến lược.",
        "love": "Sự dịu dàng của bạn là vũ khí mạnh nhất. Hãy chia sẻ cảm xúc nhiều hơn để tránh hiểu lầm.",
        "month_tips": "T4: Năng lượng kết nối cực mạnh, rất tốt cho việc ký kết hợp đồng."
    },
    3: {
        "tag": "BẬC THẦY TRUYỀN CẢM HỨNG", "icon": "🎭", "color": "#FF5E5B",
        "wave": [70, 90, 100, 80, 60, 80, 90, 70, 100, 80, 60, 90],
        "summary": "Số 3 tượng trưng cho sự sáng tạo, niềm vui và sức mạnh của ngôn từ.",
        "personality": "- **Ưu điểm:** Hài hước, lạc quan, có khả năng diễn đạt xuất sắc. Bạn luôn là tâm điểm của các cuộc vui.\n- **Nhược điểm:** Dễ bị xao nhãng, 'cả thèm chóng chán' và đôi khi nói quá nhiều mà thiếu hành động thực tế.",
        "career": "Vận may đến từ các mối quan hệ xã hội. Nghệ thuật, viết lách, bán hàng sẽ mang lại thu nhập đột phá.",
        "love": "Bạn thu hút nhiều vệ tinh xung quanh. Hãy chọn người có thể cùng bạn cười và cùng bạn sẻ chia áp lực cuộc sống.",
        "month_tips": "T3 & T9: Khả năng sáng tạo bùng nổ, hãy thực hiện các ý tưởng 'điên rồ' nhất."
    },
    4: {
        "tag": "NHÀ KIẾN THIẾT KIÊN ĐỊNH", "icon": "🏗️", "color": "#2c3e50",
        "wave": [50, 60, 70, 85, 95, 100, 80, 70, 60, 55, 65, 75],
        "summary": "Số 4 đại diện cho sự vững chãi, kỷ luật và thực tế.",
        "personality": "- **Ưu điểm:** Thực tế, tỉ mỉ, đáng tin cậy. Bạn xây dựng mọi thứ trên nền tảng vững chắc.\n- **Nhược điểm:** Cứng nhắc, đôi khi quá bảo thủ và khó thích nghi với thay đổi nhanh.",
        "career": "Năm củng cố nền móng. Các ngành kỹ thuật, tài chính, quản lý sẽ rất thuận lợi.",
        "love": "Cần sự ổn định và cam kết lâu dài. Hãy thể hiện tình yêu bằng hành động thực tế.",
        "month_tips": "T6: Tập trung vào các mục tiêu tài chính dài hạn."
    },
    5: {
        "tag": "NHÀ THÁM HIỂM TỰ DO", "icon": "✈️", "color": "#FFAD05",
        "wave": [90, 70, 100, 80, 90, 100, 75, 60, 90, 80, 100, 90],
        "summary": "Số 5 là con số của sự thay đổi, thích nghi và trải nghiệm.",
        "personality": "- **Ưu điểm:** Linh hoạt, giàu năng lượng, ham học hỏi.\n- **Nhược điểm:** Ham vui, khó tập trung mục tiêu và dễ bị cả thèm chóng chán.",
        "career": "Vận hành tốt trong môi trường biến động. Thích hợp làm du lịch, Marketing, sự kiện.",
        "love": "Cần sự mới mẻ và không gian riêng. Tránh sự gò bó quá mức.",
        "month_tips": "T5 & T11: Những chuyến đi mang lại cơ hội bất ngờ."
    },
    6: {
        "tag": "NGƯỜI NUÔI DƯỠNG ẤM ÁP", "icon": "🏡", "color": "#7FB069",
        "wave": [30, 50, 70, 90, 100, 80, 60, 50, 80, 95, 100, 50],
        "summary": "Số 6 tượng trưng cho trách nhiệm, gia đình và tình yêu thương.",
        "personality": "- **Ưu điểm:** Giàu lòng trắc ẩn, trách nhiệm cao, biết chăm sóc người khác.\n- **Nhược điểm:** Hay ôm đồm, lo lắng thái quá cho người khác mà quên bản thân.",
        "career": "Thành công trong các ngành giáo dục, y tế, chăm sóc khách hàng hoặc tư vấn.",
        "love": "Gia đình là ưu tiên số 1. Năm tuyệt vời để hàn gắn và xây tổ ấm.",
        "month_tips": "T10: Dành trọn thời gian chất lượng cho người thân yêu."
    },
    7: {
        "tag": "CHIẾN LƯỢC GIA TRÍ TUỆ", "icon": "🧠", "color": "#6C5CE7",
        "wave": [20, 40, 30, 60, 80, 50, 90, 100, 70, 40, 30, 20],
        "summary": "Số 7 là con số của tri thức, chiều sâu và sự thấu suốt tâm linh.",
        "personality": "- **Ưu điểm:** Khả năng phân tích sắc bén, trực giác mạnh, thích chiêm nghiệm.\n- **Nhược điểm:** Khép kín, đôi khi hay xa cách và khó hiểu đối với người xung quanh.",
        "career": "Năm của học tập và nghiên cứu. Trí tuệ tăng trưởng vượt bậc trong năm 2026.",
        "love": "Cần sự đồng điệu về tư duy và tâm hồn hơn là vật chất.",
        "month_tips": "T8: Đỉnh cao trí tuệ, hãy tin vào trực giác của mình."
    },
    8: {
        "tag": "NHÀ ĐIỀU HÀNH CHIẾN LƯỢC", "icon": "💰", "color": "#D4AF37",
        "wave": [60, 70, 80, 90, 100, 80, 60, 50, 40, 30, 50, 80],
        "summary": "Số 8 là con số của vật chất, quyền lực và sự cân bằng giữa nhân quả.",
        "personality": "- **Ưu điểm:** Kiên cường, tham vọng lớn, khả năng quản trị tài chính cực giỏi.\n- **Nhược điểm:** Dễ bị cuốn vào công việc mà quên mất gia đình, đôi khi thực dụng.",
        "career": "Năm 2026 là năm thu hoạch. Tiền bạc sẽ đổ về nếu bạn làm việc trung thực và chăm chỉ.",
        "love": "Hãy học cách bỏ 'chiếc áo sếp' ở ngoài cửa. Gia đình cần sự ấm áp.",
        "month_tips": "T5: Vận tài lộc cực phát, hãy xem xét đầu tư dài hạn."
    },
    9: {
        "tag": "NGƯỜI NHÂN ÁI BAO DUNG", "icon": "❤️", "color": "#EF476F",
        "wave": [10, 30, 50, 70, 90, 100, 80, 60, 40, 20, 50, 100],
        "summary": "Số 9 đại diện cho sự hoàn tất, lý tưởng và lòng nhân ái.",
        "personality": "- **Ưu điểm:** Bao dung, lý tưởng sống cao đẹp, thích giúp đỡ cộng đồng.\n- **Nhược điểm:** Dễ mơ mộng quá mức, đôi khi thiếu thực tế trong tài chính.",
        "career": "Phù hợp các hoạt động cộng đồng, nhân đạo hoặc giáo dục tầm vóc lớn.",
        "love": "Tình yêu mang tính hy sinh và cống hiến. Hãy khép lại những tổn thương cũ.",
        "month_tips": "T12: Kết thúc một chu kỳ cũ để đón nhận vận may mới."
    }
}

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🔮 BẢN ĐỒ VẬN MỆNH CHI TIẾT 2026")

with st.sidebar:
    st.header("🔑 Thông Tin Tra Cứu")
    # Cài đặt giá trị mặc định cho ô nhập liệu
    input_name = st.text_input("Nhập Họ và Tên", value="Nguyễn Xuân Quần")
    input_dob = st.date_input(
        "Chọn Ngày Sinh", 
        value=datetime(1983, 1, 1), 
        min_value=datetime(1950, 1, 1),
        max_value=datetime(2026, 12, 31)
    )
    st.markdown("---")
    submitted = st.button("🚀 KHÁM PHÁ ĐỊNH MỆNH")

# Tự động tính toán dựa trên dữ liệu hiện có trong ô nhập
b_num, d_num = calculate_all(input_name, input_dob)
res = EXTENDED_DATA.get(b_num, EXTENDED_DATA[1])

# Dòng chào mừng hiện ra khi chưa bấm nút
if not submitted:
    st.markdown("<div class='welcome-text'>✨ Hệ thống đã sẵn sàng! Đây là kết quả xem nhanh. Hãy nhấn nút 'Khám Phá' để nhận hiệu ứng bất ngờ! ✨</div>", unsafe_allow_html=True)

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
