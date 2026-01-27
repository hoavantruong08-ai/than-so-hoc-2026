import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# --- 2. HÀM CHUẨN HÓA (Xóa dấu tiếng Việt & ký tự lạ) ---
def chuẩn_hóa(text):
    if text is None or str(text).lower() == "nan": return ""
    s = str(text).strip().lower()
    if s.startswith("'"): s = s[1:]
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    return s

# --- 3. KẾT NỐI ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. PHÂN QUYỀN ---
if "role" not in st.session_state:
    st.session_state["role"] = None

with st.sidebar:
    if st.session_state["role"] == "admin":
        st.header("⚡ QUẢN TRỊ")
        menu = st.radio("Chức năng:", ["Tra cứu", "Quản lý Up_DaTa", "Nhật ký History"])
        if st.button("Đăng xuất Admin"):
            st.session_state["role"] = None
            st.rerun()
    else:
        menu = "Tra cứu"

# --- 5. TRANG TRA CỨU (FIX TRIỆT ĐỂ) ---
if menu == "Tra cứu":
    st.title("🔍 Tra Cứu Kết Quả")
    if st.session_state["role"] is None:
        pwd = st.text_input("Nhập mật khẩu:", type="password")
        if st.button("Vào hệ thống"):
            if pwd == "khachhang2026": st.session_state["role"] = "user"; st.rerun()
            elif pwd == "admin2026": st.session_state["role"] = "admin"; st.rerun()
            else: st.error("Sai mật khẩu!")
        st.stop()

    n_in = st.text_input("Họ và Tên:")
    d_in = st.text_input("Ngày sinh (8 số):")
    
    if st.button("Tra cứu ngay"):
        if n_in and d_in:
            try:
                # Đọc dữ liệu từ sheet Up_DaTa
                df = conn.read(worksheet="Up_DaTa", ttl=0).astype(str)
                
                # Chuẩn hóa đầu vào
                ten_search = chuẩn_hóa(n_in)
                ngay_search = d_in.strip()
                
                # Tạo cột tạm đã chuẩn hóa để tìm kiếm
                df['ten_clean'] = df.iloc[:, 0].apply(chuẩn_hóa)
                df['ngay_clean'] = df.iloc[:, 1].apply(lambda x: x.replace("'", "").strip())
                
                # Tìm kiếm (Kết quả phải khớp cả tên và ngày sinh)
                match = df[(df['ten_clean'] == ten_search) & (df['ngay_clean'] == ngay_search)]
                
                if not match.empty:
                    res = match.iloc[0]
                    st.success(f"Chào bạn **{res.iloc[0]}**!")
                    c1, c2 = st.columns(2)
                    c1.metric("Số Chủ Đạo", str(res.iloc[3]).split('.')[0])
                    c2.metric("Số Định Mệnh", str(res.iloc[4]).split('.')[0])
                    
                    # Ghi History
                    try:
                        hist_df = conn.read(worksheet="History", ttl=0)
                        new_log = pd.DataFrame([{
                            "Thời Gian Tra Cứu": (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S"),
                            "Họ Và Tên": res.iloc[0],
                            "Ngày Sinh": f"'{d_in}",
                            "Trạng Thái": "Thành công"
                        }])
                        conn.update(worksheet="History", data=pd.concat([hist_df, new_log], ignore_index=True))
                    except: pass
                else:
                    st.error("Không tìm thấy dữ liệu! Bạn lưu ý nhập tên KHÔNG DẤU và ngày sinh ĐỦ 8 SỐ.")
            except Exception as e:
                st.error(f"Lỗi kết nối Sheet: {e}")
        else:
            st.warning("Vui lòng điền đủ thông tin.")

# --- 6. QUẢN LÝ DỮ LIỆU ---
elif menu == "Quản lý Up_DaTa":
    st.title("📂 Cập Nhật Dữ Liệu Nguồn")
    with st.expander("➕ Thêm khách hàng mới", expanded=True):
        with st.form("form_add"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Họ Tên khách:")
            dob = c2.text_input("Mã Ngày sinh (8 số):")
            phone = c1.text_input("Số Điện Thoại:")
            scd = c2.text_input("Số Chủ Đạo:")
            sdm = st.text_input("Số Định Mệnh:")
            if st.form_submit_button("Lưu dữ liệu"):
                if name and dob:
                    try:
                        df_old = conn.read(worksheet="Up_DaTa", ttl=0)
                        new_row = pd.DataFrame([{"Họ Tên": name, "Ngày Sinh": f"'{dob}", "Số Điện Thoại": phone, "Số Chủ Đạo": scd, "Số Định Mệnh": sdm}])
                        conn.update(worksheet="Up_DaTa", data=pd.concat([df_old, new_row], ignore_index=True))
                        st.success("Đã thêm thành công!")
                        st.rerun()
                    except Exception as e: st.error(e)

    df_src = conn.read(worksheet="Up_DaTa", ttl=0)
    st.dataframe(df_src, use_container_width=True)

# --- 7. NHẬT KÝ ---
elif menu == "Nhật ký History":
    st.title("📋 Lịch Sử Hệ Thống")
    try:
        df_h = conn.read(worksheet="History", ttl=0)
        st.dataframe(df_h.sort_index(ascending=False), use_container_width=True)
    except: st.info("Chưa có lịch sử.")
