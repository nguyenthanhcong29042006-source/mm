# -*- coding: utf-8 -*-
import streamlit as st
import os
import base64
import html
from pathlib import Path
from core import auth

# ==============================================================================
# ÉP SÁT LỀ VÀ XÓA KHOẢNG TRẮNG THỪA TRÊN ĐẦU TRANG
# ==============================================================================
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 100% !important;
    }
    header {visibility: hidden;} /* Ẩn header mặc định của Streamlit nếu tạo khoảng trắng lớn */
</style>
""", unsafe_allow_html=True)

DATA_FILE = "data/gioi_thieu.md"

def load_intro_content():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                content = f.read()
                if content.strip():
                    return content
    except Exception:
        pass
    
    return """<h2 style="text-align: center; color: #003366;">GIỚI THIỆU DỰ ÁN</h2>
<h2 style="text-align: center; color: #003366;">LUẬT GẦN BẢN</h2>
<p style="text-align: center;"><b>Trợ lý thủ tục hành chính bằng giọng nói tiếng mẹ đẻ cho đồng bào dân tộc thiểu số</b></p>
<p style="text-align: center;"><i>“Chuyển đổi số: Không để ai bị bỏ lại phía sau”</i></p>
<hr>
<h3>I. Bối cảnh và bài toán xã hội</h3>
<p>Trong tiến trình chuyển đổi số quốc gia, hạ tầng công nghệ và điện lưới đã cơ bản phủ sóng đến các bản làng vùng cao. Tuy nhiên, rào cản về ngôn ngữ và chữ viết vẫn là thách thức lớn đối với đồng bào khi thực hiện các thủ tục hành chính thiết yếu.</p>
"""

def save_intro_content(content):
    try:
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    except Exception as e:
        st.error(f"Lỗi khi lưu tệp hệ thống: {e}")
        return False

def docx_to_exact_html(docx_file) -> str:
    try:
        import docx
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        
        doc = docx.Document(docx_file)
        html_parts = []
        
        for p in doc.paragraphs:
            align_style = "text-align: left;"
            if p.alignment == WD_ALIGN_PARAGRAPH.CENTER:
                align_style = "text-align: center;"
            elif p.alignment == WD_ALIGN_PARAGRAPH.RIGHT:
                align_style = "text-align: right;"
            elif p.alignment == WD_ALIGN_PARAGRAPH.JUSTIFY:
                align_style = "text-align: justify;"
            
            p_content = []
            for run in p.runs:
                text = run.text
                if not text:
                    try:
                        drawings = run._r.xpath('.//a:blip')
                        for blip in drawings:
                            embed = blip.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed')
                            if embed and embed in doc.part.related_parts:
                                image_part = doc.part.related_parts[embed]
                                image_bytes = image_part.blob
                                b64_img = base64.b64encode(image_bytes).decode('utf-8')
                                p_content.append(f'<div style="text-align: center;"><img src="data:image/png;base64,{b64_img}" style="max-width: 100%; height: auto; margin: 20px auto; border-radius: 6px;" /></div>')
                    except Exception:
                        pass
                    continue
                
                safe_text = html.escape(text)
                style_runs = []
                if run.bold:
                    safe_text = f"<b>{safe_text}</b>"
                if run.italic:
                    safe_text = f"<i>{safe_text}</i>"
                if run.font.color and run.font.color.rgb:
                    rgb = run.font.color.rgb
                    hex_color = f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
                    style_runs.append(f"color: {hex_color};")
                
                if style_runs:
                    safe_text = f'<span style="{" ".join(style_runs)}">{safe_text}</span>'
                p_content.append(safe_text)
            
            full_p_text = "".join(p_content)
            if full_p_text.strip() or '<img' in full_p_text:
                tag = "p"
                style_name = p.style.name.lower()
                if "heading 1" in style_name or "title" in style_name:
                    tag = "h2"
                elif "heading 2" in style_name:
                    tag = "h3"
                html_parts.append(f'<{tag} style="{align_style} margin-bottom: 12px;">{full_p_text}</{tag}>')
        
        for table in doc.tables:
            table_html = ['<div style="overflow-x: auto; margin: 20px 0;"><table style="border-collapse: collapse; width: 100%;">']
            for row in table.rows:
                table_html.append('<tr>')
                for cell in row.cells:
                    table_html.append(f'<td style="border: 1px solid #cccccc; padding: 10px 14px; text-align: left;">{html.escape(cell.text)}</td>')
                table_html.append('</tr>')
            table_html.append('</table></div>')
            html_parts.append("".join(table_html))
            
        return "\n".join(html_parts)
    except Exception as e:
        st.error(f"Không thể đọc file Word: {e}")
        return ""

if "intro_content" not in st.session_state:
    st.session_state["intro_content"] = load_intro_content()

# Nút điều hướng gọn gàng
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("⬅️ Quay lại", use_container_width=True):
        st.switch_page("giao_dien/cong_dan.py")

st.markdown("<h2 style='text-align: center; color: #003366; margin-top: 0;'>📖 Giới thiệu Dự án & Ý nghĩa</h2>", unsafe_allow_html=True)

u = auth.nguoi_dang_nhap()

if u and u.get("vai_tro") == "admin":
    with st.expander("⚙️ BẢNG ĐIỀU KHIỂN ADMIN - CHỈNH SỬA NỘI DUNG", expanded=False):
        tab_soan, tab_file = st.tabs(["✍️ Soạn thảo", "📁 Tải file lên"])
        with tab_soan:
            updated_content = st.text_area("Nội dung:", value=st.session_state["intro_content"], height=250)
            if st.button("💾 Lưu nội dung", type="primary"):
                if save_intro_content(updated_content):
                    st.session_state["intro_content"] = updated_content
                    st.success("Đã lưu thành công!")
                    st.rerun()
        with tab_file:
            uploaded_file = st.file_uploader("Tải file (.md, .txt, .docx)", type=["md", "txt", "docx"])
            if uploaded_file is not None:
                file_content = docx_to_exact_html(uploaded_file) if uploaded_file.name.endswith(".docx") else uploaded_file.read().decode("utf-8", errors="ignore")
                if file_content and st.button("🚀 Xác nhận cập nhật", type="primary", use_container_width=True):
                    if save_intro_content(file_content):
                        st.session_state["intro_content"] = file_content
                        st.success("Cập nhật thành công!")
                        st.rerun()

# Khung hiển thị nội dung chính với chuẩn Responsive tuyệt đối
document_html = f"""
<div style="
    background: #ffffff;
    color: #111111;
    padding: clamp(15px, 4vw, 40px);
    margin: 10px auto;
    max-width: 900px;
    width: 100%;
    border-radius: 6px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    font-family: 'Times New Roman', Times, serif;
    line-height: 1.7;
    font-size: clamp(15px, 1.8vw, 17px);
    box-sizing: border-box;
">
    <style>
        img {{ max-width: 100% !important; height: auto !important; display: block !important; margin: 20px auto !important; border-radius: 6px; }}
        h2, h3, h4 {{ color: #003366 !important; font-family: 'Times New Roman', Times, serif !important; word-wrap: break-word; }}
        p {{ word-wrap: break-word; }}
        table {{ border-collapse: collapse; width: 100%; margin: 15px 0; }}
        th, td {{ border: 1px solid #cccccc; padding: 8px 12px; text-align: left; }}
    </style>
    {st.session_state["intro_content"]}
</div>
"""
st.markdown(document_html, unsafe_allow_html=True)
