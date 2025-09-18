import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import numpy as np
import os
from PIL import Image

# =========================
# 글꼴 설정
# =========================
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
    matplotlib.font_manager.fontManager.addfont(font_path)
    font_prop = fm.FontProperties(fname=font_path)
    matplotlib.rcParams["font.family"] = font_prop.get_name()
else:
    if platform.system() == "Darwin":
        matplotlib.rcParams["font.family"] = "AppleGothic"
    elif platform.system() == "Windows":
        matplotlib.rcParams["font.family"] = "Malgun Gothic"
    else:
        matplotlib.rcParams["font.family"] = "DejaVu Sans"
    font_prop = None
matplotlib.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="데이터분석 (4) 예측 실행", page_icon="📊", layout="centered")

# =========================
# 유틸: 쿼리 파라미터
# =========================
def _get_query_params():
    try:
        return st.query_params  # Streamlit >= 1.38
    except Exception:
        return st.experimental_get_query_params()

def _set_query_params(**kwargs):
    try:
        st.query_params.clear()
        for k, v in kwargs.items():
            st.query_params[k] = v
    except Exception:
        st.experimental_set_query_params(**kwargs)

# =========================
# 심사용 모드 감지 + 진입/이탈 엣지
# =========================
qp = _get_query_params()
review_mode = (
    (isinstance(qp.get("review"), list) and qp.get("review", ["0"])[0] == "1")
    or (qp.get("review") == "1")
    or st.session_state.get("review_mode", False)
)
_prev = st.session_state.get("_prev_review_mode", False)
entered_review = (review_mode and not _prev)        # False -> True
exited_review  = ((not review_mode) and _prev)      # True -> False
st.session_state["_prev_review_mode"] = review_mode
st.session_state.review_mode = review_mode

# =========================
# 스타일: 사이드바 숨김 + 상단 토글 바
# =========================
st.markdown("""
<style>
[data-testid="stSidebarNav"] { display: none; }
.topbar {
  background: #fff7cc;
  border: 1px solid #f6c800;
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
  min-height: 44px;
  display: flex;
  align-items: center;
}
.topbar .msg {
  font-weight: 700;
  color: #4a3d00;
  font-size: 15px;
  line-height: 1.2;
  margin: 0;
}
.topbar-btn .stButton > button {
  height: 44px;
  padding: 0 14px;
  font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

tb_left, tb_right = st.columns([8, 4], vertical_alignment="center")
with tb_left:
    msg = ("🧪 심사용 모드입니다. 자동 설정되어 바로 예측 결과를 볼 수 있어요."
           if review_mode else
           "🧪 심사용 모드로 전환하면, 자동 설정과 빠른 시연이 활성화됩니다.")
    st.markdown(f'<div class="topbar"><div class="msg">{msg}</div></div>', unsafe_allow_html=True)

with tb_right:
    st.markdown('<div class="topbar-btn">', unsafe_allow_html=True)
    if review_mode:
        if st.button("🚫 심사용 종료", use_container_width=True):
            _set_query_params()
            st.session_state.review_mode = False
            st.rerun()
    else:
        if st.button("🧪 심사용 모드로 보기", use_container_width=True):
            _set_query_params(review="1")
            st.session_state.review_mode = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 배너 + 챗봇
# =========================
st.image(Image.open("images/(11)title_run_prediction.png"), use_container_width=True)
import chatdog_mount
chatdog_mount.mount()
# 사이드바
# =========================
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

# =========================
# 함수: 심사용 초기 세팅 & 정리
# =========================
REVIEW_KEYS = [
    "x_values", "y_values", "x_label", "y_label",
    "lr_value", "epochs_value", "predict_requested",
    "attempt_count", "history", "predict_summary_input",
    "review_pred_seeded"
]

def seed_review_state():
    # x/y 데이터 보장
    if "x_values" not in st.session_state or "y_values" not in st.session_state:
        st.session_state.x_values = [2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022]
        st.session_state.y_values = [12.5,12.8,13.0,13.2,13.5,13.7,14.0,14.2,14.3,14.4,14.5,14.7,15.0,15.2,15.3]
        st.session_state.x_label = st.session_state.get("x_label", "연도")
        st.session_state.y_label = st.session_state.get("y_label", "인구 1000명당 병상수")

    # 하이퍼파라미터 + 자동 실행
    st.session_state.lr_value = 0.001
    st.session_state.epochs_value = 3000
    st.session_state.predict_requested = True
    st.session_state.attempt_count = st.session_state.get("attempt_count", 0) + 1

    # 히스토리 보장
    if "history" not in st.session_state or not isinstance(st.session_state.history, list):
        st.session_state.history = []

    # 예측 해석 프리필(요청하신 문구 반영)
    st.session_state["predict_summary_input"] = (
        "1차 함수 수식을 봐도 알 수 있듯이 우리나라 병상 수는 시간이 지남에 따라 꾸준히 증가하는 추세를 보이고 있다. "
        "모델 정확도는 약 98%정도로 2026년에는 1000명당 병상 수가 약 16개로 예측된다. "
        "현재와 같은 추세가 지속된다면 앞으로도 향후 몇 년 간은 병상수는 계속 증가할 것 같다. "
        "다만 장기적으로는 사회적 요인에 따라 변동 가능성도 있다는 점도 고려해야할 것이다."
    )

    st.session_state["review_pred_seeded"] = True

def clear_review_state():
    for k in REVIEW_KEYS:
        st.session_state.pop(k, None)

# ----- 여기부터 추가 (보강 가드) -----
# 심사용 모드로 '넘어온' 경우에도 자동 시드/자동 실행이 되도록 보강
needs_data = ("x_values" not in st.session_state) or ("y_values" not in st.session_state)
needs_run  = not st.session_state.get("predict_requested", False)

# (1) 먼저 종료 엣지 처리
if exited_review:
    clear_review_state()
    st.rerun()

# (2) 이 페이지에서 막 켠 경우
if entered_review:
    seed_review_state()
    st.rerun()
# (3) 이전 페이지에서 이미 켜진 상태로 넘어온 경우 → 데이터 없거나 실행 안됐으면 시드/실행
elif review_mode and (needs_data or needs_run):
    seed_review_state()
    st.rerun()
# ----- 추가 끝 -----

# =========================
# 입력 데이터 확인
# =========================
if "x_values" not in st.session_state or "y_values" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

x_raw = st.session_state.x_values
y_raw = st.session_state.y_values
x_label = st.session_state.get("x_label", "x")
y_label = st.session_state.get("y_label", "y")

# =========================
# 하이퍼파라미터 기본값
# =========================
st.session_state.setdefault("lr_value", 0.0001)
st.session_state.setdefault("epochs_value", 1000)
st.session_state.setdefault("predict_requested", False)
st.session_state.setdefault("attempt_count", 0)

learning_rate = st.session_state.lr_value
epoch = st.session_state.epochs_value

# =========================
# UI: 함수 형태/학습률/반복횟수
# =========================
st.markdown("""
<style>
.custom-radio-label h4 { margin-bottom: 0.2rem; }
div[data-testid="stRadio"] > div { margin-top: -10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("### 📈 함수 형태를 선택하세요")
func_type = st.radio(
    "함수 종류 선택",  # 실제 라벨
    ["1차 함수", "2차 함수"],
    horizontal=True,
    label_visibility="collapsed"  # 화면에는 숨김
)
st.markdown("### 🔧 학습률 조절")
lr_col1, lr_col2, lr_col3, lr_col4 = st.columns([1, 5, 1, 4])
with lr_col1:
    if st.button("➖", key="lr_minus"):
        st.session_state.lr_value = max(0.0001, st.session_state.lr_value - 0.0001)
with lr_col2:
    st.session_state.lr_value = st.slider("학습률", 0.0001, 0.01, st.session_state.lr_value,
                                          step=0.0002, format="%.4f", label_visibility="collapsed")
with lr_col3:
    if st.button("➕", key="lr_plus"):
        st.session_state.lr_value = min(0.01, st.session_state.lr_value + 0.0001)
with lr_col4:
    st.markdown(f"<b>현재 학습률: {st.session_state.lr_value:.4f}</b>", unsafe_allow_html=True)

st.markdown("### 🔁 반복 횟수 조절")
ep_col1, ep_col2, ep_col3, ep_col4 = st.columns([1, 5, 1, 4])
with ep_col1:
    if st.button("➖", key="ep_minus"):
        st.session_state.epochs_value = max(100, st.session_state.epochs_value - 100)
with ep_col2:
    st.session_state.epochs_value = st.slider("반복 횟수", 100, 7000, st.session_state.epochs_value,
                                              step=100, label_visibility="collapsed")
with ep_col3:
    if st.button("➕", key="ep_plus"):
        st.session_state.epochs_value = min(7000, st.session_state.epochs_value + 100)
with ep_col4:
    st.markdown(f"<b>현재 반복 횟수: {st.session_state.epochs_value}회</b>", unsafe_allow_html=True)

# =========================
# 예측 실행 트리거
# =========================
if st.button("📈 예측 실행"):
    x_arr = np.array(x_raw); y_arr = np.array(y_raw)
    if len(x_arr) < 2 or np.std(x_arr) == 0 or np.any(np.isnan(x_arr)) or np.any(np.isnan(y_arr)):
        st.session_state.predict_requested = False
        st.error("⚠️ 예측할 수 없습니다. 입력 데이터가 너무 적거나, 모든 X값이 같거나, 결측치가 포함되어 있습니다.")
        st.stop()
    st.session_state.predict_requested = True
    st.session_state.history = []
    st.session_state.attempt_count += 1

# =========================
# 예측/그래프/요약
# =========================
if st.session_state.predict_requested:
    st.divider()
    st.markdown("### 📊 예측 결과")

    x = np.array(x_raw)
    y = np.array(y_raw)
    x_plot = np.linspace(x.min(), x.max(), 100)

    if func_type == "1차 함수":
        x_mean = x.mean(); x_std = x.std()
        x_scaled = (x - x_mean) / x_std
        x_plot_scaled = (x_plot - x_mean) / x_std

        m, b = 0.0, 0.0
        for _ in range(epoch):
            y_pred = m * x_scaled + b
            error = y_pred - y
            m -= learning_rate * (2 / len(x)) * (error @ x_scaled)
            b -= learning_rate * (2 / len(x)) * error.sum()
            y_pred = m * x_plot_scaled + b

        m_real = m / x_std
        b_real = -m * x_mean / x_std + b
        equation = f"y = {m_real:.4f}x {'+' if b_real >= 0 else '-'} {abs(b_real):.4f}"

    else:  # 2차
        x_mean = x.mean(); x_std = x.std()
        x_scaled = (x - x_mean) / x_std
        x_plot_scaled = (x_plot - x_mean) / x_std
        a = b = c = 0.0
        for _ in range(epoch):
            y_fit = a * x_scaled**2 + b * x_scaled + c
            error = y_fit - y
            a -= learning_rate * (2 / len(x)) * (error @ (x_scaled**2))
            b -= learning_rate * (2 / len(x)) * (error @ x_scaled)
            c -= learning_rate * (2 / len(x)) * error.sum()
        y_pred = a * x_plot_scaled**2 + b * x_plot_scaled + c
        a_real = a / (x_std**2)
        b_real = (-2 * a * x_mean / (x_std**2)) + (b / x_std)
        c_real = (a * x_mean**2 / (x_std**2)) - (b * x_mean / x_std) + c
        equation = f"y = {a_real:.4f}x² {'+' if b_real >= 0 else '-'} {abs(b_real):.4f}x {'+' if c_real >= 0 else '-'} {abs(c_real):.4f}"

    # 정확도(R^2)
    ss_total = np.sum((y - y.mean()) ** 2)
    if func_type == "1차 함수":
        y_pred_for_acc = m * ((x - x.mean()) / x.std()) + b
    else:
        y_pred_for_acc = a * ((x - x_mean) / x_std)**2 + b * ((x - x_mean) / x_std) + c
    ss_res = np.sum((y - y_pred_for_acc) ** 2)
    r2 = 1 - ss_res / ss_total

    if (np.any(np.isnan(y_pred)) or np.any(np.isinf(y_pred)) or
        np.isnan(ss_total) or np.isnan(ss_res) or np.isnan(r2) or
        np.isinf(ss_total) or np.isinf(ss_res) or np.isinf(r2)):
        st.session_state.predict_requested = False
        st.error("❌ 예측 결과가 유효하지 않습니다.\n학습률이 너무 크거나 반복 횟수가 너무 많을 수 있습니다.\n적절한 값으로 조절해 주세요.")
        st.stop()

    accuracy = round(r2 * 100, 2)
    acc_color = "red" if accuracy >= 90 else "gray"
    acc_weight = "bold" if accuracy >= 90 else "normal"

    col1, col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        ax.scatter(x, y, label="입력 데이터")
        ax.plot(x_plot, y_pred, label="예측선",color="red")
        ax.set_title("예측 결과")
        ax.set_xlabel(x_label); ax.set_ylabel(y_label)
        ax.legend()
        ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
        fig.tight_layout()
        st.pyplot(fig)

    with col2:
        st.markdown(f"🔍 예측 시도 횟수: {st.session_state.attempt_count}회")
        st.markdown(f"🖋️ **수식**: {equation}")
        st.markdown(f"📘 **학습률**: {learning_rate}")
        st.markdown(f"🔁 **반복 횟수**: {epoch}")
        st.markdown(
            f"<div style='text-align:center; font-size:32px; font-weight:{acc_weight}; color:{acc_color};'>🎯 모델 정확도: {accuracy:.2f}%</div>",
            unsafe_allow_html=True
        )

        input_x = st.number_input("예측하고 싶은 값을 입력하세요. (예: 연도, 나이, 기온 등)",
                                  value=int(x[-1]) + 1, step=1)
        try:
            if func_type == "1차 함수":
                y_input_pred = m_real * input_x + b_real
            else:
                y_input_pred = a_real * input_x**2 + b_real * input_x + c_real

            y_min, y_max = y.min(), y.max()
            y_range = y_max - y_min
            lower_bound = y_min - y_range * 0.5
            upper_bound = y_max + y_range * 0.5

            if accuracy < 70 and (y_input_pred < lower_bound or y_input_pred > upper_bound):
                st.warning(f"⚠️ 예측값이 입력한 데이터의 범위를 벗어났습니다: {y_input_pred:.1f}\n\n학습률이나 반복 횟수를 조정해보세요.")
            else:
                st.success(f"📌 예측값: {y_input_pred:,.1f}")

            entry = {
                "x_plot": x_plot, "y_pred": y_pred, "label": equation,
                "lr": learning_rate, "epoch": epoch,
                "predicted_value": y_input_pred, "input_value": input_x,
                "accuracy": accuracy, "attempt_count": st.session_state.attempt_count
            }
            if func_type == "2차 함수":
                entry["x_mean"] = x_mean; entry["x_std"] = x_std

            if "history" not in st.session_state or not isinstance(st.session_state.history, list):
                st.session_state.history = []
            st.session_state.history.append(entry)
            st.session_state.selected_model_indices = [len(st.session_state.history) - 1]
        except Exception:
            st.warning("⚠️ 예측값 계산 중 문제가 발생했습니다. 입력값 또는 설정을 다시 확인해주세요.")

    # ---------------- 예측 결과 해석 ----------------
    st.markdown("### 📘 예측 결과 해석")
    st.session_state.setdefault("predict_summary", "")
    predict_text = st.text_area(
        "예측 결과와 수식을 바탕으로 어떤 의미 있는 결론을 도출할 수 있었나요?",
        key="predict_summary_input", height=150,
        placeholder="예: 예측 수식에 따르면 2025년에는 약 35% 수준까지 감소할 것으로 보입니다..."
    )

    colA, colB, colC = st.columns([3, 15, 3])
    with colA:
        if st.button("⬅️ 이전", key="go_back"):
            st.switch_page("pages/10_data_analysis_3_data_input.py")
    with colC:
        if st.button("➡️ 다음", key="go_summary"):
            st.session_state["predict_summary"] = predict_text
            st.switch_page("pages/12_data_analysis_5_summary.py")

# =========================
