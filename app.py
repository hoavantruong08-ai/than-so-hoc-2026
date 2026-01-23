import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import unicodedata
import urllib.parse

# =========================================================
# PHẦN 1: KHO THƯ VIỆN THAM CHIẾU (Dễ dàng sửa nội dung)
# =========================================================
THAM_CHIEU_SO_CHU_DAO = {
    1: {"danh_hieu": "NHÀ LÃNH ĐẠO ĐỘC LẬP", "luan_giai": "Năng lượng tiên phong, quyết đoán và khát khao khẳng định mình.", "loi_khuyen": "Hãy dẫn dắt bằng sự thấu hiểu trong năm 2026."},
    2: {"danh_hieu": "SỨ GIẢ HÒA BÌNH", "luan_giai": "Kết nối tâm hồn, nhạy cảm và tìm kiếm sự cân bằng.", "loi_khuyen": "Trực giác là vũ khí mạnh nhất của bạn."},
    3: {"danh_hieu": "NGƯỜI TRUYỀN CẢM HỨNG", "luan_giai": "Sáng tạo và ngôn từ là thế mạnh lan tỏa niềm vui.", "loi_khuyen": "Tập trung vào một mục tiêu cụ thể để bứt phá."},
    4: {"danh_hieu": "NGƯỜI XÂY DỰNG KỶ LUẬT", "luan_giai": "Hiện thân của sự vững chãi, thực tế và quy trình.", "loi_khuyen": "Hãy học cách linh hoạt trước những thay đổi."},
    5: {"danh_hieu": "NHÀ CẢI CÁCH TỰ DO", "luan_giai": "Yêu thích đổi mới, mạo hiểm và khám phá chân trời mới.", "loi_khuyen": "Tự do nhưng cần có điểm dừng kỷ luật."},
    6: {"danh_hieu": "NGƯỜI NUÔI DƯỠNG TẬN TÂM", "luan_giai": "Trái tim ấm áp, luôn che chở gia đình và cộng đồng.", "loi_khuyen": "Hãy chăm sóc bản thân trước khi lo cho người khác."},
    7: {"danh_hieu": "NGƯỜI TÌM KIẾM TRI THỨC", "luan_giai": "Chiêm nghiệm, phân tích sâu và học hỏi qua trải nghiệm.", "loi_khuyen": "Dành thời gian tĩnh lặng để thấu hiểu nội tâm."},
    8: {"danh_hieu": "NHÀ ĐIỀU HÀNH THÀNH CÔNG", "luan_giai": "Tư duy tài chính sắc bén và khả năng chịu áp lực lớn.", "loi_khuyen": "Sự kiên trì sẽ mang lại phần thưởng xứng đáng."},
    9: {"danh_hieu": "NGƯỜI NHÂN ÁI LÝ TƯỞNG", "luan_giai": "Sống vì hoài bão lớn, bao dung và hướng tới nhân loại.", "loi_khuyen": "Khép lại quá khứ để bắt đầu hành trình mới rực rỡ."},
    11: {"danh_hieu": "BẬC THẦY TRỰC GIÁC", "luan_giai": "Năng lượng tâm linh vượt trội và tầm nhìn xa.", "loi_khuyen": "Tin vào những thông điệp trực giác gửi đến."},
    22: {"danh_hieu": "NGƯỜI KIẾN TẠO VĨ ĐẠI", "luan_giai": "Biến ý tưởng khổng lồ thành hiện thực hữu hình.", "loi_khuyen": "Đừng ngại ước mơ lớn, bạn có đủ lực thực hiện."}
}

PYTHAGORAS_CHART = {
    'A':1,'J':1,'S':1, 'B':2,'K':2,'T':2, 'C':3,'L':3,'U':3, 'D':4,'M':4,'V':4, 
    'E':5,'N':5,'W':5, 'F':6,'O':6,'X':6, 'G':7,'P':7,'Y':7, 'H':8,'Q':8,'Z':8, 'I':9,'R':9
}

# =========================================================
# PHẦN 2: LOGIC HỆ THỐNG (Không cần sửa)
# =========================================================
def rut_gon_so(n, master=True):
    while n > 9:
        if master and n in [11, 22, 33]: return n
        n = sum(int(d) for d in str(n))
    return n

def tinh_so_ten(name):
    name = ''.join(c for c in unicodedata.normalize('NFD', name.upper()) if unicodedata.category(c) != 'Mn')
    return rut_gon_so(sum(PYTHAGORAS_CHART.get(c, 0) for c in name if c.isalpha()))

# =========================================================
# PHẦN 3: GIAO DIỆN VÀ BIỂU ĐỒ SINH HỌC
# =========================================================
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .report-card { background: white; padding: 25px; border-radius: 15px; border-left: 8px solid #6c5ce7; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .share-fb { background-color: #1877F2; color: white !important; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; text-decoration: none; display: block; }
    .share-zalo { background-color: #0068FF; color: white !important; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; text-decoration: none; display: block; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔮 TRA CỨU BIỂU ĐỒ THẦN SỐ HỌC 2026")

with st.sidebar:
    st.header("📋 THÔNG TIN")
    user_name = st.text_input("Họ và Tên đầy đủ")
    user_dob = st.date_input("Ngày tháng năm sinh", datetime(1995, 1, 1))
    user_phone = st.text_input("Số điện thoại")
    btn_scan = st.button("🚀 XEM BIỂU ĐỒ & KẾT QUẢ")

if btn_scan and user_name:
    # Tính toán chỉ số
    so_chu_dao = rut_gon_so(user_dob.day + user_dob.month + sum(int(d) for d in str(user_dob.year)))
    so_su_menh = tinh_so_ten(user_name)
    data_id = THAM_CHIEU_SO_CHU_DAO.get(so_chu_dao, THAM_CHIEU_SO_CHU_DAO[1])
    
    # Ghi dữ liệu Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_old = conn.read(ttl=0)
        new_row = pd.DataFrame([{"Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Họ Tên": user_name, "Ngày Sinh": user_dob.strftime("%d/%m/%Y"), "Số Chủ Đạo": str(so_chu_dao), "Số Sứ Mệnh": str(so_su_menh), "Số Điện Thoại": user_phone}])
        conn.update(data=pd.concat([df_old, new_row], ignore_index=True))
    except: pass

    # HIỂN THỊ KẾT QUẢ
    st.write("---")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.metric("SỐ CHỦ ĐẠO (Ngày sinh)", so_chu_dao)
    with col_m2:
        st.metric("SỐ SỨ MỆNH (Họ tên)", so_su_menh)

    st.markdown(f"""
    <div class="report-card">
        <h2 style="color:#6c5ce7;">✨ {data_id['danh_hieu']}</h2>
        <p style="font-size:1.2em;"><b>Luận giải:</b> {data_id['luan_giai']}</p>
        <p style="font-size:1.2em; color:#2d3436;"><b>Lời khuyên 2026:</b> {data_id['loi_khuyen']}</p>
    </div>
    """, unsafe_allow_html=True)

    # PHẦN BIỂU ĐỒ SINH HỌC (BIỂU ĐỒ NĂNG LƯỢNG)
    st.write("---")
    st.subheader("📊 BIỂU ĐỒ PHÂN TÍCH NĂNG LƯỢNG SINH HỌC")
    
    # Tạo dữ liệu giả lập dựa trên các chỉ số thần số học để vẽ biểu đồ
    # Đây là nơi thể hiện các khía cạnh năng lượng của khách hàng
    chart_data = pd.DataFrame({
        'Chỉ số Năng lượng': ['Trực giác', 'Lý trí', 'Sáng tạo', 'Thực thi', 'Cảm xúc'],
        'Mức độ (%)': [
            rut_gon_so(so_chu_dao * 7) * 10, 
            rut_gon_so(so_su_menh * 5) * 10, 
            rut_gon_so(so_chu_dao + so_su_menh) * 8,
            85, 
            90
        ]
    })
    st.bar_chart(chart_data, x='Chỉ số Năng lượng', y='Mức độ (%)')

    # NÚT CHIA SẺ
    st.write("---")
    msg = f"Tôi có Số Chủ Đạo là {so_chu_dao}. Tra cứu biểu đồ sinh học 2026 tại:"
    url_app = "https://than-so-hoc-2026.streamlit.app/" 
    
    s1, s2 = st.columns(2)
    s1.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u={url_app}&quote={urllib.parse.quote(msg)}" target="_blank" class="share-fb">Chia sẻ Facebook</a>', unsafe_allow_html=True)
    s2.markdown(f'<a href="https://zalo.me/s/share/?url={url_app}&note={urllib.parse.quote(msg)}" target="_blank" class="share-zalo">Chia sẻ Zalo</a>', unsafe_allow_html=True)
    
    st.balloons()
