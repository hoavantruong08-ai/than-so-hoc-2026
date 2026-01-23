import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import unicodedata
import urllib.parse

# =========================================================
# PHẦN 1: CẤU HÌNH GIAO DIỆN & HÌNH ẢNH (BẢO TOÀN TRANG TRÍ)
# =========================================================
st.set_page_config(page_title="Thần Số Học Toàn Diện 2026", page_icon="🔮", layout="wide")

URL_ANH_BANNER = "https://img.freepik.com/free-vector/mystical-astrology-background-with-zodiac-signs_23-2148425501.jpg"
URL_ANH_THAY_BOI = "https://cdn-icons-png.flaticon.com/512/1491/1491204.png"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: #ffffff; }}
    .report-card {{
        background: white; color: #1c1e21; padding: 30px; border-radius: 20px;
        border-left: 10px solid #7d5fff; box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin-bottom: 25px;
    }}
    .stButton>button {{
        background: linear-gradient(45deg, #7d5fff, #b33771); color: white;
        border: none; padding: 12px; border-radius: 25px; font-weight: bold; width: 100%; transition: 0.3s;
    }}
    .stButton>button:hover {{ transform: scale(1.02); box-shadow: 0 5px 15px rgba(125, 95, 255, 0.4); }}
    .share-fb {{ background-color: #1877F2; color: white !important; padding: 10px; border-radius: 8px; text-align: center; display: block; text-decoration: none; font-weight: bold; }}
    .share-zalo {{ background-color: #0068FF; color: white !important; padding: 10px; border-radius: 8px; text-align: center; display: block; text-decoration: none; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# =========================================================
# PHẦN 2: THƯ VIỆN THAM CHIẾU (NỘI DUNG ĐẦY ĐỦ NHẤT)
# =========================================================
THU_VIEN_LUAN_GIAI = {
    1: {"tag": "NHÀ LÃNH ĐẠO ĐỘC LẬP", "desc": "Bạn mang năng lượng của người tiên phong, tự tin và có ý chí mạnh mẽ.", "advice": "Năm 2026 là lúc để bạn hiện thực hóa các ý tưởng cá nhân."},
    2: {"tag": "SỨ GIẢ HÒA BÌNH", "desc": "Bạn có khả năng kết nối, lắng nghe và thấu hiểu tuyệt vời.", "advice": "Hãy tin vào trực giác nhạy bén của bạn để đưa ra quyết định."},
    3: {"tag": "NGƯỜI TRUYỀN CẢM HỨNG", "desc": "Sáng tạo, vui vẻ và có khả năng ngôn ngữ bậc thầy.", "advice": "Năm nay hãy lan tỏa năng lượng tích cực đến cộng đồng nhiều hơn."},
    4: {"tag": "NGƯỜI XÂY DỰNG TẬN TỤY", "desc": "Bạn là người của kỷ luật, thực tế và vô cùng đáng tin cậy.", "advice": "Hãy xây dựng kế hoạch dài hạn, nền tảng sẽ vững chắc trong năm nay."},
    5: {"tag": "NHÀ THÁM HIỂM TỰ DO", "desc": "Yêu thích sự thay đổi, linh hoạt và luôn tràn đầy năng lượng thám hiểm.", "advice": "Cơ hội đi xa hoặc thay đổi công việc sẽ mở ra trong năm 2026."},
    6: {"tag": "NGƯỜI NUÔI DƯỠNG", "desc": "Trách nhiệm, giàu tình cảm và luôn hướng về gia đình.", "advice": "Dành thời gian chăm sóc tổ ấm, bạn sẽ tìm thấy bình an."},
    7: {"tag": "CHIẾN LƯỢC GIA TRI THỨC", "desc": "Sâu sắc, thích chiêm nghiệm và có tư duy triết học.", "advice": "Năm nay phù hợp để học tập chuyên sâu hoặc tu tập tâm linh."},
    8: {"tag": "NHÀ ĐIỀU HÀNH THÀNH CÔNG", "desc": "Mạnh mẽ, quyết liệt và có tài quản trị tài chính.", "advice": "Quả ngọt về tài chính đang chờ đợi nỗ lực của bạn."},
    9: {"tag": "NGƯỜI NHÂN ÁI LÝ TƯỞNG", "desc": "Giàu lòng trắc ẩn, sống vì cộng đồng và lý tưởng cao đẹp.", "advice": "Hãy học cách buông bỏ cái cũ để đón nhận những sứ mệnh mới."},
    11: {"tag": "BẬC THẦY TRỰC GIÁC", "desc": "Năng lượng tâm linh cực cao, có khả năng nhìn thấu tương lai.", "advice": "Hãy dùng tầm nhìn của mình để hướng dẫn mọi người."},
    22: {"tag": "NGƯỜI KIẾN TẠO VĨ ĐẠI", "desc": "Có khả năng biến những giấc mơ lớn nhất thành hiện thực.", "advice": "Đừng ngần ngại xây dựng những dự án tầm cỡ thế giới."}
}

PYTHAGORAS_CHART = {'A':1,'J':1,'S':1,'B':2,'K':2,'T':2,'C':3,'L':3,'U':3,'D':4,'M':4,'V':4,'E':5,'N':5,'W':5,'F':6,'O':6,'X':6,'G':7,'P':7,'Y':7,'H':8,'Q':8,'Z':8,'I':9,'R':9}

# =========================================================
# PHẦN 3: HỆ THỐNG XỬ LÝ (LOGIC)
# =========================================================
def rut_gon(n):
    while n > 9 and n not in [11, 22, 33]: n = sum(int(d) for d in str(n))
    return n

def tinh_ten(name):
    name = ''.join(c for c in unicodedata.normalize('NFD', name.upper()) if unicodedata.category(c) != 'Mn')
    total = sum(PYTHAGORAS_CHART.get(c, 0) for c in name if c.isalpha())
    return rut_gon(total)

# =========================================================
# PHẦN 4: HIỂN THỊ & CÔNG CỤ VI-RÚT (VIRAL)
# =========================================================
st.image(URL_ANH_BANNER, use_container_width=True)

with st.sidebar:
    st.image(URL_ANH_THAY_BOI, width=150)
    st.title("TRA CỨU MỆNH SỐ")
    name = st.text_input("Họ và Tên")
    dob = st.date_input("Ngày sinh", datetime(1995, 1, 1))
    phone = st.text_input("Số điện thoại")
    btn = st.button("🚀 KHÁM PHÁ VẬN MỆNH")

if btn and name:
    so_cd = rut_gon(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    so_sm = tinh_ten(name)
    res = THU_VIEN_LUAN_GIAI.get(so_cd, THU_VIEN_LUAN_GIAI[1])
    
    # 1. Lưu Google Sheets
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        new_row = pd.DataFrame([{"Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Họ Tên": name, "Ngày Sinh": dob.strftime("%d/%m/%Y"), "Số Chủ Đạo": str(so_cd), "Số Sứ Mệnh": str(so_sm), "Số Điện Thoại": phone}])
        conn.update(data=pd.concat([df, new_row], ignore_index=True))
    except: pass

    # 2. Hiển thị kết quả chính
    st.write("---")
    st.markdown(f"""
        <div class="report-card">
            <h1 style="color:#7d5fff; margin-bottom:5px;">Số Chủ Đạo của bạn: {so_cd}</h1>
            <h3 style="color:#b33771;">Sứ mệnh cuộc đời: {so_sm}</h3>
            <h2 style="margin-top:20px;">✨ {res['tag']}</h2>
            <p style="font-size:1.2em;"><b>Luận giải chi tiết:</b> {res['desc']}</p>
            <p style="font-size:1.2em; color:#d63031;"><b>Lời khuyên năm 2026:</b> {res['advice']}</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Biểu đồ sinh học
    st.subheader("📊 BIỂU ĐỒ TẦN SỐ NĂNG LƯỢNG")
    chart_data = pd.DataFrame({
        'Yếu tố': ['Năng lực nội tại', 'Khả năng biểu đạt', 'Trực giác tâm linh', 'Tính thực thi'],
        'Điểm': [so_cd*10 if so_cd < 11 else 100, so_sm*10, 85, 75]
    })
    st.bar_chart(chart_data, x='Yếu tố', y='Điểm')

    # 4. Công cụ chia sẻ
    st.write("---")
    st.subheader("📢 Chia sẻ để nhận thêm may mắn")
    u = "https://than-so-hoc-2026.streamlit.app/"
    m = urllib.parse.quote(f"Tôi mang năng lượng số {so_cd}. Khám phá vận mệnh 2026 tại đây!")
    c1, c2 = st.columns(2)
    c1.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u={u}&quote={m}" target="_blank" class="share-fb">Facebook</a>', unsafe_allow_html=True)
    c2.markdown(f'<a href="https://zalo.me/s/share/?url={u}&note={m}" target="_blank" class="share-zalo">Zalo</a>', unsafe_allow_html=True)
    st.balloons()
