import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Thần Số Học VIP", page_icon="🌟")
st.title("🔮 App Thần Số Học Mới - Kết Nối Thẳng")

# Link Sheet của bạn
url = "https://docs.google.com/spreadsheets/d/1zIkgqXFkF2QesVgbA5osCFgl6dnnY8lXr_JiZHzU1-c/edit#gid=0"

conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("form_moi"):
    name = st.text_input("Nhập Họ Tên:")
    phone = st.text_input("Nhập Số Điện Thoại:")
    submit = st.form_submit_button("Gửi Dữ Liệu")

if submit:
    if name and phone:
        try:
            # Đọc dữ liệu
            df = conn.read(spreadsheet=url)
            # Thêm dòng mới
            new_data = pd.DataFrame([{"Họ tên": name, "Số điện thoại": phone}])
            updated_df = pd.concat([df, new_data], ignore_index=True)
            # Cập nhật
            conn.update(spreadsheet=url, data=updated_df)
            st.success("Lưu thành công rồi nhé!")
            st.balloons()
        except Exception as e:
            st.error(f"Lỗi rồi: {e}")
    else:
        st.warning("Điền đủ thông tin đi bạn ơi!")
