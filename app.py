import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import unicodedata
import re
from datetime import datetime, timedelta

# --- 1. CẤU HÌNH ---
st.set_page_config(page_title="Thần Số Học 2026", page_icon="🔮", layout="wide")

# --- 2. HÀM CHUẨN HÓA THUẦN LA-TINH (Mấu chốt xử lý lỗi) ---
def clean_strictly(text):
    if text is None or str(text).lower() == "nan": return ""
    # Chuyển về chuỗi, viết thường, xóa khoảng trắng đầu cuối
    s = str(text).strip().lower()
    # Loại bỏ dấu nháy đơn thường gặp ở dữ liệu số từ Sheets
    if s.startswith("'"): s = s[1:]
    # Phân tách các tổ hợp dấu (ví dụ: 'ế' thành 'e' + dấu sắc)
    s = unicodedata.normalize('NFD', s)
    # Chỉ giữ lại các chữ cái từ a-z và số từ 0-9, loại bỏ tất cả dấu tiếng Việt và ký tự lạ
    s = ''.join([c for c in s if 'a' <= c <= 'z' or '0' <= c <= '9'])
    # Xử lý riêng ký tự 'đ' (vì NFD không tách được đ thành d + dấu)
    s = s.replace('đ', 'd')
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

    n_in = st.text_input("Họ và Tên (Không quan trọng dấu/viết hoa):")
    d_in = st.text_input("Ngày sinh (Đủ 8 số):")
    
    if st.button("Tra cứu ngay"):
        if n_in and d_in:
            try:
                # Đọc dữ liệu từ sheet Up_DaTa (Lưu ý chữ T viết hoa đúng như trên Sheet của bạn)
                df = conn.read(worksheet="Up_DaTa", ttl=0).astype(str)
                
                # Chuẩn hóa đầu vào của người dùng
                search_name = clean_strictly(n_in)
                search_date = clean_strictly(d_in)
                
                # So sánh bằng cách chuẩn hóa dữ liệu từng dòng trên Sheet
                found = False
                for index, row in df.iterrows():
                    # row.iloc[0] là Họ Tên, row.iloc[1] là Ngày Sinh
                    if clean_strictly(row.iloc[0]) == search_name and clean_strictly(row.iloc[1]) == search_date:
                        st.success(f"Chào bạn **{row.iloc[0]}**!")
                        c1, c2 = st.columns(2)
                        # Hiển thị kết quả, xử lý bỏ đuôi .0 nếu Sheets định dạng số
                        scd = str(row.iloc[3]).split('.')[0]
                        sdm = str(row.iloc[4]).split('.')[0]
                        c1.metric("Số Chủ Đạo", scd)
                        c2.metric("Số Định Mệnh", sdm)
                        
                        # Ghi nhật ký History
                        try:
                            hist_df = conn.read(worksheet="History", ttl=0)
                            new_log = pd.DataFrame([{
                                "Thời Gian Tra Cứu": (datetime.now() + timedelta(hours=7)).strftime("%d/%m/%Y %H:%M:%S"),
                                "Họ Và Tên": row.iloc[0],
                                "Ngày Sinh": f"'{d_in}",
                                "Trạng Thái": "Thành công"
                            }])
                            conn.update(worksheet="History", data=pd.concat([hist_df, new_log], ignore_index=True))
                        except: pass
                        
                        found = True
                        break
                
                if not found:
                    st.error("Không tìm thấy kết quả. Vui lòng kiểm tra lại thông tin.")
            except Exception as e:
                st.error(f"Lỗi kết nối: {e}")
        else:
            st.warning("Vui lòng nhập đầy đủ Họ tên và Ngày sinh.")

# --- 6. QUẢN LÝ DỮ LIỆU ---
elif menu == "Quản lý Up_DaTa":
    st.title("📂 Cập Nhật Dữ Liệu Nguồn")
    with st.expander("➕ Thêm khách hàng mới", expanded=True):
        with st.form("add_form"):
            c1, c2 = st.columns(2)
            name = c1.text_input("Họ Tên:")
            dob = c2.text_input("Ngày sinh (8 số):")
            phone = c1.text_input("Số Điện Thoại:")
            scd = c2.text_input("Số Chủ Đạo:")
            sdm = st.text_input("Số Định Mệnh:")
            if st.form_submit_button("Lưu"):
                if name and dob:
                    try:
                        df_old = conn.read(worksheet="Up_DaTa", ttl=0)
                        new_row = pd.DataFrame([{"Họ Tên": name, "Ngày Sinh": f"'{dob}", "Số Điện Thoại": phone, "Số Chủ Đạo": scd, "Số Định Mệnh": sdm}])
                        conn.update(worksheet="Up_DaTa", data=pd.concat([df_old, new_row], ignore_index=True))
                        st.success("Đã lưu!")
                        st.rerun()
                    except Exception as e: st.error(e)

    st.dataframe(conn.read(worksheet="Up_DaTa", ttl=0), use_container_width=True)

# --- 7. NHẬT KÝ ---
elif menu == "Nhật ký History":
    st.title("📋 Lịch Sử Hệ Thống")
    try:
        st.dataframe(conn.read(worksheet="History", ttl=0).sort_index(ascending=False), use_container_width=True)
    except: st.info("Chưa có lịch sử.")
