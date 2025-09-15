import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import platform
from matplotlib import font_manager
from PIL import Image
from pathlib import Path


st.set_page_config(
    page_title="경사하강법 (2) 학습률이란?",
    page_icon="📖",
    layout="centered"
)

font_path = "./fonts/NotoSansKR-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams["font.family"] = "Noto Sans KR"
plt.rcParams["axes.unicode_minus"] = False


hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)


banner = Image.open("images/(3)title_learning_rate.png") 
st.image(banner, use_container_width=True)
col1, col2 = st.columns([14,3])  
with col2:
    if st.button("🏠 홈으로"):
        st.switch_page("app.py")  
st.markdown("""
### 🧪 학습률이란?

- 경사하강법에서 **얼마만큼 이동할지 결정하는 값**이에요.
- 학습률이 너무 작으면 **너무 천천히 수렴**하고,  
  너무 크면 **최솟값을 지나쳐서 발산할 수 있어요.**

---

아래 그래프는 서로 다른 학습률이 어떤 이동을 만들어내는지 보여줍니다.
""")


col1, col2 = st.columns(2)
with col1:
    img1 = Image.open("images/(14)example_too_small_lr.png").resize((400, 400))  
    st.image(img1)

with col2:
    img2 = Image.open("images/(17)example_too_big_lr.png").resize((400, 400))
    st.image(img2)

st.markdown("")


col3, col4 = st.columns(2)
with col3:
    img3 = Image.open("images/(15)example_good_lr_1.png").resize((400, 400))
    st.image(img3)

with col4:
    img4 = Image.open("images/(16)example_good_lr_2.png").resize((400, 400))
    st.image(img4)

import chatdog_mount
chatdog_mount.mount()

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
