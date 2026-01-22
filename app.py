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
    1: {"tag": "NHÀ TIÊN PHONG", "icon": "🥇", "color": "#FFD700", "wave": [80, 95, 70, 90, 60, 50, 85, 100, 75, 90, 80, 95], "advice": "Năm 2026 là lúc bạn bứt phá. Hãy can đảm dẫn đầu các dự án mới!", "p": "Quyết đoán, độc lập và đầy khát vọng. Bạn sinh ra để làm chủ vận mệnh."},
    2: {"tag": "NGƯỜI KẾT NỐI", "icon": "🤝", "color": "#00CECB", "wave": [40, 60, 80, 100, 85, 65, 45, 55, 75, 95, 85, 65], "advice": "Hợp tác là chìa khóa. Hãy lắng nghe trực giác và xây dựng niềm tin.", "p": "Nhẹ nhàng, thấu cảm và giỏi giao tiếp. Bạn là chất keo gắn kết mọi người."},
    3: {"tag": "BẬC THẦY TRUYỀN CẢM HỨNG", "icon": "🎭", "color": "#FF5E5B", "wave": [70, 90, 100, 85, 65, 85, 95, 75, 100, 85, 65, 95], "advice": "Hãy chia sẻ ý tưởng của bạn. Nghệ thuật và ngôn từ sẽ mang lại vận may.", "p": "Vui vẻ, sáng tạo và đầy năng lượng. Bạn tỏa sáng nhất khi được thể hiện mình."},
    4: {"tag": "NGƯỜI XÂY DỰNG", "icon": "🏗️", "color": "#2c3e50", "wave": [50, 65, 75, 85, 95, 100, 85, 75, 65, 55, 65, 75], "advice": "Kỷ luật và thực tế. Đây là năm củng cố nền tảng tài chính bền vững.", "p": "Vững chãi, chi tiết và cực kỳ đáng tin cậy. Bạn là trụ cột của gia đình."},
    5: {"tag": "NHÀ THÁM HIỂM", "icon": "✈️", "color": "#FFAD05", "wave": [85, 75, 100, 85, 95, 100, 75, 65, 95, 85, 100, 95], "advice": "Sẵn sàng cho những chuyến đi và thay đổi bất ngờ. Vận may nằm ở sự tự do.", "p": "Linh hoạt, ham học hỏi và ghét sự gò bó. Bạn luôn tìm thấy cơ hội trong biến động."},
    6: {"tag": "NGƯỜI NUÔI DƯỠNG", "icon": "🏡", "color": "#7FB069", "wave": [35, 55, 75, 95, 100, 85, 65, 55, 85, 95, 100, 55], "advice": "Gia đình là ưu tiên số 1. Hãy chăm sóc bản thân và những người thân yêu.", "p": "Ấm áp, trách nhiệm và giàu tình thương. Bạn mang lại sự bình yên cho mọi người."},
    7: {"tag": "BẬC THẦY TRÍ TUỆ", "icon": "🧠", "color": "#6C5CE7", "wave": [25, 45, 35, 65, 85, 55, 95, 100, 75, 45, 35, 25], "advice": "Dành thời gian học tập và thiền định. Trí tuệ của bạn sẽ tăng trưởng mạnh.", "p": "Sâu sắc, nội tâm và có trực giác cực mạnh. Bạn nhìn thấu mọi sự việc."},
    8: {"tag": "NHÀ ĐIỀU HÀNH", "icon": "💰", "color": "#D4AF37", "wave": [65, 85, 95, 100, 85, 75, 65, 55, 45, 65, 85, 100], "advice": "Năm của gặt hái tài chính. Hãy giữ sự công bằng trong mọi quyết định.", "p": "Mạnh mẽ, tham vọng và giỏi quản trị. Bạn có tố chất của một nhà lãnh đạo tài ba."},
    9: {"tag": "NGƯỜI NHÂN ÁI", "icon": "❤️", "color": "#EF476F", "wave": [15, 35, 55, 75, 95, 100, 85, 65, 45, 25, 55, 100], "advice": "Khép lại quá khứ, hướng tới cộng đồng. Cho đi là nhận lại nhiều hơn.", "p": "Bao dung, lý tưởng và sống vì người khác. Bạn là người truyền lửa nhân văn."}
}

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🔮 BẢN ĐỒ VẬN MỆNH CHI TIẾT 2026")
st.markdown("---")

with st.sidebar:
    st.header("🔑 Thông Tin Tra Cứu")
    name = st.text_input("Nhập Họ và Tên", "Hoa Xuân Trường")
    dob = st.date_input("Chọn Ngày Sinh", datetime(1972, 9, 30))
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
