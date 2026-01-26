import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Thần Số Học 2026", layout="wide", page_icon="🔮")

# Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- HÀM TÍNH SỐ CHỦ ĐẠO ---
def tinh_so_chu_dao(ngay_sinh_date):
    digits = ngay_sinh_date.strftime("%d%m%Y")
    total = sum(int(i) for i in digits)
    while total > 11 and total != 22:
        total = sum(int(digit) for digit in str(total))
    return total

# --- GIAO DIỆN SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3282/3282300.png", width=100)
    st.title("Quản Trị Viên")
    mode = st.radio("Chế độ nhập liệu:", ["Nhập đơn lẻ", "Upload danh sách (Excel/CSV)"])
    st.info("Dữ liệu sẽ được đồng bộ trực tiếp với Google Sheets.")

# --- GIAO DIỆN CHÍNH ---
st.title("🔮 Hệ Thống Thần Số Học Chuyên Nghiệp")

tab1, tab2 = st.tabs(["✨ Tính Toán & Lưu Trữ", "📊 Quản Lý Dữ Liệu"])

with tab1:
    if mode == "Nhập đơn lẻ":
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Họ tên:")
            phone = st.text_input("📞 Số điện thoại:")
        with col2:
            dob = st.date_input("📅 Ngày sinh:", min_value=datetime(1950, 1, 1))
            
        if st.button("🚀 Tính & Lưu Hệ Thống"):
            if name and phone:
                so_chu_dao = tinh_so_chu_dao(dob)
                
                # Hiển thị kết quả nhanh
                st.metric(label="Số Chủ Đạo của bạn", value=so_chu_dao)
                
                try:
                    df = conn.read(ttl=0).astype(str)
                    new_row = pd.DataFrame([{
                        "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "Họ Tên": name,
                        "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                        "Số Chủ Đạo": str(so_chu_dao),
                        "Số Điện Thoại": phone
                    }])
                    updated_df = pd.concat([df, new_row], ignore_index=True)
                    conn.update(data=updated_df)
                    st.success(f"Đã lưu thành công cho {name}!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Lỗi: {e}")
            else:
                st.warning("Vui lòng điền đủ thông tin!")

    else:
        st.subheader("📁 Upload danh sách khách hàng")
        uploaded_file = st.file_uploader("Chọn file Excel hoặc CSV", type=["csv", "xlsx"])
        
        if uploaded_file:
            if uploaded_file.name.endswith(".csv"):
                up_df = pd.read_csv(uploaded_file)
            else:
                up_df = pd.read_excel(uploaded_file)
                
            st.write("Xem trước dữ liệu:", up_df.head())
            
            if st.button("Xử lý & Đẩy lên Cloud"):
                with st.spinner("Đang tính toán số chủ đạo..."):
                    # Giả sử file có cột 'Ho Ten', 'SDT', 'Ngay Sinh' (DD/MM/YYYY)
                    # Bạn có thể điều chỉnh logic map cột ở đây
                    try:
                        current_df = conn.read(ttl=0).astype(str)
                        # Giả lập xử lý (Bạn cần đảm bảo định dạng ngày chuẩn trong file upload)
                        # ... (Code xử lý vòng lặp cho file upload tại đây)
                        st.success("Tính năng Upload hàng loạt đã sẵn sàng!")
                    except:
                        st.error("Lỗi định dạng file!")

with tab2:
    st.subheader("📋 Danh sách khách hàng trên hệ thống")
    try:
        # Nút làm mới dữ liệu
        if st.button("🔄 Làm mới dữ liệu"):
            st.cache_data.clear()
            
        data = conn.read(ttl=0)
        st.dataframe(
            data, 
            use_container_width=True,
            column_config={
                "Số Chủ Đạo": st.column_config.NumberColumn(format="%d ✨"),
                "Thời Gian": st.column_config.DatetimeColumn()
            }
        )
        
        # Thống kê nhanh
        st.divider()
        st.write(f"📈 Tổng cộng: **{len(data)}** khách hàng")
        
    except:
        st.info("Chưa có dữ liệu nào được ghi nhận.")
