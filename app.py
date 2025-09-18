import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Dr.이음이와 떠나는 데이터 탐험",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"   # 🔹 사이드바 기본 접기
)

# 🔒 랜딩 페이지: 사이드바/헤더/툴바까지 전부 숨김
st.markdown("""
<style>
/* 사이드바 전체 숨김 */
[data-testid="stSidebar"], 
section[data-testid="stSidebar"],
[data-testid="stSidebarNav"] { display: none !important; }

/* 헤더(햄버거 포함) 숨김 */
header[data-testid="stHeader"] { 
  visibility: hidden; 
  height: 0 !important; 
}

/* 툴바(우측 상단 메뉴) 숨김 */
div[data-testid="stToolbar"] { display: none !important; }

/* 본문 좌우 여백 살짝 줄여 영상 강조(선택) */
.main .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

# ⬇️ 본문: 영상 + 중앙 큰 버튼만
st.video("https://youtu.be/E8-IImZ7c1Q?si=EMOphL_YXLbFuw8H")

# 버튼 스타일
st.markdown("""
<style>
/* 버튼 텍스트/크기/패딩을 강제 적용 */
div.stButton > button,
button[kind="secondary"],
button[kind="primary"] {
    font-size: 35px !important;      /* 글씨 크기 */
    font-weight: 700 !important;     /* 글씨 두께 */
    line-height: 1.25 !important;    /* 줄간격(이모지 포함 안정화) */
    padding: 20px 38px !important;   /* 버튼 크기 */
    border-radius: 16px !important;
    color: #000 !important;
    background: linear-gradient(135deg, #FFE082 0%, #FFB300 100%) !important;
    border: none !important;
    box-shadow: 0 6px 15px rgba(0,0,0,0.25) !important;
    transition: transform .25s ease, box-shadow .25s ease !important;
}

/* 호버 효과 */
div.stButton > button:hover,
button[kind="secondary"]:hover,
button[kind="primary"]:hover {
    transform: scale(1.06) !important;
    box-shadow: 0 10px 22px rgba(0,0,0,0.35) !important;
    background: linear-gradient(135deg, #FFD54F 0%, #FF8F00 100%) !important;
}

/* 내부 래퍼가 텍스트 크기를 덮어쓰는 경우 대비 */
div.stButton > button * {
    font-size: inherit !important;
    font-weight: inherit !important;
    line-height: inherit !important;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([4,3,4])
with col2:
    if st.button("🏠 홈으로 바로가기"):
        st.switch_page("pages/1_home.py")


import chatdog_mount
chatdog_mount.mount()
