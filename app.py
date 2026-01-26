import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Thần Số Học 2026", layout="wide", page_icon="🔮")

conn = st.connection("gsheets", type=GSheetsConnection)

def tinh_so_chu_dao(ngay_sinh_val):
    if pd.isna(ngay_sinh_val): return ""
    # Chuyển mọi định dạng về chuỗi số
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

st.title("🔮 Hệ Thống Thần Số Học")

# Sidebar quản lý
with st.sidebar:
    st.header("Menu Quản Trị")
    mode = st.radio("Chọn hình thức:", ["Nhập đơn lẻ", "Upload file Excel/CSV"])
    st.divider()
    st.info("Lưu ý: File upload nên có các cột: Họ Tên, Ngày Sinh, Số Điện Thoại.")

tab1, tab2 = st.tabs(["📥 Nhập Dữ Liệu", "📂 Kho Dữ Liệu Sheets"])

with tab1:
    if mode == "Nhập đơn lẻ":
        with st.form("form_nhap"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Họ tên:")
            phone = col2.text_input("Số điện thoại:")
            dob = st.date_input("Ngày sinh:")
            if st.form_submit_button("Lưu hệ thống"):
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
                    st.success(f"Đã lưu khách hàng {name}!")
    
    else:
        st.subheader("🚀 Upload file danh sách")
        up_file = st.file_uploader("Kéo thả file Excel (.xlsx) hoặc CSV vào đây", type=["csv", "xlsx"])
        
        if up_file:
            try:
                # Đọc file (Sửa lỗi Missing dependency)
                df_upload = pd.read_excel(up_file, engine='openpyxl') if up_file.name.endswith('xlsx') else pd.read_csv(up_file)
                
                st.write("🔍 **Dữ liệu trong file của bạn:**")
                st.dataframe(df_upload, use_container_width=True)
                
                if st.button("Xử lý và Đồng bộ lên Cloud"):
                    with st.spinner("Đang xử lý dữ liệu..."):
                        # Chuẩn hóa tên cột để khớp với Sheets của bạn
                        # Giả sử file upload có cột 'Họ Tên', 'Ngày Sinh', 'Số Điện Thoại'
                        df_upload["Số Chủ Đạo"] = df_upload["Ngày Sinh"].apply(tinh_so_chu_dao)
                        df_upload["Thời Gian"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        
                        # Chỉ lấy các cột cần thiết theo đúng thứ tự file Excel của bạn
                        cols_to_keep = ["Thời Gian", "Họ Tên", "Ngày Sinh", "Số Chủ Đạo", "Số Điện Thoại"]
                        # Nếu file upload thiếu cột nào thì tự thêm cột trống
                        for c in cols_to_keep:
                            if c not in df_upload.columns: df_upload[c] = ""
                            
                        final_upload = df_upload[cols_to_keep]
                        
                        # Ghi đè hoặc nối thêm vào Sheets
                        current_db = conn.read(ttl=0).astype(str)
                        updated_db = pd.concat([current_db, final_upload], ignore_index=True)
                        conn.update(data=updated_db)
                        
                        st.success(f"✅ Đã tải lên thành công {len(final_upload)} dòng dữ liệu!")
                        st.balloons()
            except Exception as e:
                st.error(f"Lỗi: {e}")

with tab2:
    if st.button("🔄 Làm mới dữ liệu từ Sheets"):
        st.cache_data.clear()
    data_cloud = conn.read(ttl=0)
    st.dataframe(data_cloud, use_container_width=True)
