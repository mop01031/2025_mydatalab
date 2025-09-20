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

# -------------------- 폰트 설정 --------------------
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

# -------------------- 페이지 설정 --------------------
st.set_page_config(page_title="데이터분석 (3) 데이터 입력 - 예시 모드", page_icon="🧪", layout="centered")

# 예시 모드 플래그 & 흔적(일반 페이지가 들어오면 이걸 보고 초기화)
st.session_state["demo_active"] = True
st.session_state["demo_recent"] = True

# 기본 사이드바 숨기기 + 상단 종료 버튼
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 1])
with col_right:
    if st.button("🚫 예시 모드 종료", use_container_width=True, key="btn_exit_demo_topic"):
        st.session_state["came_from_demo"] = True     # 일반 페이지에서 초기화 트리거
        st.session_state.pop("demo_active", None)
        st.switch_page("pages/8_data_analysis_1_basic_info.py")

# 배너
banner = Image.open("images/(10)title_data_input.png")
st.image(banner, use_container_width=True)

# 챗봇 마운트
import chatdog_mount
chatdog_mount.mount()

# 사이드바(예시 네비)
with st.sidebar:
    st.page_link("pages/1_home.py", label="HOME", icon="🏠")
    st.markdown("---")
    st.markdown("## 📖 개념 익히기")
    st.page_link("pages/2_gradient_descent_1_optimization.py", label="(1) 최적화란?")
    st.page_link("pages/3_gradient_descent_2_learning_rate.py", label="(2) 학습률이란?")
    st.page_link("pages/4_gradient_descent_3_iterations.py", label="(3) 반복횟수란?")
    st.markdown("---")
    st.page_link("pages/5_simulation_1_learning_rate_exp.py", label="(1) 학습률 실험")
    st.page_link("pages/6_simulation_2_iterations_exp.py", label="(2) 반복횟수란?")
    st.markdown("---")
    st.page_link("pages/7_example.py", label="Q. 나 혼자 산다! 다 혼자 산다?")
    st.markdown("---")
    st.markdown("## 📊 데이터분석(예시 모드)")
    st.page_link("pages/13_data_analysis_1_basic_info_2.py", label="(1) 기본 정보 입력")
    st.page_link("pages/14_data_analysis_2_topic_selection_2.py", label="(2) 분석 주제 선택")
    st.page_link("pages/15_data_analysis_3_data_input_2.py", label="(3) 데이터 입력")
    st.page_link("pages/16_data_analysis_4_prediction_2.py", label="(4) 예측 실행")
    st.page_link("pages/17_data_analysis_5_summary_2.py", label="(5) 요약 결과")

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
# -------------------- 예시 기본값 --------------------
EX_X_LABEL = "연도"
EX_Y_LABEL = "병상수(1000명당)"
EX_DATA = [
    (2008, 12.5),(2009, 12.8),(2010, 13.0),(2011, 13.2),(2012, 13.5),
    (2013, 13.7),(2014, 14.0),(2015, 14.2),(2016, 14.3),(2017, 14.4),
    (2018, 14.5),(2019, 14.7),(2020, 15.0),(2021, 15.2),(2022, 15.3),
]
EX_ANALYSIS = (
    "2008년부터 2022년까지 우리나라 병상 수는 꾸준히 증가한 것으로 보인다. "
    "2008년 1000명 당 12.5개였던 병상 수는 해마다 늘어나서 2022년에는 15.3개에 도달했다. "
    "2008년부터 2014년까지는 빠른 증가세를 보였고 2015년부터는 증가폭이 완만해졌으나 "
    "그 이후에도 여전히 상승을 유지하고 있다."
)

# -------------------- 입력 폼 (모두 demo_* 키로 관리) --------------------
default_x = "예: 공부 시간"
default_y = "예: 성적"

input_x_label = st.text_input(
    "x축 이름",
    value=st.session_state.get("demo_x_label", EX_X_LABEL),
    placeholder=default_x,
    key="input_demo_x_label"
)
input_y_label = st.text_input(
    "y축 이름",
    value=st.session_state.get("demo_y_label", EX_Y_LABEL),
    placeholder=default_y,
    key="input_demo_y_label"
)

def safe_column_name(label, default):
    if not label or str(label).strip() == "":
        return default
    return str(label).strip()

x_label = safe_column_name(input_x_label, "X")
y_label = safe_column_name(input_y_label, "Y")

# demo 키에만 저장
st.session_state["demo_x_label"] = x_label
st.session_state["demo_y_label"] = y_label

# x/y가 비면 표 렌더링 중단
if input_x_label.strip() == "" or input_y_label.strip() == "":
    st.markdown("✅ x/y축 이름을 입력하면 아래에 표가 나타납니다.")
    st.stop()

# 표 데이터: demo 테이블만 사용
if "demo_table_data" not in st.session_state:
    st.session_state["demo_table_data"] = pd.DataFrame(
        {"x": [x for x, _ in EX_DATA], "y": [y for _, y in EX_DATA]}
    )

display_data = st.session_state["demo_table_data"].rename(columns={"x": x_label, "y": y_label})
edited_data = st.data_editor(
    display_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        x_label: st.column_config.NumberColumn(label=x_label, width="small"),
        y_label: st.column_config.NumberColumn(label=y_label, width="small")
    },
    key="data_editor_demo"
)

# 산점도 플래그 (demo)
if "demo_show_plot" not in st.session_state:
    st.session_state["demo_show_plot"] = False

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("💾 데이터 저장", key="btn_save_demo_data"):
        st.info("📌 저장 후 [📊 산점도 보기]를 눌러야 다음 단계로 이동할 수 있습니다.")
        try:
            updated_df = edited_data.rename(columns={x_label: "x", y_label: "y"})
            st.session_state["demo_table_data"] = updated_df
            st.success("✅ 데이터가 저장되었습니다!")
        except Exception as e:
            st.warning("저장 중 오류: " + str(e))
with col2:
    if st.button("📊 산점도 보기", key="btn_show_plot_demo"):
        st.session_state["demo_show_plot"] = True
with col3:
    if st.button("🔄 데이터 초기화", key="btn_reset_demo"):
        st.session_state["demo_table_data"] = pd.DataFrame({"x": [None]*10, "y": [None]*10})
        st.session_state["demo_show_plot"] = False
        st.success("모든 데이터가 초기화되었습니다.")

# -------------------- 산점도 + 분석 입력 (demo 키만) --------------------
if st.session_state["demo_show_plot"]:
    try:
        df = st.session_state["demo_table_data"].dropna()
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
            from matplotlib import ticker as _ticker
            if all(float(x).is_integer() for x in x_valid):
                ax.xaxis.set_major_formatter(_ticker.FormatStrFormatter('%d'))
            else:
                ax.xaxis.set_major_formatter(_ticker.ScalarFormatter())

            fig.tight_layout()
            st.pyplot(fig)

            # demo 키에만 저장
            st.session_state["demo_x_values"] = list(x_valid)
            st.session_state["demo_y_values"] = list(y_valid)

            st.markdown("### ✏️ 산점도를 보고 분석 내용을 작성해보세요:")
            analysis_input = st.text_area(
                label="📌 분석 내용",
                value=st.session_state.get("demo_analysis_text", EX_ANALYSIS),
                placeholder="예: 공부 시간이 많을수록 성적이 높아지는 경향이 보입니다.",
                height=150,
                key="demo_analysis_text_input"
            )
            st.session_state["demo_analysis_text"] = analysis_input

            st.success("✅ 다음 단계로 이동 가능해요.")
    except Exception as e:
        st.error("산점도 오류: " + str(e))

# -------------------- 이전/다음 --------------------
if "demo_x_values" in st.session_state and "demo_y_values" in st.session_state:
    colA, colB, colC = st.columns([3, 15, 3])
    with colA:
        if st.button("⬅️ 이전", key="btn_prev_demo"):
            st.switch_page("pages/14_data_analysis_2_topic_selection_2.py")
    with colC:
        if st.button("➡️ 다음", key="btn_next_demo"):
            # 👉 16(예시)에서 바로 사용하도록 실제 키로 복사
            st.session_state["x_label"] = st.session_state["demo_x_label"]
            st.session_state["y_label"] = st.session_state["demo_y_label"]
            st.session_state["table_data"] = st.session_state["demo_table_data"]
            st.session_state["x_values"] = st.session_state["demo_x_values"]
            st.session_state["y_values"] = st.session_state["demo_y_values"]
            st.session_state["analysis_text"] = st.session_state.get("demo_analysis_text", "")
            # (선택) 나중 일반 모드에서 깔끔히 지우려면 플래그도 남겨두기
            st.session_state["demo_seeded_xy"] = True

            st.switch_page("pages/16_data_analysis_4_prediction_2.py")