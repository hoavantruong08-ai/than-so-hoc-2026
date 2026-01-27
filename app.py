import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# Ẩn menu và các nút quản lý của Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    [data-testid="stToolbar"] {display: none;}
    .stAppDeployButton {display: none !important;}
    iframe[title="Manage app"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. CÁC HÀM XỬ LÝ DỮ LIỆU ---
def clean_id(text):
    if not text or str(text) == "nan": return ""
    s = str(text).split('.')[0].strip()
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
    if s.isdigit() and len(s) == 7: s = "0" + s
    return s

def save_data(conn, sheet_name, data):
    """Hàm ghi dữ liệu đa tầng để chống lỗi AttributeError"""
    try:
        # Cách 1: Dùng phương thức chính thức hiện tại
        conn.update(worksheet=sheet_name, data=data)
    except Exception:
        try:
            # Cách 2: Dùng phương thức cũ hơn nếu server chưa cập nhật
            conn.create(worksheet=sheet_name, data=data)
        except Exception as e:
            st.error(f"Lỗi ghi Sheet: {e}. Hãy kiểm tra quyền 'Editor' của file Google Sheets.")

# --- 3. KIỂM TRA QUYỀN TRUY CẬP ---
if "role" not in st.session_state:
    st.session_state["role"] = None

with st.sidebar:
    if st.session_state["role"] == "admin":
        st.header("⚡ QUẢN TRỊ")
        menu = st.radio("Menu:", ["Tra cứu", "Quản lý Up_Data", "Nhật ký History"])
        if st.button("Đăng xuất"):
            st.session_state["role"] = None
            st.rerun()
    else:
        menu = "Tra cứu"

# --- 4. TRANG TRA CỨU ---
if menu == "Tra cứu":
    st.title("🔍 Tra Cứu Kết Quả")
    if st.session_state["role"] is None:
        pwd = st.text_input("Mật khẩu:", type="password")
        if st.button("Truy cập"):
            if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
            if pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
            st.error("Sai mật khẩu!")
        st.stop()

    conn = st.connection("gsheets", type=GSheetsConnection)
    name_in = st.text_input("Nhập Họ và Tên:")
    dob_in = st.text_input("Nhập Ngày sinh (Ví dụ: 02091997):")
    
    if st.button("Xem kết quả"):
        df = conn.read(worksheet="Up_Data", ttl=0)
        df['n_id'] = df.iloc[:, 0].apply(clean_id)
        df['d_id'] = df.iloc[:, 1].apply(clean_id)
        match = df[(df['n_id'] == clean_id(name_in)) & (df['d_id'] == clean_id(dob_in))]
        
        if not match.empty:
            st.success(f"Chào bạn **{match.iloc[0, 0]}**!")
            c1, c2 = st.columns(2)
            c1.metric("Số Chủ Đạo", str(match.iloc[0, 3]).split('.')[0])
            c2.metric("Số Định Mệnh", str(match.iloc[0, 4]).split('.')[0])
            # Ghi sử
            try:
                h_df = conn.read(worksheet="History", ttl=0)
                new_h = pd.DataFrame([{"Thời Gian Tra Cứu": (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S"), "Họ Và Tên": match.iloc[0, 0], "Ngày Sinh": f"'{clean_id(dob_in)}", "Trạng Thái": "Thành công"}])
                save_data(conn, "History", pd.concat([h_df, new_h], ignore_index=True))
            except: pass
        else: st.error("Không tìm thấy thông tin!")

# --- 5. TRANG QUẢN LÝ DỮ LIỆU NGUỒN ---
elif menu == "Quản lý Up_Data":
    st.title("📂 Cập Nhật Dữ Liệu Nguồn")
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    with st.expander("➕ Thêm khách hàng mới", expanded=True):
        with st.form("add_form_new"):
            c1, c2 = st.columns(2)
            f_name = c1.text_input("Họ Tên:")
            f_dob = c2.text_input("Mã Ngày sinh (8 số):")
            f_phone = c1.text_input("SĐT:")
            f_scd = c2.text_input("Số Chủ Đạo:")
            f_sdm = st.text_input("Số Định Mệnh:")
            if st.form_submit_button("Lưu lên Google Sheets"):
                if f_name and f_dob:
                    df_old = conn.read(worksheet="Up_Data", ttl=0)
                    new_row = pd.DataFrame([{"Họ Tên": f_name, "Ngày Sinh": f"'{f_dob}", "SĐT": f_phone, "Số Chủ Đạo": f_scd, "Số Định Mệnh": f_sdm}])
                    save_data(conn, "Up_Data", pd.concat([df_old, new_row], ignore_index=True))
                    st.success(f"Đã lưu: {f_name}")
                    st.rerun()
                else: st.warning("Hãy nhập Tên và Ngày sinh!")

    st.subheader("Danh sách hiện tại")
    st.dataframe(conn.read(worksheet="Up_Data", ttl=0), use_container_width=True)

# --- 6. NHẬT KÝ ---
elif menu == "Nhật ký History":
    st.title("📋 Lịch Sử Tra Cứu")
    conn = st.connection("gsheets", type=GSheetsConnection)
    st.dataframe(conn.read(worksheet="History", ttl=0).sort_index(ascending=False), use_container_width=True)
