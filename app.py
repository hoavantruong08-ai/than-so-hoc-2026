import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Cấu hình trang
st.set_page_config(page_title="Thần Số Học 2026", layout="wide")

# 2. Kết nối Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Hàm tính Số Chủ Đạo
def tinh_so_chu_dao(ngay_sinh_val):
    if pd.isna(ngay_sinh_val): return ""
    # Chuyển đổi mọi định dạng ngày về chuỗi số sạch
    s = str(ngay_sinh_val).replace("/", "").replace("-", "").split()[0]
    digits = "".join(filter(str.isdigit, s))
    if not digits: return ""
    try:
        total = sum(int(i) for i in digits)
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        return str(total)
    except:
        return ""

# 4. Giao diện Sidebar
with st.sidebar:
    st.title("🔮 Quản Trị")
    mode = st.radio("Chọn phương thức nhập:", ["Nhập thủ công", "Upload File Excel"])

st.title("🔮 Hệ Thống Thần Số Học")

tab1, tab2 = st.tabs(["📥 Nhập Dữ Liệu", "📂 Kho Lưu Trữ"])

with tab1:
    if mode == "Nhập thủ công":
        with st.form("form_le"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Họ tên:")
            phone = col2.text_input("Số điện thoại:")
            dob = st.date_input("Ngày sinh:")
            
            if st.form_submit_button("Lưu lên hệ thống"):
                if name and phone:
                    so = tinh_so_chu_dao(dob)
                    new_row = pd.DataFrame([{
                        "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                        "Họ Tên": name,
                        "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                        "Số Chủ Đạo": so,
                        "Số Điện Thoại": phone
                    }])
                    df_old = conn.read(ttl=0).astype(str)
                    conn.update(data=pd.concat([df_old, new_row], ignore_index=True))
                    st.success(f"✅ Đã lưu: {name}")

    else:
        st.subheader("🚀 Tải lên danh sách từ Excel")
        up_file = st.file_uploader("Kéo thả file .xlsx vào đây", type=["xlsx"])
        
        if up_file:
            try:
                # Đọc file với engine openpyxl đã cài ở bước 1
                df_upload = pd.read_excel(up_file, engine='openpyxl')
                st.write("🔍 Xem trước dữ liệu từ file:")
                st.dataframe(df_upload.head(10), use_container_width=True)
                
                if st.button("🔥 Xác nhận đồng bộ lên Google Sheets"):
                    with st.spinner("Đang xử lý..."):
                        # Tự động tính Số Chủ Đạo nếu cột đó đang trống trong file
                        df_upload["Số Chủ Đạo"] = df_upload["Ngày Sinh"].apply(tinh_so_chu_dao)
                        if "Thời Gian" not in df_upload.columns:
                            df_upload["Thời Gian"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        
                        # Đọc data cũ và gộp lại
                        df_old = conn.read(ttl=0).astype(str)
                        # Đảm bảo định dạng string để tránh lỗi merge
                        df_upload = df_upload.astype(str)
                        updated_df = pd.concat([df_old, df_upload], ignore_index=True)
                        
                        conn.update(data=updated_df)
                        st.success(f"✅ Thành công! Đã tải lên {len(df_upload)} khách hàng.")
                        st.balloons()
            except Exception as e:
                st.error(f"❌ Lỗi xử lý file: {e}")

with tab2:
    if st.button("🔄 Làm mới danh sách"):
        st.cache_data.clear()
    data = conn.read(ttl=0)
    st.dataframe(data, use_container_width=True)
