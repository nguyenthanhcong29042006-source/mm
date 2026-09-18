# -*- coding: utf-8 -*-
import streamlit as st
import os
from core import auth

# ==============================================================================
# CƠ CHẾ LƯU TRỮ FILE CỨNG (Đảm bảo dữ liệu không bị mất khi server reset)
# ==============================================================================
DATA_FILE = "data/gioi_thieu.md"

def load_intro_content():
    """Đọc nội dung giới thiệu từ file cứng nếu tồn tại, ngược lại trả về nội dung mặc định."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return """# Giới thiệu Dự án Luật Gần Bản

**Chuyển đổi số: Không để ai bị bỏ lại phía sau.**

Trang thông tin giới thiệu và tài liệu dự án trợ giúp pháp lý, đưa chính sách pháp luật đến gần hơn với đồng bào và bà con vùng cao.
"""

def save_intro_content(content):
    """Ghi đè nội dung mới do Admin soạn thảo ra file cứng vật lý."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.write(content)

# Nạp dữ liệu vào bộ nhớ tạm session_state nếu khởi chạy lần đầu
if "intro_content" not in st.session_state:
    st.session_state["intro_content"] = load_intro_content()

# Nút điều hướng quay lại trang chủ Hỏi đáp
if st.button("⬅️ Quay lại trang Hỏi đáp chính"):
    st.switch_page("giao_dien/cong_dan.py")

st.markdown("---")
st.title("📖 Giới thiệu Dự án & Ý nghĩa")

# Lấy thông tin tài khoản đang đăng nhập để kiểm tra phân quyền
u = auth.nguoi_dang_nhap()

# ==============================================================================
# LOGIC PHÂN QUYỀN ADMIN: Chỉ tài khoản admin mới nhìn thấy khung chỉnh sửa
# ==============================================================================
if u and u.get("vai_tro") == "admin":
    with st.expander("⚙️ BẢNG ĐIỀU KHIỂN ADMIN - CHỈNH SỬA NỘI DUNG", expanded=False):
        st.warning("Bạn đang đăng nhập bằng tài khoản Quản trị viên. Mọi thay đổi sẽ được lưu vĩnh viễn vào hệ thống.")
        
        # Khung nhập liệu hỗ trợ cú pháp Markdown trực quan
        updated_content = st.text_area(
            "Soạn thảo nội dung giới thiệu:", 
            value=st.session_state["intro_content"], 
            height=350
        )
        
        col_luu, col_huy = st.columns([1, 4])
        with col_luu:
            if st.button("💾 Lưu nội dung", type="primary"):
                # Cập nhật vào session và ghi lưu trực tiếp ra file cứng
                st.session_state["intro_content"] = updated_content
                save_intro_content(updated_content)
                st.success("Đã lưu và cập nhật hệ thống thành công!")
                st.rerun()
        with col_huy:
            if st.button("🔄 Hủy / Tải lại"):
                # Khôi phục trạng thái từ file gốc
                st.session_state["intro_content"] = load_intro_content()
                st.rerun()
                
    st.markdown("---")

# ==============================================================================
# HIỂN THỊ NỘI DUNG CHÍNH (Áp dụng cho mọi người dùng)
# ==============================================================================
st.markdown(st.session_state["intro_content"])
