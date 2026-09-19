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
# LOGIC PHÂN QUYỀN ADMIN: Tải file Word giữ nguyên định dạng chuẩn tài liệu
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
            st.caption("Tải lên file Markdown, Text hoặc Word (.docx). Hệ thống sẽ chuyển đổi giữ nguyên bố cục và hình ảnh.")
            uploaded_file = st.file_uploader("Chọn file tải lên", type=["md", "txt", "docx"])
            
            if uploaded_file is not None:
                file_content = ""
                
                if uploaded_file.name.endswith(".docx"):
                    try:
                        import mammoth
                        # Chuyển đổi file docx sang HTML chuẩn, nhúng ảnh base64
                        result = mammoth.convert_to_html(uploaded_file)
                        file_content = result.value
                    except ImportError:
                        st.error("Hệ thống chưa cài thư viện `mammoth`. Hãy thêm `mammoth` vào requirements.txt.")
                    except Exception as e:
                        st.error(f"Lỗi đọc file Word: {e}")
                else:
                    try:
                        file_content = uploaded_file.read().decode("utf-8")
                    except Exception:
                        file_content = uploaded_file.read().decode("latin-1")
                
                if file_content:
                    st.caption("Xem trước bố cục tài liệu:")
                    # Hiển thị bản xem trước trong khung giấy
                    preview_html = f"""
                    <div style="background: #ffffff; color: #000000; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); font-family: 'Times New Roman', Times, serif; line-height: 1.65; max-height: 400px; overflow-y: auto;">
                        <style>
                            img {{ max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 4px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }}
                            h1, h2, h3, h4 {{ color: #003366; font-family: 'Times New Roman', Times, serif; margin-top: 20px; }}
                            table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
                            th, td {{ border: 1px solid #d3d3d3; padding: 8px 12px; text-align: left; }}
                            th {{ background-color: #f5f5f5; }}
                        </style>
                        {file_content}
                    </div>
                    """
                    st.markdown(preview_html, unsafe_allow_html=True)
                    
                    if st.button("🚀 Xác nhận cập nhật từ file", type="primary"):
                        st.session_state["intro_content"] = file_content
                        save_intro_content(file_content)
                        st.success("Đã cập nhật nội dung chuẩn định dạng từ file thành công!")
                        st.rerun()
                
    st.markdown("---")

# ==============================================================================
# HIỂN THỊ NỘI DUNG CHÍNH (Đóng khung giống như một trang tài liệu Word thực thụ)
# ==============================================================================
document_html = f"""
<div style="
    background: #ffffff;
    color: #111111;
    padding: 50px 60px;
    margin: 10px auto;
    max-width: 900px;
    border-radius: 6px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    font-family: 'Times New Roman', Times, serif;
    line-height: 1.7;
    font-size: 17px;
">
    <style>
        /* Tùy chỉnh CSS để hình ảnh, tiêu đề, bảng hiển thị y hệt văn bản hành chính */
        img {{
            max-width: 100% !important;
            height: auto !important;
            display: block !important;
            margin: 25px auto !important;
            border-radius: 6px !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.12) !important;
        }}
        h1, h2, h3, h4, h5, h6 {{
            color: #003366 !important;
            font-family: 'Times New Roman', Times, serif !important;
            font-weight: bold !important;
            margin-top: 25px !important;
            margin-bottom: 12px !important;
        }}
        p {{
            margin-bottom: 15px !important;
            text-align: justify !important;
        }}
        ul, ol {{
            margin-bottom: 15px !important;
            padding-left: 30px !important;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}
        th, td {{
            border: 1px solid #cccccc;
            padding: 10px 14px;
            text-align: left;
        }}
        th {{
            background-color: #f0f4f8;
            color: #003366;
        }}
    </style>
    {st.session_state["intro_content"]}
</div>
"""

st.markdown(document_html, unsafe_allow_html=True)
