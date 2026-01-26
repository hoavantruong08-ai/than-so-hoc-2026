import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Tra Cứu Thần Số Học", page_icon="🔮")

# Kết nối cùng database (Google Sheets) với App Admin
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🔍 Tra Cứu Kết Quả Thần Số Học")
st.write("Nhập thông tin của bạn bên dưới để xem kết quả")

# Phần tra cứu
with st.container():
    search_query = st.text_input("Nhập Số điện thoại của bạn:")
    btn_search = st.button("Tra cứu ngay")

if btn_search:
    if search_query:
        # Đọc dữ liệu từ Sheets
        df = conn.read(ttl=0)
        
        # Tìm kiếm khách hàng theo Số điện thoại
        # (Lưu ý: Chuyển cả hai về string để so sánh chính xác)
        result = df[df['Số Điện Thoại'].astype(str).str.contains(search_query)]
        
        if not result.empty:
            st.success(f"Chào bạn {result.iloc[0]['Họ Tên']}! Dưới đây là kết quả của bạn:")
            
            # Hiển thị kết quả đẹp mắt bằng Metric hoặc Card
            col1, col2 = st.columns(2)
            col1.metric("Số Chủ Đạo", result.iloc[0]['Số Chủ Đạo'])
            col2.write(f"**Ngày sinh:** {result.iloc[0]['Ngày Sinh']}")
            
            # Bạn có thể thêm các lời giải thích về con số ở đây
            st.info("💡 **Lời khuyên:** Hãy phát huy thế mạnh của con số này trong năm 2026!")
        else:
            st.error("Không tìm thấy thông tin. Vui lòng liên hệ Admin để được hỗ trợ.")
    else:
        st.warning("Vui lòng nhập số điện thoại để tra cứu.")

# Chặn khách hàng download/upload bằng cách không thêm st.file_uploader hay st.download_button
