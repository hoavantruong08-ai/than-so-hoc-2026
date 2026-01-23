import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import unicodedata
import urllib.parse

# =========================================================
# PHẦN 1: CẤU HÌNH HÌNH ẢNH (BẠN THAY LINK ẢNH TẠI ĐÂY)
# =========================================================
# Bạn có thể thay link trong dấu ngoặc kép bằng link ảnh của bạn
URL_ANH_BANNER = "https://img.freepik.com/free-vector/mystical-astrology-background-with-zodiac-signs_23-2148425501.jpg"
URL_ANH_THAY_BOI = "https://cdn-icons-png.flaticon.com/512/3591/3591242.png" 

# =========================================================
# PHẦN 2: KHO THƯ VIỆN THAM CHIẾU (Dễ dàng sửa nội dung)
# =========================================================
THAM_CHIEU_SO_CHU_DAO = {
    1: {"danh_hieu": "NHÀ LÃNH ĐẠO ĐỘC LẬP", "luan_giai": "Năng lượng tiên phong, quyết đoán và khát khao khẳng định mình.", "loi_khuyen": "Hãy dẫn dắt bằng sự thấu hiểu trong năm 2026."},
    2: {"danh_hieu": "SỨ GIẢ HÒA BÌNH", "luan_giai": "Kết nối tâm hồn, nhạy cảm và tìm kiếm sự cân bằng.", "loi_khuyen": "Trực giác là vũ khí mạnh nhất của bạn."},
    # ... (Các số khác bạn giữ nguyên như bản trước)
}

PYTHAGORAS_CHART = {
    'A':1,'J':1,'S':1, 'B':2,'K':2,'T':2, 'C':3,'L':3,'U':3, 'D':4,'M':4,'V':4, 
    'E':5,'N':5,'W':5, 'F':6,'O':6,'X':6, 'G':7,'P':7,'Y':7, 'H':8,'Q':8,'Z':8, 'I':9,'R':9
}

# =========================================================
# PHẦN 3: LOGIC HỆ THỐNG
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
# PHẦN 4: GIAO DIỆN VÀ TRANG TRÍ
# =========================================================
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# CSS trang trí
st.markdown("""
    <style>
    .report-card { background: white; padding: 25px; border-radius: 15px; border-left: 8px solid #6c5ce7; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .share-fb { background-color: #1877F2; color: white !important; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; text-decoration: none; display: block; }
    .share-zalo { background-color: #0068FF; color: white !important; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; text-decoration: none; display: block; }
    [data-testid="stSidebar"] { background-image: linear-gradient(#2e1a47, #1a1a2e); color: white; }
    </style>
    """, unsafe_allow_html=True)

# 1. Ảnh Banner đầu trang
st.image(URL_ANH_BANNER, use_container_width=True)

st.title("🔮 KHÁM PHÁ BẢN ĐỒ VẬN MỆNH 2026")

with st.sidebar:
    # 2. Ảnh Ông thầy bói ở Sidebar
    st.image(URL_ANH_THAY_BOI, width=150)
    st.header("📋 THÔNG TIN")
    user_name = st.text_input("Họ và Tên đầy đủ")
    user_dob = st.date_input("Ngày tháng năm sinh", datetime(1995, 1, 1))
    user_phone = st.text_input("Số điện thoại")
    btn_scan = st.button("🚀 XEM BIỂU ĐỒ & KẾT QUẢ")

if btn_scan and user_name:
    so_chu_dao = rut_gon_so(user_dob.day + user_dob.month + sum(int(d) for d in str(user_dob.year)))
    so_su_menh = tinh_so_ten(user_name)
    data_id = THAM_CHIEU_SO_CHU_DAO.get(so_chu_dao, {"danh_hieu": "ĐANG CẬP NHẬT", "luan_giai": "...", "loi_khuyen": "..."})
    
    # Ghi dữ liệu Sheets
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
        st.metric("SỐ CHỦ ĐẠO", so_chu_dao)
    with col_m2:
        st.metric("SỐ SỨ MỆNH", so_su_menh)

    st.markdown(f"""
    <div class="report-card">
        <h2 style="color:#6c5ce7;">✨ {data_id['danh_hieu']}</h2>
        <p style="font-size:1.2em;"><b>Luận giải:</b> {data_id['luan_giai']}</p>
        <p style="font-size:1.2em; color:#2d3436;"><b>Lời khuyên 2026:</b> {data_id['loi_khuyen']}</p>
    </div>
    """, unsafe_allow_html=True)

    # BIỂU ĐỒ
    st.subheader("📊 BIỂU ĐỒ NĂNG LƯỢNG SINH HỌC")
    chart_data = pd.DataFrame({
        'Yếu tố': ['Trực giác', 'Lý trí', 'Sáng tạo', 'Thực thi', 'Cảm xúc'],
        'Điểm': [so_chu_dao*9, so_su_menh*8, 75, 85, 90]
    })
    st.bar_chart(chart_data, x='Yếu tố', y='Điểm')

    # CHIA SẺ
    st.write("---")
    url_app = "https://than-so-hoc-2026.streamlit.app/" 
    s1, s2 = st.columns(2)
    s1.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u={url_app}" target="_blank" class="share-fb">Facebook</a>', unsafe_allow_html=True)
    s2.markdown(f'<a href="https://zalo.me/s/share/?url={url_app}" target="_blank" class="share-zalo">Zalo</a>', unsafe_allow_html=True)
    st.balloons()
