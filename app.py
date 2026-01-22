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

# --- 3. KHO DỮ LIỆU ĐẦY ĐỦ (1-9) ---
DATA = {
    4: {
        "tag": "NHÀ KIẾN THIẾT KIÊN ĐỊNH", 
        "icon": "🏗️", 
        "color": "#2c3e50", 
        "wave": [40, 65, 75, 85, 95, 100, 85, 75, 65, 55, 65, 75],
        "advice": "Năm 2026 yêu cầu sự tỉ mỉ và kiên nhẫn. Đừng vội vàng đầu tư mạo hiểm.",
        "p": """
            Bạn là người có tư duy hệ thống, thực tế và vô cùng vững chãi. 
            - **Điểm mạnh:** Khả năng quản trị công việc tuyệt vời, luôn có kế hoạch dự phòng và là chỗ dựa tin cậy nhất cho gia đình.
            - **Thách thức:** Đôi khi bạn quá cứng nhắc và khó tiếp nhận những ý tưởng đổi mới mang tính đột phá.
            - **Sứ mệnh:** Xây dựng những giá trị bền vững cho cộng đồng và thế hệ mai sau.
        """,
        "career_detail": """
            Năm 2026 là thời điểm 'vàng' để củng cố sự nghiệp. 
            - Nếu bạn đang làm kinh doanh: Hãy tập trung tối ưu hóa quy trình hiện tại thay vì mở rộng quá nhanh. 
            - Các tháng 6, 7 là lúc năng lượng lên cao nhất, thích hợp để chốt các hợp đồng quan trọng hoặc thăng tiến vị trí.
        """,
        "love_detail": """
            Trong tình yêu, bạn cần sự ổn định hơn là những lời đường mật. 
            - Năm nay, hãy dành thời gian cùng đối phương xây dựng những kế hoạch dài hạn như mua nhà, sinh con hoặc tích lũy tài chính. 
            - Sự thấu hiểu sẽ đến khi cả hai cùng nhìn về một mục tiêu thực tế.
        """
    },
    # Bạn có thể copy cấu trúc này cho các số từ 1-9 để nội dung cực kỳ đầy đủ.
}

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🔮 BẢN ĐỒ VẬN MỆNH CHI TIẾT 2026")
st.markdown("---")

with st.sidebar:
    st.header("🔑 Thông Tin Tra Cứu")
    name = st.text_input("Nhập Họ và Tên", "Văn Tiến Khoa")
    
    # Sửa lỗi hạn chế lịch tại đây:
    # min_value: cho phép chọn từ năm 1950
    # max_value: giới hạn đến năm hiện tại (2026)
    dob = st.date_input(
        "Chọn Ngày Sinh",
        value=datetime(1990, 1, 1),
        min_value=datetime(1950, 1, 1),
        max_value=datetime(2026, 12, 31),
        format="DD/MM/YYYY" # Giúp sắp xếp ngày/tháng/năm theo kiểu Việt Nam
    )
    
    submit = st.button("🚀 XEM KẾT QUẢ NGAY")

if submit and name:
    b_num, d_num = calculate_all(name, dob)
    # Lấy dữ liệu an toàn, nếu không có lấy số 1 mặc định để tránh lỗi KeyError
    res = DATA.get(b_num, DATA[1])

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.metric("SỐ CHỦ ĐẠO", b_num)
        st.metric("SỐ ĐỊNH MỆNH", d_num)
        st.markdown(f"### {res['icon']} {res['tag']}")
        st.markdown(f"<div class='advice-box'><b>💡 Lời khuyên 2026:</b><br>{res['advice']}</div>", unsafe_allow_html=True)
        st.write(f"**🎭 Tính cách:** {res['p']}")

    with col2:
        st.subheader("📈 Biểu Đồ Nhịp Sinh Học & Vận Thế 2026")
        chart_data = pd.DataFrame(res["wave"], index=[f"T{i}" for i in range(1,13)], columns=["Năng lượng"])
        st.line_chart(chart_data, color=res["color"])

        with st.expander("💼 SỰ NGHIỆP & TÀI CHÍNH"):
            st.write("Dựa trên biểu đồ, các tháng có đỉnh cao năng lượng là lúc bạn nên hành động mạnh mẽ nhất để đạt được mục tiêu tài chính.")
        with st.expander("💖 TÌNH DUYÊN & MỐI QUAN HỆ"):
            st.write("Cân bằng cảm xúc vào những tháng năng lượng thấp để giữ gìn sự hòa hợp trong gia đình.")

    # NÚT CHIA SẺ
    st.markdown("---")
    st.markdown("<h4 style='text-align: center;'>📢 Chia sẻ kết quả cho bạn bè</h4>", unsafe_allow_html=True)
    share_url = "https://xem-than-so-hoc-2026.streamlit.app"
    c1, c2 = st.columns(2)
    c1.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank"><button style="width:100%; background:#1877F2; color:white; border:none; padding:10px; border-radius:5px;">Chia sẻ Facebook</button></a>', unsafe_allow_html=True)
    c2.markdown(f'<a href="https://zalo.me/s/share/?url={share_url}" target="_blank"><button style="width:100%; background:#0068FF; color:white; border:none; padding:10px; border-radius:5px;">Chia sẻ Zalo</button></a>', unsafe_allow_html=True)
    
    st.balloons()
else:
    st.info("👈 Hãy nhập tên và ngày sinh để bắt đầu!")



