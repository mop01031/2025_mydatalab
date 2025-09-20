import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import platform
import matplotlib.font_manager as fm
import matplotlib
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
import os
from PIL import Image


font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
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

st.set_page_config(
    page_title="데이터분석 (3) 데이터 입력",
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

# --- 예시 모드 잔여 상태 정리(세이프가드) ---
if st.session_state.pop("came_from_demo", False) or st.session_state.pop("demo_recent", False):
    for k in ("lr_value", "epochs_value", "predict_requested",
              "attempt_count", "history", "selected_model_indices",
              "predict_summary"):
        st.session_state.pop(k, None)
    # 데모에서 주입한 x/y도 제거하고 싶다면(선택)
    if st.session_state.pop("demo_seeded_xy", False):
        for k in ("x_values", "y_values", "x_label", "y_label", "analysis_text"):
            st.session_state.pop(k, None)
    st.rerun()

# ✅ 예시 모드에서 돌아왔거나(플래그) 예시 데이터가 실제 키로 복사된 흔적이 있으면 초기화
demo_markers = (
    "demo_active", "demo_recent", "demo_seeded_xy",
    "demo_subject", "demo_x_label", "demo_y_label",
    "demo_table_data", "demo_x_values", "demo_y_values", "demo_analysis_text"
)

reset_needed = (
    st.session_state.pop("came_from_demo", False) or
    st.session_state.pop("demo_seeded_xy", False) or
    st.session_state.pop("demo_recent", False) or
    any(k in st.session_state for k in demo_markers)
)

if reset_needed:
    # 일반 모드 키 초기화
    for k in (
        "table_data", "x_values", "y_values",
        "x_label", "y_label",
        "analysis_text", "show_plot",
        "data_editor"  # data_editor 위젯 상태까지 리셋
    ):
        st.session_state.pop(k, None)

    # 데모 관련 키도 정리
    for k in demo_markers:
        st.session_state.pop(k, None)

    st.rerun()


banner = Image.open("images/(10)title_data_input.png")  
st.image(banner, use_container_width=True)

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

if "name" not in st.session_state or "subject" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

with st.expander("📘 사용 순서 안내 (클릭해서 열기)"):
    st.markdown("""
    1. **x축/y축 이름을 먼저 입력하세요.**  
       예: `공부시간`, `성적` 등

    2. **표에 데이터를 입력하세요.**  
       숫자만 입력 가능해요. 한 줄에 하나의 데이터쌍을 입력합니다.

    3. **[💾 데이터 저장] 버튼을 꼭 누르세요.**  
       저장하지 않으면 입력한 데이터가 사라질 수 있어요.

    4. **[📊 산점도 보기] 버튼으로 시각화 결과를 확인하세요.**

    5. 모든 조건을 만족하면 [➡️ 다음] 버튼이 활성화됩니다.
    """)

st.warning("""
⚠️ **주의사항**  
x축과 y축 이름, 데이터를 입력한 후에는 반드시 **[💾 데이터 저장] 버튼**을 눌러주세요.  
저장을 완료하지 않으면 **x/y축 이름 변경이 제대로 적용되지 않을 수 있습니다.**
""")

default_x = "예: 공부 시간"
default_y = "예: 성적"

input_x_label = st.text_input("x축 이름", placeholder=default_x)
input_y_label = st.text_input("y축 이름", placeholder=default_y)
def safe_column_name(label, default):
    if not label or str(label).strip() == "":
        return default
    return str(label).strip()


x_label = safe_column_name(input_x_label, "X")
y_label = safe_column_name(input_y_label, "Y")

st.session_state.x_label = x_label
st.session_state.y_label = y_label

if input_x_label.strip() == "" or input_y_label.strip() == "":
    st.markdown("✅ x/y축 이름을 입력하면 아래에 표가 나타납니다.")
    st.stop()


if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame({"x": [0.0] * 10, "y": [0.0] * 10})

safe_x_label = x_label
safe_y_label = y_label
display_data = st.session_state.table_data.rename(columns={"x": safe_x_label, "y": safe_y_label})

edited_data = st.data_editor(
    display_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        x_label: st.column_config.NumberColumn(label=x_label, width="small"),
        y_label: st.column_config.NumberColumn(label=y_label, width="small")
    },
    key="data_editor"
)

if "show_plot" not in st.session_state:
    st.session_state.show_plot = False

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("💾 데이터 저장"):
        st.info("📌 저장 후 [📊 산점도 보기]를 눌러야 다음 단계로 이동할 수 있습니다.")
        try:
            st.session_state.x_label = x_label
            st.session_state.y_label = y_label
            updated_df = edited_data.rename(columns={x_label: "x", y_label: "y"})
            st.session_state.table_data = updated_df
            st.success("✅ 데이터가 저장되었습니다!")
        except Exception as e:
            st.warning("저장 중 오류: " + str(e))

with col2:
    if st.button("📊 산점도 보기"):
        st.session_state.show_plot = True

with col3:
    if st.button("🔄 데이터 초기화"):
        st.session_state.table_data = pd.DataFrame({"x": [None]*10, "y": [None]*10})
        st.session_state.show_plot = False
        st.success("모든 데이터가 초기화되었습니다.")

if st.session_state.show_plot:
    try:
        df = st.session_state.table_data.dropna()
        xs = df["x"].tolist()
        ys = df["y"].tolist()
        valid_data = [(x, y) for x, y in zip(xs, ys) if x != 0 or y != 0]

        if len(valid_data) < 2:
            st.warning("⚠️ 데이터는 2쌍 이상 필요해요.")
        else:
            x_valid, y_valid = zip(*valid_data)
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(x_valid, y_valid)

            if font_prop:
                ax.set_xlabel(x_label, fontproperties=font_prop)
                ax.set_ylabel(y_label, fontproperties=font_prop)
                ax.set_title("산점도 확인하기", fontproperties=font_prop)
            else:
                ax.set_xlabel(x_label)
                ax.set_ylabel(y_label)
                ax.set_title("산점도 확인하기")

            ax.xaxis.set_major_locator(MaxNLocator(nbins='auto', prune='both'))

            import matplotlib.ticker as mtick
            ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"{int(x):,}"))
            if all(float(x).is_integer() for x in x_valid):
                ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
            else:
                ax.xaxis.set_major_formatter(ticker.ScalarFormatter())

            fig.tight_layout()
            st.pyplot(fig)

            st.session_state.x_values = list(x_valid)
            st.session_state.y_values = list(y_valid)

            st.markdown("### ✏️ 산점도를 보고 분석 내용을 작성해보세요:")
            analysis_input = st.text_area(
                label="📌 분석 내용",
                value=st.session_state.get("analysis_text", ""),
                placeholder="예: 공부 시간이 많을수록 성적이 높아지는 경향이 보입니다.",
                height=150
            )
            st.session_state.analysis_text = analysis_input

            st.success("✅ 다음 단계로 이동 가능해요.")
    except Exception as e:
        st.error("산점도 오류: " + str(e))

if "x_values" in st.session_state and "y_values" in st.session_state:
    colA, colB, colC = st.columns([3, 15, 3])
    with colA:
        if st.button("⬅️ 이전"):
            st.switch_page("pages/9_data_analysis_2_topic_selection.py")
    with colC:
        if st.button("➡️ 다음"):
            st.switch_page("pages/11_data_analysis_4_prediction.py")

