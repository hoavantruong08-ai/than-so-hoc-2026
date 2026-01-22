import streamlit as st
import unicodedata
import pandas as pd
import numpy as np
from datetime import datetime

# --- CẤU HÌNH TRANG CHUYÊN NGHIỆP ---
st.set_page_config(page_title="Thần Số Học Pro 2026", page_icon="🔮", layout="wide")

# Tùy chỉnh CSS để giao diện đẹp hơn
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_name=True)

# --- DỮ LIỆU NÂNG CẤP VỚI ICON & HÌNH ẢNH ---
DATA_DETAILED = {
    7: {
        "icon": "🧠",
        "title": "SỐ 7: NGƯỜI CHIÊM NGHIỆM TRÍ TUỆ",
        "image": "https://img.freepik.com/free-vector/mystical-astrology-concept_23-2148530368.jpg",
        "energy_wave": [20, 30, 10, 50, 80, 40, 90, 100, 60, 40, 20, 10],
        "advice_2026": "Năm 2026 là năm để bạn 'mài rìu'. Đừng vội vã hành động. Hãy tập trung học tập và thiền định.",
        "nhan_cach": "Sâu sắc, thích một mình, trực giác cực cao. Bạn không tin vào vẻ bề ngoài mà luôn tìm kiếm bản chất.",
        "cong_viec": "Hợp với nghiên cứu, giảng dạy, kỹ thuật hoặc nghệ thuật tự do.",
        "tinh_duyen": "Cần sự riêng tư. Hợp với những người có chiều sâu tâm hồn tương đương."
    },
    8: {
        "icon": "💰",
        "title": "SỐ 8: NHÀ ĐIỀU HÀNH CHIẾN LƯỢC",
        "image": "https://img.freepik.com/free-vector/golden-mandala-background-design_53876-120155.jpg",
        "energy_wave": [60, 70, 80, 90, 100, 80, 60, 50, 40, 30, 50, 80],
        "advice_2026": "Năm của gặt hái! Tài chính sẽ có bước tiến lớn nếu bạn giữ được sự kỷ luật.",
        "nhan_cach": "Mạnh mẽ, thực tế, có tham vọng lớn và khả năng tổ chức tuyệt vời.",
        "cong_viec": "Lãnh đạo doanh nghiệp, tài chính, bất động sản hoặc chính trị.",
        "tinh_duyen": "Thích sự che chở, đôi khi hơi áp đặt đối phương."
    },
    9: {
        "icon": "❤️",
        "title": "SỐ 9: NGƯỜI TRUYỀN CẢM HỨNG",
        "image": "https://img.freepik.com/free-vector/spiritual-sacred-geometry-ornament_23-2148505504.jpg",
        "energy_wave": [10, 20, 40, 60, 80, 100, 90, 70, 50, 30, 20, 90],
        "advice_2026": "Hãy buông bỏ những gì không còn phục vụ bạn. Năm của sự kết thúc tốt đẹp và nhân đạo.",
        "nhan_cach": "Bao dung, lý tưởng hóa, luôn muốn giúp đỡ người khác.",
        "cong_viec": "Công tác xã hội, y tế, nghệ thuật hoặc các tổ chức phi lợi nhuận.",
        "tinh_duyen": "Yêu chân thành, coi trọng tình nghĩa hơn vật chất."
    }
}

# --- HÀM TÍNH TOÁN ---
def calculate_numbers(name, dob):
    # Tính số chủ đạo (Birth Number)
    b_sum = dob.day + dob.month + sum(int(d) for d in str(dob.year))
    while b_sum > 9 and b_sum not in [11, 22, 33]:
        b_sum = sum(int(d) for d in str(b_sum))
    
    # Tính số tên gọi (Name Number - Rút gọn cho ví dụ)
    # Ở đây lấy tạm số 7, 8 hoặc 9 để demo dữ liệu chuyên nghiệp
    n_num = (len(name) % 3) + 7 
    return b_sum, n_num

# --- GIAO DIỆN CHÍNH ---
st.title("🔮 DASHBOARD THẦN SỐ HỌC CHUYÊN SÂU 2026")
st.markdown("---")

# Cấu hình Sidebar
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913501.png", width=100)
    st.header("📍 Hồ Sơ Cá Nhân")
    name = st.text_input("Họ và Tên", placeholder="Lê Thị Mỹ")
    dob = st.date_input("Ngày tháng năm sinh", min_value=datetime(1950, 1, 1))
    submit = st.button("🚀 KHÁM PHÁ ĐỊNH MỆNH")

if submit and name:
    b_num, n_num = calculate_numbers(name, dob)
    data = DATA_DETAILED.get(n_num, DATA_DETAILED[7]) # Mặc định lấy số 7 nếu chưa có data số khác

    # --- BỐ CỤC 2 CỘT (COLUMNS) ---
    col1, col2 = st.columns([1, 1.8], gap="large")

    with col1:
        st.subheader("📌 Chỉ Số Cốt Lõi")
        c1, c2 = st.columns(2)
        c1.metric("Số Chủ Đạo", b_num)
        c2.metric("Số Định Mệnh", n_num)
        
        st.image(data["image"], use_container_width=True, caption=f"Biểu tượng năng lượng số {n_num}")
        
        st.success(f"**Thông điệp chủ chốt:**\n\n{data['advice_2026']}")

    with col2:
        st.subheader(f"{data['icon']} {data['title']}")
        
        # --- BIỂU ĐỒ HÌNH SIN NHỊP SINH HỌC ---
        st.markdown("**📈 Biểu đồ năng lượng & Nhịp sinh học năm 2026**")
        months = ["Th1", "Th2", "Th3", "Th4", "Th5", "Th6", "Th7", "Th8", "Th9", "Th10", "Th11", "Th12"]
        chart_data = pd.DataFrame(data["energy_wave"], index=months, columns=["Mức năng lượng"])
        st.line_chart(chart_data)
        st.caption("Chú thích: Điểm cao nhất là thời điểm bùng nổ, điểm thấp nhất nên dành để nghỉ ngơi.")

        # --- CẤU TRÚC EXPANDER ---
        st.markdown("---")
        with st.expander("👤 CHI TIẾT NHÂN CÁCH & TÂM HỒN", expanded=True):
            st.write(data["nhan_cach"])
            
        with st.expander("💼 ĐỊNH HƯỚNG SỰ NGHIỆP & CÔNG VIỆC"):
            st.write(data["cong_viec"])
            
        with st.expander("❤️ DỰ BÁO TÌNH DUYÊN & MỐI QUAN HỆ"):
            st.write(data["tinh_duyen"])

    st.toast("Đã tải xong dữ liệu định mệnh của bạn!", icon="✅")

else:
    st.info("👋 Chào mừng bạn! Hãy nhập thông tin bên trái để mở khóa bản đồ cuộc đời năm 2026.")
    # Hình ảnh trang trí khi chưa nhập liệu
    st.image("https://img.freepik.com/free-photo/zen-stones-calm-water_53876-121285.jpg", use_container_width=True)
