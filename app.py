import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Thần Số Học Pro 2026", page_icon="🔮", layout="wide")

# --- PHONG CÁCH GIAO DIỆN (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    .report-card { background: white; padding: 25px; border-radius: 20px; border-top: 5px solid #6c5ce7; margin-bottom: 20px; }
    h1 { color: #2d3436; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- DỮ LIỆU CHUYÊN SÂU ---
DATA = {
    1: {"tag": "NHÀ LÃNH ĐẠO ĐỘC LẬP", "desc": "Bạn sinh ra để dẫn dắt. Cá tính mạnh mẽ, kiên định và có khả năng tự lập cao.", "advice": "Năm 2026 là năm để bạn bắt đầu những dự án cá nhân mới."},
    2: {"tag": "SỨ GIẢ HÒA BÌNH", "desc": "Sức mạnh của bạn nằm ở sự lắng nghe, thấu hiểu và kết nối mọi người.", "advice": "Hãy tin vào trực giác của mình hơn trong năm nay."},
    3: {"tag": "NGƯỜI TRUYỀN CẢM HỨNG", "desc": "Sáng tạo, vui vẻ và đầy năng lượng. Bạn là linh hồn của mọi cuộc vui.", "advice": "Tập trung vào các kỹ năng giao tiếp và nghệ thuật."},
    4: {"tag": "NGƯỜI XÂY DỰNG TẬN TỤY", "desc": "Kỷ luật, thực tế và cực kỳ đáng tin cậy. Bạn là nền móng của mọi tổ chức.", "advice": "Cần chú ý hơn đến sức khỏe và sự cân bằng cuộc sống."},
    5: {"tag": "NHÀ THÁM HIỂM TỰ DO", "desc": "Thích thay đổi, ưa mạo hiểm và không ngại thử thách mới.", "advice": "Năm 2026 mang đến nhiều cơ hội đi xa và mở rộng tầm nhìn."},
    6: {"icon": "❤️", "tag": "NGƯỜI NUÔI DƯỠNG", "desc": "Trách nhiệm, yêu thương và luôn hướng về gia đình.", "advice": "Dành thời gian chăm sóc tổ ấm và các mối quan hệ cốt lõi."},
    7: {"tag": "CHIẾN LƯỢC GIA TÂM LINH", "desc": "Thích chiêm nghiệm, nghiên cứu sâu và có thế giới nội tâm phong phú.", "advice": "Đây là năm học hỏi và nâng cao kiến thức chuyên môn."},
    8: {"tag": "NHÀ ĐIỀU HÀNH TÀI BA", "desc": "Quyền lực, tài chính và sự điều hành là thế mạnh của bạn.", "advice": "Cơ hội thăng tiến và gia tăng tài sản đang chờ đợi bạn."},
    9: {"tag": "NGƯỜI NHÂN ÁI LÝ TƯỞNG", "desc": "Sống vì cộng đồng, bao dung và đầy lòng nhân ái.", "advice": "Hãy học cách buông bỏ những điều cũ để đón nhận cái mới."},
    11: {"tag": "BẬC THẦY TRỰC GIÁC", "desc": "Năng lượng tâm linh cực cao, có khả năng nhìn thấu sự việc.", "advice": "Hãy chia sẻ tầm nhìn của bạn để giúp đỡ người khác."},
    22: {"tag": "BẬC THẦY KIẾN TẠO", "desc": "Biến những giấc mơ viển vông nhất thành hiện thực hữu hình.", "advice": "Đừng ngại những kế hoạch lớn, bạn có đủ lực để làm."}
}

# --- HÀM TÍNH TOÁN ---
def get_root_number(n):
    while n > 9 and n not in [11, 22, 33]:
        n = sum(int(d) for d in str(n))
    return n

# --- GIAO DIỆN CHÍNH ---
st.title("🔮 HỆ THỐNG TRA CỨU MỆNH SỐ 2026")

with st.expander("📝 NHẬP THÔNG TIN TRA CỨU", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Họ và Tên")
    with col2:
        dob = st.date_input("Ngày sinh", datetime(1995, 1, 1))
    with col3:
        phone = st.text_input("Số Điện Thoại")
    
    submit = st.button("🚀 XEM LUẬN GIẢI CHI TIẾT")

if submit and name:
    # 1. Tính toán
    b_num = get_root_number(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    res = DATA.get(b_num, DATA[1])
    
    # 2. Lưu Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_old = conn.read(ttl=0)
        new_row = pd.DataFrame([{
            "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "Họ Tên": name,
            "Ngày Sinh": dob.strftime("%d/%m/%Y"),
            "Số Chủ Đạo": str(b_num),
            "Số Điện Thoại": phone if phone else "N/A"
        }])
        df_updated = pd.concat([df_old, new_row], ignore_index=True)
        conn.update(data=df_updated)
        st.toast("✅ Đã lưu dữ liệu khách hàng!")
    except:
        st.toast("⚠️ Kết nối Sheet đang bảo trì, vẫn hiển thị kết quả!")

    # 3. Hiển thị báo cáo Pro
    st.divider()
    
    # Khu vực Metric
    m1, m2, m3 = st.columns(3)
    m1.metric("CON SỐ CHỦ ĐẠO", b_num)
    m2.metric("NĂM THẾ GIỚI", "2026 (Số 1)")
    m3.metric("NĂNG LƯỢNG", f"{b_num * 10}%")

    # Khu vực Luận giải
    st.markdown(f"""
    <div class="report-card">
        <h2 style='color: #6c5ce7;'>✨ {res['tag']}</h2>
        <p style='font-size: 1.2em;'><b>Bản chất:</b> {res['desc']}</p>
        <p style='color: #2d3436;'><b>Lời khuyên năm 2026:</b> {res['advice']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Khu vực Biểu đồ
    st.subheader("📊 PHÂN TÍCH CHỈ SỐ NĂNG LƯỢNG")
    chart_data = pd.DataFrame({
        'Chỉ số': ['Trực giác', 'Lãnh đạo', 'Sáng tạo', 'Thực thi', 'Cảm xúc'],
        'Điểm': [b_num*8 if b_num < 10 else 95, 100-b_num*3, b_num*9 if b_num < 5 else 70, 85, 90]
    })
    st.bar_chart(chart_data, x='Chỉ số', y='Điểm')
    
    st.balloons()
elif submit and not name:
    st.error("Vui lòng nhập tên để hệ thống làm việc!")
