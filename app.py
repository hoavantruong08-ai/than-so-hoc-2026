import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CẤU HÌNH MẬT KHẨU ---
ADMIN_PASSWORD = "your_password_here"  # <--- THAY ĐỔI MẬT KHẨU CỦA BẠN TẠI ĐÂY

# Cấu hình trang
st.set_page_config(page_title="Quản Trị Thần Số Học", layout="wide", page_icon="🔐")

# --- KIỂM TRA ĐĂNG NHẬP ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Hệ Thống Quản Trị Bảo Mật")
    pwd_input = st.text_input("Nhập mật khẩu Admin để tiếp tục:", type="password")
    if st.button("Đăng nhập"):
        if pwd_input == ADMIN_PASSWORD:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("❌ Mật khẩu không chính xác!")
    st.stop() # Dừng app tại đây nếu chưa đăng nhập

# --- NỘI DUNG APP SAU KHI ĐĂNG NHẬP ---
conn = st.connection("gsheets", type=GSheetsConnection)

def tinh_so_chu_dao(ngay_sinh_val):
    if pd.isna(ngay_sinh_val): return "N/A"
    if isinstance(ngay_sinh_val, (datetime, pd.Timestamp)):
        digits = ngay_sinh_val.strftime("%d%m%Y")
    else:
        str_val = str(ngay_sinh_val).split(' ')[0]
        digits = "".join(filter(str.isdigit, str_val))
    if not digits: return "N/A"
    try:
        total = sum(int(i) for i in digits)
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        return total
    except: return "N/A"

def find_default_index(column_list, keywords):
    for i, name in enumerate(column_list):
        if any(key.lower() in str(name).lower() for key in keywords):
            return i
    return 0

# --- SIDEBAR ---
with st.sidebar:
    st.title("⚙️ Quản Trị")
    if st.button("Đăng xuất"):
        st.session_state["authenticated"] = False
        st.rerun()
    st.divider()
    mode = st.radio("Chế độ nhập liệu:", ["Nhập đơn lẻ", "Upload danh sách"])

# --- MAIN ---
st.title("🔮 Hệ Thống Thần Số Học (Admin)")

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
                    "Số Điện Thoại": f"'{phone}"
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
                
                st.dataframe(input_df.head(5), use_container_width=True)
                st.divider()
                cols = input_df.columns.tolist()
                c1, c2, c3 = st.columns(3)
                
                idx_name = find_default_index(cols, ["họ tên", "tên", "name"])
                idx_dob = find_default_index(cols, ["ngày sinh", "dob", "birthday"])
                idx_phone = find_default_index(cols, ["điện thoại", "phone", "sđt"])

                col_name = c1.selectbox("Cột Họ Tên", cols, index=idx_name)
                col_dob = c2.selectbox("Cột Ngày Sinh", cols, index=idx_dob)
                col_phone = c3.selectbox("Cột Số Điện Thoại", cols, index=idx_phone)

                if st.button("🪄 Xử lý & Đẩy lên Google Sheets", type="primary"):
                    with st.spinner("Đang xử lý..."):
                        processed_df = input_df[[col_name, col_dob, col_phone]].copy()
                        processed_df.columns = ["Họ Tên", "Ngày Sinh", "Số Điện Thoại"]
                        processed_df["Số Chủ Đạo"] = processed_df["Ngày Sinh"].apply(tinh_so_chu_dao)
                        processed_df["Ngày Sinh"] = processed_df["Ngày Sinh"].apply(lambda x: pd.to_datetime(x).strftime("%d/%m/%Y") if pd.notnull(x) else "")
                        processed_df["Thời Gian"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                        processed_df["Số Điện Thoại"] = processed_df["Số Điện Thoại"].astype(str)
                        
                        df_old = conn.read(ttl=0).astype(str)
                        final_df = pd.concat([df_old, processed_df], ignore_index=True)
                        conn.update(data=final_df)
                        st.success(f"✅ Đã thêm {len(processed_df)} khách hàng!")
                        st.balloons()
            except Exception as e:
                st.error(f"Lỗi: {e}")

with tab2:
    if st.button("🔄 Tải lại dữ liệu"):
        st.cache_data.clear()
        st.rerun()
    data = conn.read(ttl=0)
    st.dataframe(data, use_container_width=True, hide_index=True)
