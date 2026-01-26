import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Cấu hình
st.set_page_config(page_title="Thần Số Học 2026", layout="wide")

# Kết nối (Tự động lấy từ Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

def clean_and_calculate(dob_raw):
    """Hàm xử lý ngày sinh từ mọi nguồn (Date object, String, hay Excel Serial)"""
    try:
        if isinstance(dob_raw, datetime):
            s = dob_raw.strftime("%d%m%Y")
        else:
            s = "".join(filter(str.isdigit, str(dob_raw)))
        
        if len(s) < 6: return "N/A"
        
        total = sum(int(i) for i in s)
        while total > 11 and total != 22:
            total = sum(int(digit) for digit in str(total))
        return str(total)
    except:
        return "Lỗi định dạng"

# --- GIAO DIỆN ---
st.title("🔮 Hệ Thống Thần Số Học")

# Sidebar để chuyển đổi
with st.sidebar:
    st.header("Cài đặt")
    mode = st.radio("Chế độ:", ["Nhập tay", "Upload file Excel"])

if mode == "Nhập tay":
    with st.form("my_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Họ tên")
        phone = c2.text_input("Số điện thoại")
        dob = st.date_input("Ngày sinh")
        if st.form_submit_button("Lưu"):
            if name and phone:
                so = clean_and_calculate(dob)
                df_old = conn.read(ttl=0).astype(str)
                new_data = pd.DataFrame([{"Thời Gian": datetime.now().strftime("%d/%m/%Y"), "Họ Tên": name, "Ngày Sinh": dob.strftime("%d/%m/%Y"), "Số Chủ Đạo": so, "Số Điện Thoại": phone}])
                conn.update(data=pd.concat([df_old, new_data], ignore_index=True))
                st.success("Đã lưu!")

else:
    st.subheader("Tải file Excel lên")
    uploaded_file = st.file_uploader("Chọn file .xlsx", type="xlsx")
    
    if uploaded_file:
        try:
            # Đọc file
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.write("Dữ liệu tìm thấy:", df.head(3))
            
            if st.button("Xử lý & Đưa lên Sheets"):
                # Kiểm tra cột (Tên cột phải khớp với file của bạn)
                # Nếu file bạn đặt tên khác, hãy sửa tên trong ngoặc []
                if "Ngày Sinh" in df.columns:
                    df["Số Chủ Đạo"] = df["Ngày Sinh"].apply(clean_and_calculate)
                    df["Thời Gian"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                    
                    # Gộp với data hiện tại
                    old_df = conn.read(ttl=0).astype(str)
                    combined = pd.concat([old_df, df.astype(str)], ignore_index=True)
                    conn.update(data=combined)
                    st.success("Đã upload thành công!")
                    st.balloons()
                else:
                    st.error("File Excel cần có cột mang tên 'Ngày Sinh'")
        except Exception as e:
            st.error(f"Lỗi: {e}")

st.divider()
st.subheader("Dữ liệu hiện có")
try:
    st.dataframe(conn.read(ttl=0), use_container_width=True)
except:
    st.write("Chưa có dữ liệu.")
