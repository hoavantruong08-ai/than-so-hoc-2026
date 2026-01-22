import streamlit as st
import unicodedata
from fpdf import FPDF
from datetime import datetime

# --- CẤU HÌNH GIAO DIỆN RỘNG ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# --- 1. CƠ SỞ DỮ LIỆU NỘI DUNG 1: VẬN HẠN 2026 ---
DATA_2026 = {
    1: "Năm 2026: Sân chơi của sự khởi đầu mới. Hãy mạnh dạn triển khai dự án cá nhân. May mắn: Tháng 2, 6, 9.",
    2: "Năm 2026: Sức mạnh nằm ở sự kết nối và đối tác. Tình duyên thăng hoa. May mắn: Tháng 3, 7, 11.",
    3: "Năm 2026: Thời điểm tỏa sáng sáng tạo. Hãy thử thách ở lĩnh vực mới. May mắn: Tháng 5, 8, 12.",
    4: "Năm 2026: Năm của kỷ luật và tài chính ổn định. Lập kế hoạch dài hạn. May mắn: Tháng 1, 4, 10.",
    5: "Năm 2026: Thôi thúc thay đổi và tự do. Những chuyến đi mang lại vận may. May mắn: Tháng 3, 6, 9.",
    6: "Năm 2026: Hướng về gia đình, hàn gắn rạn nứt tình cảm. May mắn: Tháng 2, 7, 12.",
    7: "Năm 2026: Dành thời gian chiêm nghiệm, học hỏi chuyên sâu kiến thức. May mắn: Tháng 4, 8, 11.",
    8: "Năm 2026: Năm của thịnh vượng và tiền bạc. Nỗ lực được đền đáp xứng đáng. May mắn: Tháng 1, 5, 10.",
    9: "Năm 2026: Khép lại cái cũ, chuẩn bị cho sự tái sinh tốt đẹp hơn. May mắn: Tháng 9, 12."
}

# --- 2. CƠ SỞ DỮ LIỆU NỘI DUNG 2: ĐỐI CHIẾU TRỌN ĐỜI ---
DATA_TRON_DOI = {
    1: "Số 1: Hùng mạnh, độc lập, lãnh đạo. Lập trường vững chắc, ít thay đổi. Thích thám sát, mạo hiểm.",
    2: "Số 2: Hòa nhã, ngọt ngào, khéo léo. Sẵn sàng giúp đỡ, xã giao tốt nhưng dễ bị chi phối bởi tình cảm.",
    7: "Số 7: Trí tuệ, thâm trầm, thích kín đáo và cô quạnh. Có tiêu chuẩn rất cao và tín ngưỡng sâu sắc.",
    8: "Số 8: Quyền lực, thành công và kỷ luật sắt đá. Có sức hút nhân cách lớn và tài chính xuất sắc.",
    9: "Số 9: Nhân ái, lý tưởng, tình thương vô bờ bến. Sống vì đại nghĩa và giúp đỡ nhân loại."
} # Bạn có thể thêm đầy đủ từ 1-9 vào đây

# --- HÀM TÍNH TOÁN ---
def calculate_all(name, date_obj):
    def red(n, master=True):
        while n > 9:
            if master and n in [11, 22, 33]: break
            n = sum(int(d) for d in str(n))
        return n
    b_num = red(date_obj.day + date_obj.month + sum(int(d) for d in str(date_obj.year)))
    clean_n = "".join(c for c in unicodedata.normalize('NFKD', name) if not unicodedata.combining(c)).upper()
    map_p = {'A':1,'J':1,'S':1,'B':2,'K':2,'T':2,'C':3,'L':3,'U':3,'D':4,'M':4,'V':4,'E':5,'N':5,'W':5,'F':6,'O':6,'X':6,'G':7,'P':7,'Y':7,'H':8,'Q':8,'Z':8,'I':9,'R':9}
    n_num = red(sum(map_p.get(c, 0) for c in clean_n if c.isalpha()), False)
    return b_num, n_num

# --- GIAO DIỆN WEB ---
st.title("🔮 Hệ Thống Tra Cứu Thần Số Học")

with st.sidebar:
    st.header("📍 Nhập Thông Tin")
    name_input = st.text_input("Họ và Tên", placeholder="Ví dụ: Lê Thị Mỹ")
    date_input = st.date_input("Ngày sinh", min_value=datetime(1950, 1, 1))
    btn = st.button("🌟 TRA CỨU NGAY", use_container_width=True)

if btn and name_input:
    b, n = calculate_all(name_input, date_input)
    st.success(f"### KẾT QUẢ CHO: {name_input.upper()}")

    # NỘI DUNG 1 HIỆN Ở TRÊN
    st.subheader("📅 NỘI DUNG 1: VẬN HẠN NĂM 2026")
    st.info(f"**Con số chủ đạo của năm 2026: {b}**\n\n{DATA_2026.get(b, 'Đang cập nhật...')}")

    st.markdown("---")

    # NỘI DUNG 2 HIỆN Ở DƯỚI
    st.subheader("📜 NỘI DUNG 2: ĐỐI CHIẾU TRỌN ĐỜI")
    st.warning(f"**Con số định mệnh (Tên gọi): {n}**\n\n{DATA_TRON_DOI.get(n, 'Đang cập nhật...')}")
    
    # Nút PDF
    st.divider()
    st.write("Bạn có thể tải kết quả này về máy:")
    st.button("📥 Tải Báo Cáo PDF (Tính năng đang cấu hình)")
else:
    st.info("Vui lòng điền thông tin bên trái và nhấn nút để xem kết quả chi tiết.")