# -*- coding: utf-8 -*-
import streamlit as st
import os
from pathlib import Path
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
# LOGIC PHÂN QUYỀN ADMIN: Soạn thảo trực tiếp hoặc Tải file lên (.md, .txt, .docx)
# ==============================================================================
if u and u.get("vai_tro") == "admin":
    with st.expander("⚙️ BẢNG ĐIỀU KHIỂN ADMIN - CHỈNH SỬA NỘI DUNG", expanded=False):
        st.warning("Bạn đang đăng nhập bằng tài khoản Quản trị viên. Mọi thay đổi sẽ được lưu vĩnh viễn vào hệ thống.")
        
        tab_soan, tab_file = st.tabs(["✍️ Soạn thảo trực tiếp", "📁 Tải file lên (.md, .txt, .docx)"])
        
        with tab_soan:
            updated_content = st.text_area(
                "Soạn thảo nội dung giới thiệu:", 
                value=st.session_state["intro_content"], 
                height=300
            )
            if st.button("💾 Lưu nội dung soạn thảo", type="primary"):
                st.session_state["intro_content"] = updated_content
                save_intro_content(updated_content)
                st.success("Đã lưu và cập nhật thành công!")
                st.rerun()
                
        with tab_file:
            st.caption("Tải lên file định dạng Markdown, Text hoặc Word (.docx) chứa nội dung mới.")
            uploaded_file = st.file_uploader("Chọn file tải lên", type=["md", "txt", "docx"])
            
            if uploaded_file is not None:
                file_text = ""
                # Xử lý tùy thuộc vào định dạng file người dùng tải lên
                if uploaded_file.name.endswith(".docx"):
                    try:
                        import docx
                        doc = docx.Document(uploaded_file)
                        file_text = "\n".join([p.text for p in doc.paragraphs])
                    except ImportError:
                        st.error("Hệ thống chưa cài thư viện đọc file Word (`python-docx`). Hãy cài bổ sung vào requirements.txt.")
                    except Exception as e:
                        st.error(f"Lỗi đọc file Word: {e}")
                else:
                    # Xử lý file .md hoặc .txt
                    try:
                        file_text = uploaded_file.read().decode("utf-8")
                    except Exception:
                        file_text = uploaded_file.read().decode("latin-1")
                
                if file_text:
                    st.text_area("Xem trước nội dung trích xuất từ file:", value=file_text, height=200, disabled=True)
                    
                    if st.button("🚀 Xác nhận cập nhật từ file", type="primary"):
                        st.session_state["intro_content"] = file_text
                        save_intro_content(file_text)
                        st.success("Đã cập nhật nội dung từ file lên hệ thống thành công!")
                        st.rerun()
                
    st.markdown("---")

# ==============================================================================
# HIỂN THỊ NỘI DUNG CHÍNH (Áp dụng cho mọi người dùng)
# ==============================================================================
st.markdown(st.session_state["intro_content"])
