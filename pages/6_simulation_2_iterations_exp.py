import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import platform
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import os
from matplotlib import font_manager as fm
from PIL import Image

st.set_page_config(
    page_title="시뮬레이션 (2) 반복횟수 실험",
    page_icon="💻",
    layout="centered"
)


font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams["font.family"] = font_prop.get_name()
else:
    if platform.system() == "Darwin":
        plt.rcParams["font.family"] = "AppleGothic"
    elif platform.system() == "Windows":
        plt.rcParams["font.family"] = "Malgun Gothic"
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    font_prop = None

plt.rcParams["axes.unicode_minus"] = False


hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)



import pandas as pd

df = pd.read_csv("data/data_epoch.csv")  
x = df["x"].values
y = df["y"].values


x_mean = np.mean(x)
x_centered = x - x_mean
x_input = np.linspace(min(x), max(x), 100)
x_plot = x_input - x_mean

fixed_learning_rate = 0.001 
epoch_options = [100, 500, 1000, 5000]


def gradient_descent(x, y, lr, epochs):
    m, b = 10, -10  
    n = len(x)
    for _ in range(epochs):
        y_pred = m * x + b
        dm = (-2/n) * sum(x * (y - y_pred))
        db = (-2/n) * sum(y - y_pred)
        m -= lr * dm
        b -= lr * db
    return m, b

if "draw_graph_epochs" not in st.session_state:
    st.session_state.draw_graph_epochs = False
if "select_action_epochs" not in st.session_state:
    st.session_state.select_action_epochs = None
for ep in epoch_options:
    key = f"epoch_checkbox_{ep}"
    if key not in st.session_state:
        st.session_state[key] = (ep == 100)

if st.session_state.select_action_epochs == "select_all":
    for ep in epoch_options:
        st.session_state[f"epoch_checkbox_{ep}"] = True
    st.session_state.select_action_epochs = None
    st.rerun()

elif st.session_state.select_action_epochs == "clear_all":
    for ep in epoch_options:
        st.session_state[f"epoch_checkbox_{ep}"] = False
    st.session_state.select_action_epochs = None
    st.rerun()

elif st.session_state.select_action_epochs == "reset":
    for ep in epoch_options:
        st.session_state[f"epoch_checkbox_{ep}"] = (ep == 100)
    st.session_state.draw_graph_epochs = False
    st.session_state.select_action_epochs = None
    st.rerun()

banner = Image.open("images/(6)title_epochs_exp.png")  
st.image(banner, use_container_width=True)
col1, col2 = st.columns([14,3])  
with col2:
    if st.button("🏠 홈으로"):
        st.switch_page("app.py")

st.markdown("### ✅ 비교하고 싶은 반복횟수를 선택하세요")
cols = st.columns(len(epoch_options))
selected_epochs = []
for i, ep in enumerate(epoch_options):
    key = f"epoch_checkbox_{ep}"
    if cols[i].checkbox(f"{ep}", key=key):
        selected_epochs.append(ep)

btn_row = st.columns([2, 1, 1, 1])
with btn_row[0]:
    if st.button("📈 선택한 반복횟수로 그래프 그리기", use_container_width=True):
        if selected_epochs:
            st.session_state.draw_graph_epochs = True
            st.session_state.selected_epochs_snapshot = selected_epochs.copy()
        else:
            st.warning("반복횟수를 하나 이상 선택해주세요.")
            st.session_state.draw_graph_epochs = False
with btn_row[1]:
    if st.button("✅ 전체 선택", use_container_width=True):
        st.session_state.select_action_epochs = "select_all"
        st.rerun()
with btn_row[2]:
    if st.button("❎ 전체 해제", use_container_width=True):
        st.session_state.select_action_epochs = "clear_all"
        st.rerun()
with btn_row[3]:
    if st.button("♻️ 초기화", use_container_width=True):
        st.session_state.select_action_epochs = "reset"
        st.rerun()

if st.session_state.draw_graph_epochs and "selected_epochs_snapshot" in st.session_state:
    st.markdown("### 📊 반복횟수별 그래프 비교")
    tabs = st.tabs([f"반복횟수={ep}" for ep in st.session_state.selected_epochs_snapshot])
    for i, ep in enumerate(st.session_state.selected_epochs_snapshot):
        with tabs[i]:
            m, b = gradient_descent(x_centered, y, fixed_learning_rate, ep)
            y_pred = m * x_plot + b

            fig, ax = plt.subplots()
            ax.scatter(x, y, color="blue", label="입력 데이터")
            ax.plot(x_input, y_pred, color="red", label=f"예측선 (반복횟수={ep})")
            if font_prop:
                ax.set_title(f"반복횟수 {ep}회에 대한 예측 결과", fontproperties=font_prop)
                ax.set_xlabel("x", fontproperties=font_prop)
                ax.set_ylabel("y", fontproperties=font_prop)
                ax.legend(prop=font_prop)
            else:
                ax.set_title(f"반복횟수 {ep}회에 대한 예측 결과")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.legend()
            st.pyplot(fig)

st.markdown("### 📘 실습을 통해 무엇을 배웠나요?")
st.text_area(
    "여러 반복횟수를 비교한 결과, 어떤 점을 배웠나요? 반복이 많아질수록 어떤 변화가 있었나요?",
    height=150,
    key="epoch_summary"
)



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