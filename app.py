import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection
import unicodedata
import urllib.parse

# --- 1. CẤU HÌNH & GIAO DIỆN ---
st.set_page_config(page_title="Thần Số Học Pythagoras 2026", page_icon="🔮", layout="wide")

st.markdown("""
    <style>
    .report-card { background: white; padding: 20px; border-radius: 15px; border-left: 8px solid #6c5ce7; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .metric-box { text-align: center; padding: 10px; background: #f8f9fa; border-radius: 10px; }
    .share-btn-fb { background-color: #1877F2; color: white !important; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; text-decoration: none; display: block; }
    .share-btn-zalo { background-color: #0068FF; color: white !important; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; text-decoration: none; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DỮ LIỆU THUYẾT MINH CHUYÊN SÂU ---
INTERPRETATION = {
    1: {"tag": "NHÀ LÃNH ĐẠO ĐỘC LẬP", "desc": "Bạn mang năng lượng của người tiên phong, quyết đoán và có khao khát khẳng định bản thân mãnh liệt.", "advice": "Hãy tự tin dẫn dắt nhưng đừng quên lắng nghe cộng sự."},
    2: {"tag": "SỨ GIẢ HÒA BÌNH", "desc": "Bạn có khả năng kết nối tâm hồn, nhạy cảm và luôn tìm kiếm sự cân bằng trong các mối quan hệ.", "advice": "Trực giác là vũ khí mạnh nhất của bạn trong năm 2026."},
    3: {"tag": "NGƯỜI TRUYỀN CẢM HỨNG", "desc": "Sáng tạo và ngôn từ là thế mạnh. Bạn lan tỏa niềm vui và sự lạc quan đến mọi người xung quanh.", "advice": "Hãy tập trung năng lượng vào một mục tiêu cụ thể để bứt phá."},
    4: {"tag": "NGƯỜI XÂY DỰNG KỶ LUẬT", "desc": "Bạn là hiện thân của sự vững chãi, thực tế và làm việc có quy trình rõ ràng.", "advice": "Cần học cách linh hoạt hơn trước những thay đổi của thời đại."},
    5: {"tag": "NHÀ CẢI CÁCH TỰ DO", "desc": "Yêu thích sự đổi mới, không ngại mạo hiểm và luôn khao khát khám phá những chân trời mới.", "advice": "Hãy tận hưởng sự thay đổi nhưng đừng đánh mất mục tiêu cốt lõi."},
    6: {"tag": "NGƯỜI NUÔI DƯỠNG TẬN TÂM", "desc": "Mang trái tim ấm áp, bạn luôn sẵn lòng che chở và chăm sóc cho gia đình, cộng đồng.", "advice": "Đừng quên chăm sóc bản thân mình trước khi lo cho người khác."},
    7: {"tag": "NGƯỜI TÌM KIẾM TRI THỨC", "desc": "Bạn thích chiêm nghiệm, phân tích sâu và có khả năng tự học hỏi rất cao thông qua trải nghiệm.", "advice": "Năm nay là thời điểm vàng để bạn tu tập hoặc nghiên cứu chuyên sâu."},
    8: {"tag": "NHÀ ĐIỀU HÀNH THÀNH CÔNG", "desc": "Bạn có năng lực quản trị, tư duy tài chính sắc bén và khả năng chịu áp lực lớn.", "advice": "Sự kiên trì sẽ mang lại phần thưởng vật chất xứng đáng trong năm nay."},
    9: {"tag": "NGƯỜI NHÂN ÁI LÝ TƯỞNG", "desc": "Sống vì hoài bão lớn lao, giàu lòng trắc ẩn và luôn hướng tới những giá trị tốt đẹp cho nhân loại.", "advice": "Hãy học cách khép lại quá khứ để bắt đầu một chu kỳ mới rực rỡ."},
    11: {"tag": "BẬC THẦY TRỰC GIÁC", "desc": "Năng lượng tâm linh vượt trội, bạn có tầm nhìn xa và khả năng truyền cảm hứng tâm hồn.", "advice": "Hãy tin vào những thông điệp mà vũ trụ gửi đến cho bạn."},
    22: {"tag": "NGƯỜI KIẾN TẠO VĨ ĐẠI", "desc": "Bạn có khả năng biến những ý tưởng khổng lồ thành hiện thực thông qua kế hoạch chi tiết.", "advice": "Đừng ngần ngại ước mơ lớn, bạn có đủ lực để thực hiện nó."}
}

# --- 3. HỆ THỐNG TÍNH TOÁN ---
PYTHAGORAS_CHART = {
    'A':1,'J':1,'S':1, 'B':2,'K':2,'T':2, 'C':3,'L':3,'U':3, 'D':4,'M':4,'V':4, 'E':5,'N':5,'W':5, 'F':6,'O':6,'X':6, 'G':7,'P':7,'Y':7, 'H':8,'Q':8,'Z':8, 'I':9,'R':9
}

def reduce_num(n, master=True):
    while n > 9:
        if master and n in [11, 22, 33]: return n
        n = sum(int(d) for d in str(n))
    return n

def calc_name(name):
    name = ''.join(c for c in unicodedata.normalize('NFD', name.upper()) if unicodedata.category(c) != 'Mn')
    return reduce_num(sum(PYTHAGORAS_CHART.get(c, 0) for c in name if c.isalpha()))

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🔮 THẦN SỐ HỌC TOÀN DIỆN 2026")
st.markdown("#### Khám phá sự kết hợp giữa Ngày Sinh & Họ Tên theo bảng Pythagoras")

with st.sidebar:
    st.header("📋 NHẬP THÔNG TIN")
    user_name = st.text_input("Họ và Tên đầy đủ")
    user_dob = st.date_input("Ngày tháng năm sinh", datetime(1995, 1, 1))
    user_phone = st.text_input("Số điện thoại (để lưu kết quả)")
    btn_scan = st.button("🚀 LUẬN GIẢI NGAY")

if btn_scan and user_name:
    # Tính toán
    path_num = reduce_num(user_dob.day + user_dob.month + sum(int(d) for d in str(user_dob.year)))
    name_num = calc_name(user_name)
    info = INTERPRETATION.get(path_num, INTERPRETATION[1])
    
    # Lưu Sheet
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df_old = conn.read(ttl=0)
        new_row = pd.DataFrame([{"Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "Họ Tên": user_name, "Ngày Sinh": user_dob.strftime("%d/%m/%Y"), "Số Chủ Đạo": str(path_num), "Số Sứ Mệnh": str(name_num), "Số Điện Thoại": user_phone}])
        conn.update(data=pd.concat([df_old, new_row], ignore_index=True))
    except: pass

    # HIỂN THỊ KẾT QUẢ
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="metric-box"><h3>SỐ CHỦ ĐẠO</h3><h1 style="color:#6c5ce7;">{path_num}</h1><p>(Tính từ Ngày Sinh)</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><h3>SỐ SỨ MỆNH</h3><h1 style="color:#00b894;">{name_num}</h1><p>(Tính từ Họ Tên)</p></div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="report-card">
        <h2 style="color:#6c5ce7;">✨ {info['tag']}</h2>
        <p style="font-size:1.1em;"><b>Luận giải:</b> {info['desc']}</p>
        <p style="font-size:1.1em; color:#2d3436;"><b>Lời khuyên 2026:</b> {info['advice']}</p>
    </div>
    """, unsafe_allow_html=True)

    # CHIA SẺ
    st.subheader("📢 Chia sẻ vận mệnh của bạn")
    msg = f"Tôi là số {path_num} - {info['tag']}. Tra cứu ngay tại:"
    encoded_msg = urllib.parse.quote(msg)
    url = "https://than-so-hoc-2026.streamlit.app/" # LINK APP CỦA BẠN
    
    s1, s2 = st.columns(2)
    s1.markdown(f'<a href="https://www.facebook.com/sharer/sharer.php?u={url}&quote={encoded_msg}" target="_blank" class="share-btn-fb">Chia sẻ Facebook</a>', unsafe_allow_html=True)
    s2.markdown(f'<a href="https://zalo.me/s/share/?url={url}&note={encoded_msg}" target="_blank" class="share-btn-zalo">Chia sẻ Zalo</a>', unsafe_allow_html=True)

    # BIỂU ĐỒ
    st.write("---")
    st.subheader("📊 BIỂU ĐỒ NĂNG LƯỢNG")
    st.bar_chart(pd.DataFrame({'Chỉ số': ['Nội tại', 'Biểu đạt', 'Trực giác', 'Hành động'], 'Điểm': [path_num*10, name_num*10, 85, 75]}), x='Chỉ số', y='Điểm')
    st.balloons()
