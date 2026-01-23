import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import unicodedata
import urllib.parse

# =========================================================
# PHẦN 1: THƯ VIỆN HÌNH ẢNH (IMAGE ASSETS)
# Quản lý toàn bộ ảnh của App tại đây
# =========================================================
ASSETS = {
    "BANNER_MAIN": "https://img.freepik.com/free-vector/mystical-astrology-background-with-zodiac-signs_23-2148425501.jpg",
    "ICON_THAY_BOI": "https://cdn-icons-png.flaticon.com/512/1491/1491204.png",
    "ICON_SUCCESS": "https://cdn-icons-png.flaticon.com/512/190/190411.png",
    "BG_CARD": "https://www.transparenttextures.com/patterns/cubes.png" # Ảnh nền vân nhẹ cho thẻ
}

# =========================================================
# PHẦN 2: THƯ VIỆN LUẬN GIẢI (CONTENT LIBRARY)
# Nâng cấp nội dung cho 11 con số tại đây
# =========================================================
CONTENT = {
    1: {"tag": "NHÀ LÃNH ĐẠO ĐỘC LẬP", "desc": "Năng lượng tiên phong, mạnh mẽ và đầy khát vọng dẫn đầu.", "advice": "Năm 2026, hãy tự tin khởi xướng những ý tưởng mới."},
    2: {"tag": "SỨ GIẢ HÒA BÌNH", "desc": "Bạn có khả năng kết nối, lắng nghe và thấu hiểu tuyệt vời.", "advice": "Hãy tin vào trực giác nhạy bén của bạn."},
    3: {"tag": "NGƯỜI TRUYỀN CẢM HỨNG", "desc": "Sáng tạo, vui vẻ và có khả năng ngôn ngữ bậc thầy.", "advice": "Hãy lan tỏa năng lượng tích cực đến cộng đồng."},
    4: {"tag": "NGƯỜI XÂY DỰNG TẬN TỤY", "desc": "Kỷ luật, thực tế và vô cùng đáng tin cậy.", "advice": "Xây dựng kế hoạch dài hạn, nền tảng sẽ vững chắc."},
    5: {"tag": "NHÀ THÁM HIỂM TỰ DO", "desc": "Yêu thích sự thay đổi, linh hoạt và năng lượng thám hiểm.", "advice": "Cơ hội thay đổi đột phá sẽ mở ra trong năm nay."},
    6: {"tag": "NGƯỜI NUÔI DƯỠNG", "desc": "Trách nhiệm, giàu tình cảm và luôn hướng về gia đình.", "advice": "Dành thời gian chăm sóc tổ ấm để tìm thấy bình an."},
    7: {"tag": "CHIẾN LƯỢC GIA TRI THỨC", "desc": "Sâu sắc, thích chiêm nghiệm và tư duy triết học.", "advice": "Phù hợp để học tập chuyên sâu hoặc tu tập tâm linh."},
    8: {"tag": "NHÀ ĐIỀU HÀNH THÀNH CÔNG", "desc": "Mạnh mẽ, quyết liệt và tài quản trị tài chính.", "advice": "Quả ngọt về tài chính đang chờ đợi nỗ lực của bạn."},
    9: {"tag": "NGƯỜI NHÂN ÁI LÝ TƯỞNG", "desc": "Giàu lòng trắc ẩn, sống vì cộng đồng.", "advice": "Buông bỏ cái cũ để đón nhận sứ mệnh mới."},
    11: {"tag": "BẬC THẦY TRỰC GIÁC", "desc": "Năng lượng tâm linh cực cao, nhìn thấu tương lai.", "advice": "Hãy dùng tầm nhìn của mình để hướng dẫn mọi người."},
    22: {"tag": "NGƯỜI KIẾN TẠO VĨ ĐẠI", "desc": "Biến giấc mơ lớn nhất thành hiện thực hữu hình.", "advice": "Đừng ngần ngại xây dựng dự án tầm cỡ."}
}

# =========================================================
# PHẦN 3: LOGIC HỆ THỐNG (BẢO TOÀN CÔNG VIỆC CŨ)
# =========================================================
st.set_page_config(page_title="Thần Số Học Pro 2026", page_icon="🔮", layout="wide")

# CSS Chuyên nghiệp
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0e1117; color: white; }}
    .report-card {{
        background: white; color: #1c1e21; padding: 30px; border-radius: 20px;
        border-left: 10px solid #7d5fff; box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        background-image: url("{ASSETS['BG_CARD']}");
    }}
    .stButton>button {{
        background: linear-gradient(45deg, #7d5fff, #b33771); color: white;
        border: none; padding: 12px; border-radius: 25px; font-weight: bold; width: 100%;
    }}
    .share-fb {{ background-color: #1877F2; color: white !important; padding: 10px; border-radius: 8px; text-align: center; display: block; text-decoration: none; font-weight: bold; }}
    .share-zalo {{ background-color: #0068FF; color: white !important; padding: 10px; border-radius: 8px; text-align: center; display: block; text-decoration: none; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

def rut_gon(n):
    while n > 9 and n not in [11, 22, 33]: n = sum(int(d) for d in str(n))
    return n

def tinh_ten(name):
    chart = {'A':1,'J':1,'S':1,'B':2,'K':2,'T':2,'C':3,'L':3,'U':3,'D':4,'M':4,'V':4,'E':5,'N':5,'W':5,'F':6,'O':6,'X':6,'G':7,'P':7,'Y':7,'H':8,'Q':8,'Z':8,'I':9,'R':9}
    name = ''.join(c for c in unicodedata.normalize('NFD', name.upper()) if unicodedata.category(c) != 'Mn')
    return rut_gon(sum(chart.get(c, 0) for c in name if c.isalpha()))

# =========================================================
# PHẦN 4: HIỂN THỊ (GIAO DIỆN CHỐT)
# =========================================================
st.image(ASSETS["BANNER_MAIN"], use_container_width=True)

with st.sidebar:
    st.image(ASSETS["ICON_THAY_BOI"], width=120)
    st.header("📋 NHẬP THÔNG TIN")
    name = st.text_input("Họ và Tên")
    dob = st.date_input("Ngày sinh", datetime(1995, 1, 1))
    phone = st.text_input("Số điện thoại")
    btn = st.button("🚀 GIẢI MÃ VẬN MỆNH")

if btn and name:
    # 1. Tính toán & Ghi Sheet (Bảo toàn công việc cũ)
    so_cd = rut_gon(dob.day + dob.month + sum(int(d) for d in str(dob.year)))
    so_sm = tinh_ten(name)
    res = CONTENT.get(so_cd, CONTENT[1])
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(ttl=0)
        new_row = pd.DataFrame([{"Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Họ Tên": name, "Ngày Sinh": dob.strftime("%d/%m/%Y"), "Số Chủ Đạo": str(so_cd), "Số Sứ Mệnh": str(so_sm), "Số Điện Thoại": phone}])
        conn.update(data=pd.concat([df, new_row], ignore_index=True))
    except: pass

    # 2. Hiển thị Card Kết quả
    st.write("---")
    st.markdown(f"""
        <div class="report-card">
            <h1 style="color:#7d5fff; margin:0;">Số Chủ Đạo: {so_cd}</h1>
            <h3 style="color:#b33771; margin-bottom:20px;">Số Sứ Mệnh: {so_sm}</h3>
            <hr>
            <h2 style="margin-top:20px;">✨ {res['tag']}</h2>
            <p style="font-size:1.2em;"><b>Luận giải:</b> {res['desc']}</p>
            <p style="font-size:1.2em; color:#d63031;"><b>Lời khuyên năm 2026:</b> {res['advice']}</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Biểu đồ sinh học
    st.subheader("📊 BIỂU ĐỒ NĂNG LƯỢNG")
    st.bar_chart(pd.DataFrame({'Yếu tố': ['Nội tại', 'Biểu đạt', 'Trực giác', 'Hành động'], 'Điểm': [so_cd*10 if so_cd < 11 else 100, so_sm*10, 85, 75]}), x='Yếu tố', y='Điểm')

    # 4. Chia sẻ
    st.write("---")
    u = "https://than-so-hoc-2026.streamlit.app/"
    m = urllib.parse.quote(f"Số Chủ Đạo của tôi là {so_cd}. Tra cứu tại:")
    c1, c2 = st.columns(2)
    c1.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u={u}&quote={m}" target="_blank" class="share-fb">Facebook</a>', unsafe_allow_html=True)
    c2.markdown(f'<a href="https://zalo.me/s/share/?url={u}&note={m}" target="_blank" class="share-zalo">Zalo</a>', unsafe_allow_html=True)
    st.balloons()
