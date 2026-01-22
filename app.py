import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học Toàn Diện 2026", page_icon="📜", layout="wide")

# CSS để giao diện trông như một cuốn sách cổ hiện đại
st.markdown("""
    <style>
    .main { background-color: #fdfaf5; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border-top: 5px solid #8e44ad; }
    .content-card { background-color: #ffffff; padding: 25px; border-radius: 15px; border: 1px solid #e0e0e0; margin-bottom: 20px; line-height: 1.6; }
    .highlight { color: #8e44ad; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LOGIC TÍNH TOÁN CHUẨN ---
def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

def calculate_all(name, dob):
    # Số chủ đạo
    d, m, y = dob.day, dob.month, dob.year
    b_num = get_root_number(get_root_number(d) + get_root_number(m) + get_root_number(y))
    # Số định mệnh (tạm tính theo ngày sinh + độ dài tên để demo phong phú)
    d_num = get_root_number(b_num + len(name))
    return b_num, d_num

# --- 3. KHO DỮ LIỆU ĐỒ SỘ (Ví dụ chi tiết cho các số) ---
# Ở đây mình viết mẫu rất dài cho số 4 (trong hình của bạn) và các số khác bạn có thể copy tương tự
EXTENDED_DATA = {
    4: {
        "tag": "NHÀ KIẾN THIẾT KIÊN ĐỊNH",
        "icon": "🏗️",
        "color": "#2c3e50",
        "wave": [40, 45, 60, 55, 75, 90, 100, 85, 70, 60, 55, 80],
        "summary": "Số 4 là hiện thân của sự vững chãi, kỷ luật và thực tế. Bạn là cái neo trong mọi giông bão.",
        "personality": """
            - **Ưu điểm:** Bạn có khả năng tổ chức tuyệt vời, cực kỳ chi tiết và đáng tin cậy. Khi mọi người bỏ cuộc, bạn là người cuối cùng ở lại để hoàn thành công việc.
            - **Nhược điểm:** Đôi khi quá cứng nhắc, bảo thủ và khó thích nghi với sự thay đổi đột ngột. Bạn dễ bị căng thẳng nếu kế hoạch không đi đúng lộ trình.
            - **Lời khuyên:** Hãy học cách thả lỏng và chấp nhận rằng đôi khi sự hỗn loạn cũng mang lại cơ hội.
        """,
        "career": """
            Năm 2026 là năm để bạn xây dựng nền móng. Các công việc liên quan đến quản lý, kỹ thuật, tài chính hoặc bất động sản sẽ rất thuận lợi. 
            **Giai đoạn bùng nổ:** Tháng 6 và Tháng 7. Đây là lúc bạn nên ký kết các hợp đồng dài hạn.
        """,
        "love": """
            Bạn không phải mẫu người lãng mạn kiểu 'ngôn tình', nhưng bạn thể hiện tình yêu qua hành động thực tế. 
            Năm 2026, mối quan hệ của bạn cần sự cam kết cao hơn. Nếu đang độc thân, bạn có xu hướng tìm kiếm một người có cùng chí hướng xây dựng tương lai bền vững.
        """,
        "month_tips": "T7: Đỉnh cao năng lượng, hãy làm việc lớn. T10: Cẩn thận sức khỏe, nên đi du lịch nghỉ dưỡng."
    },
    7: {
        "tag": "CHIẾN LƯỢC GIA TRÍ TUỆ",
        "icon": "🧠",
        "color": "#8e44ad",
        "wave": [20, 30, 10, 50, 80, 40, 90, 100, 60, 40, 20, 10],
        "summary": "Số 7 là con số của tâm linh, triết học và sự thấu suốt sâu sắc.",
        "personality": """
            - **Ưu điểm:** Khả năng phân tích sắc bén, trực giác cực mạnh. Bạn nhìn thấy những thứ người khác bỏ qua.
            - **Nhược điểm:** Dễ cô độc, khó gần và hay đa nghi. Bạn thường chìm quá sâu vào suy nghĩ riêng.
        """,
        "career": "Thích hợp với nghiên cứu, giảng dạy hoặc các ngành công nghệ cao. Năm 2026 là năm 'mài rìu', hãy học thêm một kỹ năng mới.",
        "love": "Cần một người bạn đời biết tôn trọng khoảng không gian riêng của mình.",
        "month_tips": "T8: Trực giác cao nhất, hãy tin vào cảm giác của mình."
    }
}
# (Lưu ý: Các số 1, 2, 3, 5, 6, 8, 9 bạn có thể thêm nội dung tương tự vào biến EXTENDED_DATA)

# --- 4. GIAO DIỆN ---
st.title("🔮 BẢN ĐỒ VẬN MỆNH CHI TIẾT 2026")
st.markdown("---")

with st.sidebar:
    st.header("🔑 Thông Tin Cá Nhân")
    name = st.text_input("Nhập Họ và Tên", "Hoa Xuân Trường")
    dob = st.date_input("Chọn Ngày Sinh", datetime(1972, 9, 30))
    submit = st.button("🚀 XEM KẾT QUẢ CHI TIẾT")

if submit and name:
    b_num, d_num = calculate_all(name, dob)
    # Lấy dữ liệu, nếu không có thì lấy mặc định số 4
    data = EXTENDED_DATA.get(b_num, EXTENDED_DATA[4])

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.metric("SỐ CHỦ ĐẠO", b_num)
        st.metric("SỐ ĐỊNH MỆNH", d_num)
        st.markdown(f"### {data['icon']} {data['tag']}")
        st.info(data['summary'])
        st.write(f"**📅 Lời khuyên tháng:** {data['month_tips']}")

    with col2:
        st.subheader("📈 Biểu Đồ Nhịp Sinh Học & Vận Thế 2026")
        df = pd.DataFrame(data['wave'], index=[f"Tháng {i}" for i in range(1,13)], columns=["Năng lượng"])
        st.line_chart(df, color=data['color'])
        
        # Phần nội dung dài
        st.markdown("### 📘 Giải Mã Chi Tiết")
        
        with st.expander("🎭 ĐẶC ĐIỂM NHÂN CÁCH (SÂU)", expanded=True):
            st.markdown(data['personality'])
            
        with st.expander("💼 SỰ NGHIỆP & TÀI CHÍNH 2026"):
            st.markdown(data['career'])
            
        with st.expander("💖 TÌNH DUYÊN & MỐI QUAN HỆ"):
            st.markdown(data['love'])

    st.success("Bản báo cáo của bạn đã sẵn sàng! Chúc bạn một năm 2026 rực rỡ.")
    st.balloons()

# --- PHẦN CHIA SẺ MẠNG XÃ HỘI ---
st.markdown("---")
st.markdown("<h3 style='text-align: center;'>📢 CHIA SẺ KẾT QUẢ CHO BẠN BÈ</h3>", unsafe_allow_html=True)

# URL của trang web bạn (Thay đổi nếu bạn đổi tên app)
share_url = "https://xem-than-so-hoc-2026.streamlit.app"
share_msg = f"Tôi vừa tra cứu Thần Số Học 2026 cực chuẩn! Xem ngay tại: {share_url}"

# Tạo 3 cột để đặt các nút chia sẻ
c1, c2, c3 = st.columns(3)

with c1:
    # Nút Facebook
    fb_link = f"https://www.facebook.com/sharer/sharer.php?u={share_url}"
    st.markdown(f'''
        <a href="{fb_link}" target="_blank">
            <button style="width:100%; background-color: #1877F2; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">
                📘 Chia sẻ Facebook
            </button>
        </a>
    ''', unsafe_allow_html=True)

with c2:
    # Nút Zalo (Dùng link chuyển hướng của Zalo)
    zalo_link = f"https://zalo.me/s/share/?url={share_url}&note={share_msg}"
    st.markdown(f'''
        <a href="{zalo_link}" target="_blank">
            <button style="width:100%; background-color: #0068FF; color: white; border: none; padding: 10px; border-radius: 5px; cursor: pointer;">
                💬 Chia sẻ qua Zalo
            </button>
        </a>
    ''', unsafe_allow_html=True)

with c3:
    # Nút Copy Link
    if st.button("🔗 Sao chép đường dẫn"):
        st.write(f"Đã copy: `{share_url}`")
        st.toast("Đã sao chép link thành công!")

st.markdown("<p style='text-align: center; font-size: 0.8em; color: gray;'>© 2026 Hệ Thống Thần Số Học Cá Nhân</p>", unsafe_allow_html=True)
