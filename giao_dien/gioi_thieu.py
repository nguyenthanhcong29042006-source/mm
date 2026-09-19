# -*- coding: utf-8 -*-
import streamlit as st
import os
import zipfile
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
# LOGIC PHÂN QUYỀN ADMIN: Soạn thảo trực tiếp hoặc Tải file lên (Hỗ trợ bóc tách cả Ảnh)
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
            st.caption("Tải lên file Markdown, Text hoặc Word (.docx). Hệ thống sẽ tự động bóc tách cả chữ và hình ảnh.")
            uploaded_file = st.file_uploader("Chọn file tải lên", type=["md", "txt", "docx"])
            
            if uploaded_file is not None:
                file_text = ""
                image_markdowns = []
                
                if uploaded_file.name.endswith(".docx"):
                    try:
                        import docx
                        # 1. Đọc văn bản từ file Word
                        doc = docx.Document(uploaded_file)
                        text_parts = [p.text for p in doc.paragraphs if p.text.strip()]
                        file_text = "\n\n".join(text_parts)
                        
                        # 2. Tự động trích xuất hình ảnh từ file docx (vì docx thực chất là file nén zip)
                        uploaded_file.seek(0)
                        img_folder = "data/intro_images"
                        os.makedirs(img_folder, exist_ok=True)
                        
                        with zipfile.ZipFile(uploaded_file, 'r') as z:
                            for filename in z.namelist():
                                if filename.startswith('word/media/'):
                                    img_data = z.read(filename)
                                    img_name = os.path.basename(filename)
                                    img_path = os.path.join(img_folder, img_name)
                                    with open(img_path, "wb") as img_file:
                                        img_file.write(img_data)
                                    # Tạo cú pháp Markdown hiển thị ảnh tự động
                                    image_markdowns.append(f"\n\n![{img_name}]({img_path})\n\n")
                                    
                        # Ghép văn bản và các hình ảnh trích xuất được vào nhau
                        file_text = file_text + "".join(image_markdowns)
                        
                    except ImportError:
                        st.error("Hệ thống chưa cài thư viện `python-docx` trong requirements.txt.")
                    except Exception as e:
                        st.error(f"Lỗi xử lý file Word: {e}")
                else:
                    try:
                        file_text = uploaded_file.read().decode("utf-8")
                    except Exception:
                        file_text = uploaded_file.read().decode("latin-1")
                
                if file_text:
                    st.text_area("Xem trước nội dung (bao gồm cả ảnh trích xuất):", value=file_text, height=200, disabled=True)
                    
                    if st.button("🚀 Xác nhận cập nhật từ file", type="primary"):
                        st.session_state["intro_content"] = file_text
                        save_intro_content(file_text)
                        st.success("Đã cập nhật nội dung và hình ảnh từ file lên hệ thống thành công!")
                        st.rerun()
                
    st.markdown("---")

# ==============================================================================
# HIỂN THỊ NỘI DUNG CHÍNH (Áp dụng cho mọi người dùng)
# ==============================================================================
st.markdown(st.session_state["intro_content"], unsafe_allow_html=True)
