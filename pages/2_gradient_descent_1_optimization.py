import streamlit as st
from PIL import Image
from pathlib import Path


st.set_page_config(
    page_title="경사하강법 (1) 최적화란?",
    page_icon="📖",
    layout="centered"
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

banner = Image.open("images/(2)title_optimization.png")  
st.image(banner, use_container_width=True)

col1, col2 = st.columns([14,3])  
with col2:
    if st.button("🏠 홈으로"):
        st.switch_page("app.py")  


st.markdown("""
### 🧠 최적화란?

- 최적화는 어떤 문제에서 **가장 좋은 결과(최댓값 또는 최솟값)를 찾는 과정**이에요.
- 예를 들어, 공부 시간에 따른 성적을 예측할 때,
  `가장 좋은 공부 시간`을 찾는 것도 일종의 최적화 문제입니다.

---

### 📉 경사하강법이란?

- 최적화 과정에서 사용하는 알고리즘 중 하나로,
  **기울기(경사)를 따라 조금씩 이동하면서 최소값을 찾아가는 방법**이에요.
- 함수의 기울기를 계산해서 **조금씩 이동하며 손실을 줄여가는 반복적인 방법**이죠.

---

### 💡 핵심 용어 정리

- **기울기(Gradient)**: 함수가 증가하거나 감소하는 방향과 속도
- **학습률(Learning Rate)**: 한 번에 이동하는 거리
- **반복 횟수(Epoch)**: 이 과정을 몇 번 반복할 것인지

""")
import chatdog_mount
chatdog_mount.mount()

with st.sidebar:
    st.page_link("app.py", label="영상(?)",icon="🐶")
    st.page_link("pages/1_home.py", label="HOME", icon="🏠")
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
