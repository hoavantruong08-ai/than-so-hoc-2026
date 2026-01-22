import streamlit as st
import unicodedata
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học Pro 2026", page_icon="🔮", layout="wide")

# Tùy chỉnh CSS để giao diện đẹp hơn
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU NÂNG CẤP ---
DATA_DETAILED = {
    1: {
        "icon": "🥇", "title": "SỐ 1: NHÀ LÃNH ĐẠO TIÊN PHONG",
        "image": "https://img.freepik.com/free-vector/abstract-golden-crown-design_53876-120155.jpg",
        "energy_wave": [80, 90, 100, 70, 50, 40, 60, 80, 90, 100, 80, 70],
        "advice_2026": "Năm của những khởi đầu mới táo bạo. Hãy tự tin dẫn dắt!",
        "nhan_cach": "Độc lập, quyết đoán, có ý chí sắt đá và khao khát khẳng định mình.",
        "cong_viec": "Lãnh đạo, khởi nghiệp, quản lý hoặc chuyên gia độc lập.",
        "tinh_duyen": "Mạnh mẽ, đôi khi hơi áp đặt, cần học cách lắng nghe bạn đời."
    },
    2: {
        "icon": "🤝", "title": "SỐ 2: NGƯỜI KẾT NỐI HÒA BÌNH",
        "image": "https://img.freepik.com/free-vector/spiritual-sacred-geometry-ornament_23-2148505504.jpg",
        "energy_wave": [40, 50, 60, 80, 90, 100, 80, 60, 40, 30, 50, 70],
        "advice_2026": "Năm của sự hợp tác. Thành công đến từ việc lắng nghe và hòa giải.",
        "nhan_cach": "Nhạy cảm, nhẹ nhàng, giàu lòng trắc ẩn và rất tinh tế.",
        "cong_viec": "Ngoại giao, tư vấn tâm lý, trợ lý hoặc hoạt động nghệ thuật.",
        "tinh_duyen": "Sâu sắc, chung thủy, luôn hy sinh cho hạnh phúc gia đình."
    },
    3: {
        "icon": "🎭", "title": "SỐ 3: BẬC THẦY TRUYỀN THÔNG",
        "image": "https://img.freepik.com/free-vector/mystical-astrology-concept_23-2148530368.jpg",
        "energy_wave": [60, 80, 90, 100, 70, 60, 80, 90, 100, 70, 50, 90],
        "advice_2026": "Năm để tỏa sáng! Hãy chia sẻ ý tưởng của bạn với cả thế giới.",
        "nhan_cach": "Vui vẻ, sáng tạo, có năng khiếu ngôn ngữ và thu hút đám đông.",
        "cong_viec": "Diễn giả, nhà văn, marketing, giải trí hoặc giảng dạy.",
        "tinh_duyen": "Thú vị, nhiều màu sắc nhưng cần học cách kiểm soát cảm xúc."
    },
    4: {
        "icon": "🏗️", "title": "SỐ 4: NGƯỜI XÂY DỰNG NỀN TẢNG",
        "image": "https://img.freepik.com/free-photo/zen-stones-calm-water_53876-121285.jpg",
        "energy_wave": [50, 40, 60, 70, 80, 90, 100, 80, 60, 50, 40, 60],
        "advice_2026": "Năm của sự ổn định và kỷ luật. Hãy tập trung vào những giá trị cốt lõi.",
        "nhan_cach": "Thực tế, vững chãi, coi trọng truyền thống và sự chi tiết.",
        "cong_viec": "Kỹ thuật, xây dựng, kế toán, pháp luật hoặc quản trị hệ thống.",
        "tinh_duyen": "Rất đáng tin cậy, là trụ cột vững chắc của gia đình."
    },
    5: {
        "icon": "✈️", "title": "SỐ 5: NHÀ THÁM HIỂM TỰ DO",
        "image": "https://img.freepik.com/free-vector/abstract-dynamic-shape-background_53876-120155.jpg",
        "energy_wave": [70, 90, 100, 80, 60, 70, 90, 100, 80, 60, 70, 100],
        "advice_2026": "Năm của những thay đổi bất ngờ. Hãy sẵn sàng trải nghiệm điều mới!",
        "nhan_cach": "Thích tự do, linh hoạt, ham học hỏi và ghét sự gò bó.",
        "cong_viec": "Du lịch, bán hàng, truyền thông hoặc các công việc hay di chuyển.",
        "tinh_duyen": "Nồng nhiệt, thích sự mới mẻ, cần đối tác hiểu rõ sự tự do của mình."
    },
    6: {
        "icon": "🏡", "title": "SỐ 6: NGƯỜI NUÔI DƯỠNG TÌNH YÊU",
        "image": "https://img.freepik.com/free-vector/mother-nature-concept-illustration_23-2148530368.jpg",
        "energy_wave": [30, 50, 70, 90, 100, 80, 70, 60, 80, 90, 100, 40],
        "advice_2026": "Năm của mái ấm và trách nhiệm. Hãy dành thời gian chăm sóc người thân.",
        "nhan_cach": "Giàu tình thương, trách nhiệm, thích chăm sóc và làm đẹp cho đời.",
        "cong_viec": "Y tế, giáo dục, trang trí nội thất hoặc tư vấn cộng đồng.",
        "tinh_duyen": "Ấm áp, coi trọng tổ ấm, là người yêu lý tưởng bậc nhất."
    },
    7: {
        "icon": "🧠", "title": "SỐ 7: NGƯỜI CHIÊM NGHIỆM TRÍ TUỆ",
        "image": "https://img.freepik.com/free-vector/mystical-astrology-concept_23-2148530368.jpg",
        "energy_wave": [20, 30, 10, 50, 80, 40, 90, 100, 60, 40, 20, 10],
        "advice_2026": "Năm để bạn 'mài rìu'. Hãy tập trung học tập và thiền định.",
        "nhan_cach": "Sâu sắc, thích một mình, trực giác cực cao.",
        "cong_viec": "Nghiên cứu, giảng dạy, kỹ thuật hoặc chuyên gia tư vấn.",
        "tinh_duyen": "Cần sự riêng tư và thấu hiểu sâu sắc từ đối phương."
    },
    8: {
        "icon": "💰", "title": "SỐ 8: NHÀ ĐIỀU HÀNH CHIẾN LƯỢC",
        "image": "https://img.freepik.com/free-vector/golden-mandala-background-design_53876-120155.jpg",
        "energy_wave": [60, 70, 80, 90, 100, 80, 60, 50, 40, 30, 50, 80],
        "advice_2026": "Năm của gặt hái! Tài chính sẽ có bước tiến lớn nếu bạn kỷ luật.",
        "nhan_cach": "Mạnh mẽ, thực tế, có tham vọng lớn và bản lĩnh lãnh đạo.",
        "cong_viec": "Kinh doanh, tài chính, bất động sản hoặc chính trị.",
        "tinh_duyen": "Thích che chở, đôi khi hơi áp đặt do bản tính lãnh đạo."
    },
    9: {
        "icon": "❤️", "title": "SỐ 9: NGƯỜI TRUYỀN CẢM HỨNG",
        "image": "https://img.freepik.com/free-vector/spiritual-sacred-geometry-ornament_23-2148505504.jpg",
        "energy_wave": [10, 20, 40, 60, 80, 100, 90, 70, 50, 30, 20, 90],
        "advice_2026": "Hãy buông bỏ cái cũ để đón nhận cái mới. Năm của sự nhân đạo.",
        "nhan_cach": "Bao dung, lý tưởng hóa, sống vì cộng đồng.",
        "cong_viec": "Công tác xã hội, y tế, nghệ thuật hoặc từ thiện.",
        "tinh_duyen": "Yêu chân thành, coi trọng tình nghĩa và tâm hồn."
    }
}
def calculate_numbers(name, dob):
    b_sum = dob.day + dob.month + sum(int(d) for d in str(dob.year))
    while b_sum > 9 and b_sum not in [11, 22, 33]:
        b_sum = sum(int(d) for d in str(b_sum))
    n_num = (len(name) % 3) + 7 
    return b_sum, n_num

# --- GIAO DIỆN CHÍNH ---
st.title("🔮 DASHBOARD THẦN SỐ HỌC CHUYÊN SÂU 2026")

with st.sidebar:
    st.header("📍 Hồ Sơ Cá Nhân")
    name_input = st.text_input("Họ và Tên", placeholder="Ví dụ: Lưu Xuân Quảng")
    date_input = st.date_input("Ngày sinh", min_value=datetime(1950, 1, 1))
    btn = st.button("🚀 KHÁM PHÁ ĐỊNH MỆNH")

if btn and name_input:
    b, n = calculate_numbers(name_input, date_input)
    res = DATA_DETAILED.get(n, DATA_DETAILED[7])

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.subheader("📌 Chỉ Số Cốt Lõi")
        m1, m2 = st.columns(2)
        m1.metric("Số Chủ Đạo", b)
        m2.metric("Số Định Mệnh", n)
        st.image(res["image"], use_container_width=True)
        st.success(f"**Lời khuyên 2026:** {res['advice_2026']}")

    with col2:
        st.subheader(f"{res['icon']} {res['title']}")
        st.write("**📈 Biểu đồ năng lượng & Nhịp sinh học 2026**")
        chart_data = pd.DataFrame(res["energy_wave"], 
                                 index=[f"T{i}" for i in range(1,13)], 
                                 columns=["Năng lượng"])
        st.line_chart(chart_data)

        with st.expander("👤 CHI TIẾT NHÂN CÁCH", expanded=True):
            st.write(res["nhan_cach"])
        with st.expander("💼 ĐỊNH HƯỚNG SỰ NGHIỆP"):
            st.write(res["cong_viec"])
        with st.expander("❤️ DỰ BÁO TÌNH DUYÊN"):
            st.write(res["tinh_duyen"])
else:
    st.info("👋 Nhập thông tin bên trái để xem kết quả chuyên nghiệp!")


