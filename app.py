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
    7: {
        "icon": "🧠", "title": "SỐ 7: NGƯỜI CHIÊM NGHIỆM TRÍ TUỆ",
        "image": "https://img.freepik.com/free-vector/mystical-astrology-concept_23-2148530368.jpg",
        "energy_wave": [20, 30, 10, 50, 80, 40, 90, 100, 60, 40, 20, 10],
        "advice_2026": "Năm 2026 là năm để bạn 'mài rìu'. Hãy tập trung học tập và thiền định.",
        "nhan_cach": "Sâu sắc, thích một mình, trực giác cực cao.",
        "cong_viec": "Hợp với nghiên cứu, giảng dạy, kỹ thuật.",
        "tinh_duyen": "Cần sự riêng tư và thấu hiểu sâu sắc."
    },
    8: {
        "icon": "💰", "title": "SỐ 8: NHÀ ĐIỀU HÀNH CHIẾN LƯỢC",
        "image": "https://img.freepik.com/free-vector/golden-mandala-background-design_53876-120155.jpg",
        "energy_wave": [60, 70, 80, 90, 100, 80, 60, 50, 40, 30, 50, 80],
        "advice_2026": "Năm của gặt hái! Tài chính sẽ có bước tiến lớn nếu bạn kỷ luật.",
        "nhan_cach": "Mạnh mẽ, thực tế, có tham vọng lớn.",
        "cong_viec": "Lãnh đạo, tài chính, bất động sản.",
        "tinh_duyen": "Thích che chở, đôi khi hơi áp đặt."
    },
    9: {
        "icon": "❤️", "title": "SỐ 9: NGƯỜI TRUYỀN CẢM HỨNG",
        "image": "https://img.freepik.com/free-vector/spiritual-sacred-geometry-ornament_23-2148505504.jpg",
        "energy_wave": [10, 20, 40, 60, 80, 100, 90, 70, 50, 30, 20, 90],
        "advice_2026": "Hãy buông bỏ cái cũ. Năm của sự kết thúc tốt đẹp và nhân đạo.",
        "nhan_cach": "Bao dung, lý tưởng hóa, thích giúp người.",
        "cong_viec": "Công tác xã hội, y tế, nghệ thuật.",
        "tinh_duyen": "Yêu chân thành, coi trọng tình nghĩa."
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

