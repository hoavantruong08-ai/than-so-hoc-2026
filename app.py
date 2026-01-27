import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# --- 2. HÀM XỬ LÝ ID (Chuẩn hóa để so sánh) ---
def clean_id(text):
    if text is None or str(text).lower() == "nan": return ""
    s = str(text).strip()
    if s.startswith("'"): s = s[1:]
    s = unicodedata.normalize('NFD', s)
    s = ''.join([c for c in s if unicodedata.category(c) != 'Mn'])
    s = s.replace('đ', 'd').replace('Đ', 'D')
    s = re.sub(r'[^a-zA-Z0-9]', '', s).lower()
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

# --- 5. TRANG TRA CỨU ---
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
    d_in = st.text_input("Ngày sinh (Mã 8 số):")
    
    if st.button("Tra cứu ngay"):
        if n_in and d_in:
            try:
                # ĐÚNG TÊN SHEET: Up_DaTa
                df = conn.read(worksheet="Up_DaTa", ttl=0).astype(str)
                
                df['n_compare'] = df.iloc[:, 0].apply(clean_id)
                df['d_compare'] = df.iloc[:, 1].apply(clean_id)
                
                match = df[(df['n_compare'] == clean_id(n_in)) & (df['d_compare'] == clean_id(d_in))]
                
                if not match.empty:
                    st.success(f"Chào bạn **{match.iloc[0, 0]}**!")
                    c1, c2 = st.columns(2)
                    c1.metric("Số Chủ Đạo", match.iloc[0, 3])
                    c2.metric("Số Định Mệnh", match.iloc[0, 4])
                    
                    # Ghi History
                    try:
                        hist_df = conn.read(worksheet="History", ttl=0)
                        new_log = pd.DataFrame([{
                            "Thời Gian Tra Cứu": (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S"),
                            "Họ Và Tên": match.iloc[0, 0],
                            "Ngày Sinh": f"'{clean_id(d_in)}",
                            "Trạng Thái": "Thành công"
                        }])
                        updated_hist = pd.concat([hist_df, new_log], ignore_index=True)
                        conn.update(worksheet="History", data=updated_hist)
                    except: pass
                else:
                    st.error("Không tìm thấy dữ liệu!")
            except Exception as e:
                st.error(f"Lỗi truy xuất: {e}")
        else:
            st.warning("Vui lòng nhập đầy đủ thông tin.")

# --- 6. QUẢN LÝ DỮ LIỆU ---
elif menu == "Quản lý Up_DaTa":
    st.title("📂 Cập Nhật Dữ Liệu Nguồn")
    
    with st.expander("➕ Thêm khách hàng mới", expanded=True):
        with st.form("form_add_new"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Họ Tên khách:")
            dob = c2.text_input("Mã Ngày sinh (8 số):")
            phone = c1.text_input("Số Điện Thoại:") # Khớp với tiêu đề cột A
            scd = c2.text_input("Số Chủ Đạo:")
            sdm = st.text_input("Số Định Mệnh:")
            btn = st.form_submit_button("Lưu vào Google Sheets")
            
        if btn:
            if name and dob:
                try:
                    df_old = conn.read(worksheet="Up_DaTa", ttl=0)
                    new_row = pd.DataFrame([{
                        "Họ Tên": str(name), 
                        "Ngày Sinh": f"'{str(dob)}", 
                        "Số Điện Thoại": str(phone), 
                        "Số Chủ Đạo": str(scd), 
                        "Số Định Mệnh": str(sdm)
                    }])
                    df_final = pd.concat([df_old, new_row], ignore_index=True)
                    conn.update(worksheet="Up_DaTa", data=df_final)
                    st.success(f"Đã lưu: {name}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi: {e}")

    st.subheader("Danh sách hiện tại")
    try:
        df_src = conn.read(worksheet="Up_DaTa", ttl=0)
        st.dataframe(df_src, use_container_width=True)
    except:
        st.info("Chưa có dữ liệu.")

# --- 7. NHẬT KÝ ---
elif menu == "Nhật ký History":
    st.title("📋 Lịch Sử Hệ Thống")
    try:
        df_h = conn.read(worksheet="History", ttl=0)
        st.dataframe(df_h.sort_index(ascending=False), use_container_width=True)
    except:
        st.info("Chưa có lịch sử.")
