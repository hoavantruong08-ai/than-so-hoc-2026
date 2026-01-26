import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình trang
st.set_page_config(page_title="Thần Số Học 2026", layout="wide", page_icon="🔮")

conn = st.connection("gsheets", type=GSheetsConnection)

# --- HÀM HỖ TRỢ ---
def tinh_so_chu_dao(ngay_sinh_val):
    """Tính số chủ đạo từ ngày sinh"""
    if pd.isna(ngay_sinh_val):
        return "N/A"
    
    # Chuyển đổi về chuỗi số (bỏ các ký tự đặc biệt)
    if isinstance(ngay_sinh_val, (datetime, pd.Timestamp)):
        digits = ngay_sinh_val.strftime("%d%m%Y")
    else:
        # Xử lý chuỗi từ Excel/CSV, lấy phần ngày trước khoảng trắng (nếu có)
        str_val = str(ngay_sinh_val).split(' ')[0]
        digits = "".join(filter(str.isdigit, str_val))
    
    if not digits:
        return "N/A"
        
    try:
        total = sum(int(i) for i in digits)
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        return total
    except:
        return "N/A"

def find_default_index(column_list, keywords):
    """Tự động tìm vị trí cột dựa trên từ khóa"""
    for i, name in enumerate(column_list):
        if any(key.lower() in str(name).lower() for key in keywords):
            return i
    return 0

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Quản Trị")
    mode = st.radio("Chế độ nhập liệu:", ["Nhập đơn lẻ", "Upload danh sách"])
    st.divider()
    st.info("Phiên bản: 2.0 (Đã tối ưu Excel)")

# --- MAIN ---
st.title("🔮 Hệ Thống Thần Số Học")

tab1, tab2 = st.tabs(["✨ Xử Lý Dữ Liệu", "📊 Kho Lưu Trữ"])

with tab1:
    if mode == "Nhập đơn lẻ":
        with st.form("single_input"):
            col1, col2 = st.columns(2)
            name = col1.text_input("Họ tên:")
            phone = col2.text_input("Số điện thoại:")
            dob = st.date_input("Ngày sinh:", min_value=datetime(1950, 1, 1), format="DD/MM/YYYY")
            submit = st.form_submit_button("Tính & Lưu")
            
            if submit and name and phone:
                so = tinh_so_chu_dao(dob)
                new_data = pd.DataFrame([{
                    "Thời Gian": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "Họ Tên": name,
                    "Ngày Sinh": dob.strftime("%d/%m/%Y"),
                    "Số Chủ Đạo": str(so),
                    "Số Điện Thoại": f"'{phone}" # Thêm dấu nháy để tránh mất số 0 trong Google Sheets
                }])
                df_old = conn.read(ttl=0).astype(str)
                updated_df = pd.concat([df_old, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success(f"Đã lưu: {name} - Số chủ đạo: {so}")

    else:
        st.subheader("📁 Tải file lên hệ thống")
        uploaded_file = st.file_uploader("Chọn file Excel (.xlsx) hoặc CSV", type=["csv", "xlsx"])
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    input_df = pd.read_csv(uploaded_file)
                else:
                    input_df = pd.read_excel(uploaded_file, engine='openpyxl')
                
                # Làm sạch dữ liệu ngày tháng hiển thị trong bảng thô
                temp_display = input_df.copy()
                st.write("🔍 **Dữ liệu từ file của bạn:**")
                st.dataframe(temp_display.head(10), use_container_width=True)

                # Cấu hình chọn cột
                st.divider()
                st.markdown("### 🛠 Cấu hình cột dữ liệu")
                cols = input_df.columns.tolist()
                c1, c2, c3 = st.columns(3)
                
                # Tự động gợi ý cột
                idx_name = find_default_index(cols, ["họ tên", "tên", "name", "khách hàng"])
                idx_dob = find_default_index(cols, ["ngày sinh", "dob", "birthday", "sinh"])
                idx_phone = find_default_index(cols, ["điện thoại", "phone", "sđt", "tel"])

                col_name = c1.selectbox("Cột Họ Tên", cols, index=idx_name)
                col_dob = c2.selectbox("Cột Ngày Sinh", cols, index=idx_dob)
                col_phone = c3.selectbox("Cột Số Điện Thoại", cols, index=idx_phone)

                if st.button("🪄 Xử lý & Đẩy lên Google Sheets", type="primary", use_container_width=True):
                    with st.spinner("Đang tính toán và đồng bộ dữ liệu..."):
                        # Tạo bản sao và xử lý
                        processed_df = input_df[[col_name, col_dob, col_phone]].copy()
                        processed_df.columns = ["Họ Tên", "Ngày Sinh", "Số Điện Thoại"]
                        
                        # Tính số chủ đạo
                        processed_df["Số Chủ Đạo"] = processed_df["Ngày Sinh"].apply(tinh_so_chu_dao)
                        
                        # Định dạng lại ngày sinh thành chuỗi dd/mm/yyyy
                        def format_date(val):
                            try:
                                return pd.to_datetime(val).strftime("%d/%m/%Y")
                            except:
                                return str(val)
                        
                        processed_df["Ngày Sinh"] = processed_df["Ngày Sinh"].apply(format_date)
                        processed_df["Thời Gian"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        processed_df["Số Điện Thoại"] = processed_df["Số Điện Thoại"].astype(str)
                        
                        # Đẩy lên Sheets
                        df_old = conn.read(ttl=0).astype(str)
                        final_df = pd.concat([df_old, processed_df], ignore_index=True)
                        conn.update(data=final_df)
                        
                        st.success(f"✅ Thành công! Đã thêm {len(processed_df)} dòng vào hệ thống.")
                        st.balloons()
            except Exception as e:
                st.error(f"Lỗi: {e}. Vui lòng kiểm tra lại cấu trúc file.")

with tab2:
    col_a, col_b = st.columns([4, 1])
    col_a.subheader("📋 Danh sách đã lưu")
    if col_b.button("🔄 Tải lại", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
    
    data = conn.read(ttl=0)
    # Hiển thị bảng đẹp hơn với cấu hình cột
    st.dataframe(
        data, 
        use_container_width=True,
        column_config={
            "Thời Gian": st.column_config.TextColumn("🕒 Thời Gian"),
            "Số Chủ Đạo": st.column_config.NumberColumn("🔢 Số Chủ Đạo", format="%d"),
            "Số Điện Thoại": st.column_config.TextColumn("📞 Số Điện Thoại")
        },
        hide_index=True
    )
