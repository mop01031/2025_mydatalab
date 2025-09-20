import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import platform
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import os
from matplotlib import font_manager as fm
import matplotlib
matplotlib.use("Agg")  
from PIL import Image

st.set_page_config(
    page_title="시뮬레이션 (1) 학습률 실험",
    page_icon="💻",
    layout="centered"
)


font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams["font.family"] = font_name
    font_prop = fm.FontProperties(fname=font_path)
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



x = np.linspace(0, 20, 20)
noise = np.random.normal(0, 2.0, size=len(x))  
y = 5 * x + 10 + noise

x_mean = np.mean(x)
x_centered = x - x_mean
x_input = np.linspace(min(x), max(x), 100)
x_plot = x_input - x_mean
fixed_epochs = 100

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


learning_rates = [0.0001, 0.001, 0.01, 0.1]

if "draw_graph" not in st.session_state:
    st.session_state.draw_graph = False
if "select_action" not in st.session_state:
    st.session_state.select_action = None
for lr in learning_rates:
    key = f"lr_checkbox_{lr}"
    if key not in st.session_state:
        st.session_state[key] = (lr == 0.001)

if st.session_state.select_action == "select_all":
    for lr in learning_rates:
        st.session_state[f"lr_checkbox_{lr}"] = True
    st.session_state.select_action = None
    st.rerun()
elif st.session_state.select_action == "clear_all":
    for lr in learning_rates:
        st.session_state[f"lr_checkbox_{lr}"] = False
    st.session_state.select_action = None
    st.rerun()
elif st.session_state.select_action == "reset":
    for lr in learning_rates:
        st.session_state[f"lr_checkbox_{lr}"] = (lr == 0.001)
    st.session_state.draw_graph = False
    st.session_state.select_action = None
    st.rerun()


banner = Image.open("images/(5)title_learning_rate_exp.png")  
st.image(banner, use_container_width=True)

col1, col2 = st.columns([14,3])  
with col2:
    if st.button("🏠 홈으로"):
        st.switch_page("pages/1_home.py")  

st.markdown("### ✅ 비교하고 싶은 학습률을 선택하세요")
cols = st.columns(len(learning_rates))
selected_rates = []
for i, lr in enumerate(learning_rates):
    key = f"lr_checkbox_{lr}"
    if cols[i].checkbox(f"{lr}", key=key):
        selected_rates.append(lr)

current_selected = selected_rates.copy()

st.markdown("")

btn_row = st.columns([2, 1, 1, 1])
with btn_row[0]:
    if st.button("📈 선택한 학습률로 그래프 그리기", use_container_width=True):
        if selected_rates:
            st.session_state.draw_graph = True
            st.session_state.selected_rates_snapshot = selected_rates.copy()
        else:
            st.warning("학습률을 하나 이상 선택해주세요.")
            st.session_state.draw_graph = False
with btn_row[1]:
    if st.button("✅ 전체 선택", use_container_width=True):
        st.session_state.select_action = "select_all"
        st.rerun()
with btn_row[2]:
    if st.button("❎ 전체 해제", use_container_width=True):
        st.session_state.select_action = "clear_all"
        st.rerun()
with btn_row[3]:
    if st.button("♻️ 초기화", use_container_width=True):
        st.session_state.select_action = "reset"
        st.rerun()


if st.session_state.draw_graph and "selected_rates_snapshot" in st.session_state:
    st.markdown("### 📊 학습률별 그래프 비교")
    tabs = st.tabs([f"학습률={lr}" for lr in st.session_state.selected_rates_snapshot])
    for i, lr in enumerate(st.session_state.selected_rates_snapshot):
        with tabs[i]:
            m, b = gradient_descent(x_centered, y, lr, fixed_epochs)
            y_pred = m * x_input + b

            fig, ax = plt.subplots()
            ax.scatter(x, y, color="blue", label="입력 데이터")
            ax.plot(x_plot + x_mean, y_pred, color="red", label=f"예측선 (학습률={lr})")
            if font_prop:
                ax.set_title(f"학습률 {lr} 에 대한 예측 결과", fontproperties=font_prop)
                ax.set_xlabel("x", fontproperties=font_prop)
                ax.set_ylabel("y", fontproperties=font_prop)
                ax.legend(prop=font_prop)
            else:
                ax.set_title(f"학습률 {lr} 에 대한 예측 결과")
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                ax.legend()
            st.pyplot(fig)


st.markdown("### 📘 실습을 통해 무엇을 배웠나요?")
st.text_area(
    "여러 학습률을 비교한 결과, 어떤 점을 배웠나요? 가장 적절한 학습률은 무엇이라고 생각하나요?",
    height=150,
    key="final_summary"
)



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

import chatdog_mount
chatdog_mount.mount()