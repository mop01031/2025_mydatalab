import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import platform
from matplotlib import font_manager
from sklearn.metrics import r2_score
from PIL import Image

st.set_page_config(
    page_title="경사하강법 (3) 반복횟수란?",
    page_icon="📘",
    layout="centered"
)


font_path = "./fonts/NotoSansKR-Regular.ttf"
font_manager.fontManager.addfont(font_path)
plt.rcParams["font.family"] = "Noto Sans KR"
plt.rcParams["axes.unicode_minus"] = False

# 🔒 사이드바 숨기기
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

banner = Image.open("images/(4)title_epochs.png")  
st.image(banner, use_container_width=True)
col1, col2 = st.columns([14,3])  
with col2:
    if st.button("🏠 홈으로"):
        st.switch_page("pages/1_home.py")   

st.markdown("""
### 🔁 반복횟수란?

- 경사하강법은 여러 번 반복하며 최적값을 찾아가요.
- 한 번의 반복에서 경사를 따라 이동하고,  
  이 과정을 **여러 번 반복**할수록 더 좋은 결과를 얻을 수 있어요.

---

아래 그래프는 반복횟수에 따라 예측선이 어떻게 변하는지를 보여줍니다.
""")


np.random.seed(42)
x = np.linspace(1, 10, 20)
y = 2 * x + 1 + np.random.normal(0, 1, size=len(x))

x_mean = np.mean(x)
x_centered = x - x_mean
x_input = np.linspace(min(x), max(x), 100)
x_input_centered = x_input - x_mean


def gradient_descent(x, y, lr, epochs):
    m, b = 0, 0
    n = len(x)
    for _ in range(epochs):
        y_pred = m * x + b
        dm = (-2/n) * sum(x * (y - y_pred))
        db = (-2/n) * sum(y - y_pred)
        m -= lr * dm
        b -= lr * db
    return m, b


learning_rate = 0.005
epoch_list = [10, 100, 400, 1000]
colors = ["purple", "green", "orange", "brown"]
fig, ax = plt.subplots()
ax.scatter(x, y, color="blue", label="입력 데이터")


accuracy_text = ""

for epoch, color in zip(epoch_list, colors):
    m, b = gradient_descent(x_centered, y, learning_rate, epoch)
    y_pred = m * x_input_centered + b
    ax.plot(x_input, y_pred, label=f"{epoch}회 반복", color=color, linestyle='-', linewidth=2)
    
    y_train_pred = m * x_centered + b
    r2 = r2_score(y, y_train_pred)
    accuracy_percent = round(r2 * 100)
    accuracy_text += f"🔁 {epoch}회 반복: 정확도 = {accuracy_percent}%\n"

ax.set_title("반복횟수에 따른 예측선 변화")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0))
st.pyplot(fig)


st.markdown("### 📈 반복횟수별 정확도")
st.code(accuracy_text, language="markdown")



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