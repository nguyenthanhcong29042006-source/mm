st.markdown("""
<style>
  /* ---------- ÉP THANH TIÊU ĐỀ LUÔN NẰM TRÊN MỘT HÀNG TRÊN MỌI THIẾT BỊ ---------- */
  div[data-testid="stHorizontalBlock"]:first-of-type {
      display: flex !important;
      flex-direction: row !important;
      flex-wrap: nowrap !important;
      align-items: center !important;
  }
  div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="stColumn"] {
      width: auto !important;
  }
  div[data-testid="stHorizontalBlock"]:first-of-type > div[data-testid="stColumn"]:first-child {
      flex-grow: 1 !important;
  }
  div[data-testid="stColumn"]:last-child {
      flex-shrink: 0 !important;
  }
  
  /* Các thiết lập CSS giao diện khác giữ nguyên như cũ... */
  .stApp, p, h1,h2,h3,h4,h5,h6, label, button, input, .stMarkdown, .stText, .stTextArea
      { font-family: 'Times New Roman', Times, serif !important; }

  [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stStatusWidget"],
  [data-testid="manage-app-button"], .stAppDeployButton, #MainMenu, footer,
  [class*="viewerBadge"], [class*="profileContainer"] { display: none !important; }

  header[data-testid="stHeader"] {
      background: transparent !important;
      height: 0 !important;
      min-height: 0 !important;
  }
  
  [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
      display: none !important;
  }

  .block-container { padding-top: 1rem !important; padding-bottom: 3rem !important; max-width: 900px !important; }

  .lgb-header {
      display: inline-flex; 
      align-items: center; 
      gap: 6px; 
      margin: 0 !important;
      padding: 0 !important;
  }
  .lgb-header img { 
      height: 28px !important; 
      width: auto !important; 
      object-fit: contain; 
      flex-shrink: 0;
  }
  .lgb-ten {
      color: #003366; font-size: 16px; font-weight: bold;
      letter-spacing: .2px; white-space: nowrap;
  }
  .lgb-slogan {
      color: #666; font-size: 11px; font-style: italic;
      border-left: 1px solid #ccc; padding-left: 6px; margin-left: 4px;
  }
  @media (max-width: 640px) {
      .lgb-slogan { display: none; }          
      .lgb-ten    { font-size: 14px; }
  }
</style>
""", unsafe_allow_html=True)
