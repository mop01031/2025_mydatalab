import streamlit as st
from PIL import Image
from pathlib import Path
import importlib.util


st.set_page_config(
    page_title="Dr.이음이와 떠나는 데이터 탐험",
    page_icon="🚀",
    layout="wide"
)

# 🔒 자동 생성된 사이드바 메뉴 숨기기
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)


#st.title("🚀 Dr.이음이와 떠나는 데이터 탐험")

# 유튜브 영상
st.video("https://youtu.be/x0lK0qsdLUo?si=o_m2xoL1vzRuSGJV")

# 🌟 노랑-주황 버튼 (글씨 검정, 굵게, 정가운데)
st.markdown("""
    <style>
    div.stButton > button {
        font-size: 32px;
        font-family: 'Arial', 'Noto Sans KR', sans-serif;
        font-weight: 800;
        color: #000000;  /* 글씨 검정 */
        padding: 16px 50px;
        border-radius: 14px;
        background: linear-gradient(135deg, #FFE082 0%, #FFB300 100%);
        border: none;
        box-shadow: 0px 6px 15px rgba(0,0,0,0.25);
        transition: all 0.3s ease;
        cursor: pointer;
        display: block;
        margin: 0 auto; /* 가운데 정렬 */
    }
    div.stButton > button:hover {
        transform: scale(1.08);
        box-shadow: 0px 10px 22px rgba(0,0,0,0.35);
        background: linear-gradient(135deg, #FFD54F 0%, #FF8F00 100%);
        color: #000000;
    }
    </style>
""", unsafe_allow_html=True)

# 버튼을 화면 정가운데 배치 (세로 가운데는 Streamlit 기본 구조상 제한적)
col1, col2, col3 = st.columns([4,3,4])
with col2:
    if st.button("🏠메인 홈으로 바로가기"):
        st.switch_page("pages/1_home.py")


with st.sidebar:
    
    st.page_link("pages/1_home.py", label="HOME", icon="🏠")
    st.page_link("app.py", label="소개하기",icon="🐶")
    st.markdown("---")

    st.markdown("## 📖 개념 익히기")
    st.page_link("pages/2_gradient_descent_1_optimization.py", label="(1) 최적화란?")
    st.page_link("pages/3_gradient_descent_2_learning_rate.py", label="(2) 학습률이란?")
    st.page_link("pages/4_gradient_descent_3_iterations.py", label="(3) 반복횟수란?")

    st.markdown("---")
    st.markdown("## 💻 시뮬레이션")
    st.page_link("pages/5_simulation_1_learning_rate_exp.py", label="(1) 학습률 실험")
    st.page_link("pages/6_simulation_2_iterations_exp.py", label="(2) 반복횟수 실험")

    st.markdown("---")
    st.markdown("## 🔎 예제")
    st.page_link("pages/7_example.py", label="Q. 나 혼자 산다! 다 혼자 산다?")

    st.markdown("---")
    st.markdown("## 📊 데이터분석")
    st.page_link("pages/8_data_analysis_1_basic_info.py", label="(1) 기본 정보 입력")
    st.page_link("pages/9_data_analysis_2_topic_selection.py", label="(2) 분석 주제 선택")
    st.page_link("pages/10_data_analysis_3_data_input.py", label="(3) 데이터 입력")
    st.page_link("pages/11_data_analysis_4_prediction.py", label="(4) 예측 실행")
    st.page_link("pages/12_data_analysis_5_summary.py", label="(5) 요약 결과")
import chatdog_mount
chatdog_mount.mount()