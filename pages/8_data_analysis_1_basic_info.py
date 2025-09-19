import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="데이터분석 (1) 기본 정보 입력",
    page_icon="📊",
    layout="centered"
)

hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

# --- 배너 이미지 ---
banner = Image.open("images/(8)title_basic_info.png")  
st.image(banner, use_container_width=True)

# --- 입력 폼 ---
name = st.text_input("이름", value=st.session_state.get("name", ""), key="input_name")
student_id = st.text_input("학번", value=st.session_state.get("student_id", ""), key="input_id")
school = st.text_input("학교", value=st.session_state.get("school", ""), key="input_school")
date = st.date_input("날짜 선택", value=st.session_state.get("date"), key="input_date")

if st.button("✅ 저장하기"):
    if name and student_id and school:
        st.session_state.name = name
        st.session_state.student_id = student_id
        st.session_state.school = school
        st.session_state.date = str(date)
        st.success("✅ 정보가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
    else:
        st.warning("⚠️ 모든 항목을 입력해주세요.")

if "name" in st.session_state:
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("➡️ 다음"):
            st.switch_page("pages/9_data_analysis_2_topic_selection.py")

# --- 사이드바 ---
with st.sidebar:
    st.page_link("pages/1_home.py", label="HOME", icon="🏠")
    st.markdown("---")

    st.markdown("## 📖 개념 익히기")
    st.page_link("pages/2_gradient_descent_1_optimization.py", label="(1) 최적화란?")
    st.page_link("pages/3_gradient_descent_2_learning_rate.py", label="(2) 학습률이란?")
    st.page_link("pages/4_gradient_descent_3_iterations.py", label="(3) 반복횟수란?")

    st.markdown("---")
    st.markdown("## 💻 시뮬레이션")
    st.page_link("pages/5_simulation_1_learning_rate_exp.py", label="(1) 학습률 실험")
    st.page_link("pages/6_simulation_2_iterations_exp.py", label="(2) 반복횟수란?")

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

# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
