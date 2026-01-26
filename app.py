import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình trang - Đặt ngay đầu tiên để tránh lỗi
st.set_page_config(page_title="Thần Số Học 2026", layout="wide")

# Hàm tính toán an toàn
def tinh_so_chu_dao(val):
    try:
        s = "".join(filter(str.isdigit, str(val)))
        if not s: return "N/A"
        total = sum(int(i) for i in s)
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        return str(total)
    except:
        return "Lỗi"

st.title("🔮 Hệ Thống Thần Số Học")

# Kiểm tra kết nối an toàn
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception as e:
    st.error("Chưa cấu hình Secrets hoặc lỗi kết nối Sheets.")
    st.stop() # Dừng app tại đây nếu lỗi kết nối để không bị văng

# Giao diện chính
tab1, tab2 = st.tabs(["📥 Nhập Liệu & Upload", "📊 Xem Dữ Liệu"])

with tab1:
    # Sidebar chỉ để đổi chế độ
    st.sidebar.title("Cài đặt")
    mode = st.sidebar.radio("Chọn hình thức:", ["Nhập tay", "Upload Excel/CSV"])

    if mode == "Nhập tay":
        with st.form("form_single"):
            name = st.text_input("Họ tên")
            phone = st.text_input("Số điện thoại")
            dob = st.date_input("Ngày sinh")
            if st.form_submit_button("Lưu dữ liệu"):
                if name and phone:
                    so = tinh_so_chu_dao(dob)
                    new_df = pd.DataFrame([{"Thời Gian": datetime.now().strftime("%d/%m/%Y"), "Họ Tên": name, "Ngày Sinh": dob.strftime("%d/%m/%Y"), "Số Chủ Đạo": so, "Số Điện Thoại": phone}])
                    old_df = conn.read(ttl=0).astype(str)
                    conn.update(data=pd.concat([old_df, new_df], ignore_index=True))
                    st.success("Đã lưu!")

    else:
        st.subheader("Tải file danh sách")
        f = st.file_uploader("Chọn file Excel (.xlsx) hoặc CSV", type=["xlsx", "csv"])
        if f:
            try:
                # Đọc file dựa trên đuôi
                df_up = pd.read_excel(f, engine='openpyxl') if f.name.endswith('xlsx') else pd.read_csv(f)
                st.write("Xem trước dữ liệu:", df_up.head(3))
                
                if st.button("Xác nhận Đẩy lên Sheets"):
                    # Tự động map cột hoặc báo lỗi nếu thiếu
                    if "Ngày Sinh" in df_up.columns:
                        df_up["Số Chủ Đạo"] = df_up["Ngày Sinh"].apply(tinh_so_chu_dao)
                        df_up["Thời Gian"] = datetime.now().strftime("%d/%m/%Y")
                        
                        existing = conn.read(ttl=0).astype(str)
                        updated = pd.concat([existing, df_up.astype(str)], ignore_index=True)
                        conn.update(data=updated)
                        st.success("Đã đồng bộ thành công!")
                    else:
                        st.error("File cần có cột tên là 'Ngày Sinh'")
            except Exception as e:
                st.error(f"Lỗi đọc file: {e}")

with tab2:
    if st.button("Làm mới danh sách"):
        st.cache_data.clear()
    try:
        data = conn.read(ttl=0)
        st.dataframe(data, use_container_width=True)
    except:
        st.write("Chưa có dữ liệu để hiển thị.")
