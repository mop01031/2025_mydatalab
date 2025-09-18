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

# ---------------- 글꼴 설정 ----------------
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

st.set_page_config(page_title="데이터분석 (3) 데이터 입력", page_icon="📊", layout="centered")

# ---------------- 심사용 모드 감지 & 토글 ----------------
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

qp = _get_query_params()
review_mode = (
    (isinstance(qp.get("review"), list) and qp.get("review", ["0"])[0] == "1")
    or (qp.get("review") == "1")
    or st.session_state.get("review_mode", False)
)
st.session_state.review_mode = review_mode

# 엣지 감지(페이지 전역)
_prev = st.session_state.get("_prev_review_mode", False)
entered_review = (review_mode and not _prev)
exited_review  = ((not review_mode) and _prev)
st.session_state["_prev_review_mode"] = review_mode

# ---------------- 상단 토글 바 스타일 ----------------
st.markdown("""
<style>
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
.topbar .msg { font-weight:700; color:#4a3d00; font-size:15px; line-height:1.2; margin:0; }
.topbar-btn .stButton > button { height:44px; padding:0 14px; font-weight:600; }
[data-testid="stSidebarNav"] { display:none; }
</style>
""", unsafe_allow_html=True)

tb_left, tb_right = st.columns([8, 4], vertical_alignment="center")
with tb_left:
    msg = ("🧪 예시 모드입니다. 예시 데이터가 표에 자동 입력되어 있어요. 바로 확인하고 ‘다음’으로 이동할 수 있어요."
           if review_mode else
           "🧪 예시 모드로 전환하면, 예시 데이터 자동입력과 빠른 진행이 활성화됩니다.")
    st.markdown(f'<div class="topbar"><div class="msg">{msg}</div></div>', unsafe_allow_html=True)

with tb_right:
    st.markdown('<div class="topbar-btn">', unsafe_allow_html=True)
    if review_mode:
        if st.button("🚫 예시 모드 종료", use_container_width=True):
            _set_query_params()
            st.session_state.review_mode = False
            st.rerun()
    else:
        if st.button("🧪 예시 모드로 보기", use_container_width=True):
            _set_query_params(review="1")
            st.session_state.review_mode = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- 배너 / 챗봇 / 사이드바 ----------------
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

# ---------------- 이전 단계 가드(심사용이면 우회) ----------------
if not review_mode and ("name" not in st.session_state or "subject" not in st.session_state):
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()
# 심사용 종료: 백업 복원 + 상위 단계 값도 정리
if exited_review:
    # 1) 이 페이지에서 백업해둔 값 복원/정리
    for k in ["table_data","x_label","y_label","show_plot","x_values","y_values","analysis_text"]:
        bk = f"_backup_{k}"
        if bk in st.session_state:
            val = st.session_state.pop(bk)
            if val is None:
                st.session_state.pop(k, None)
            else:
                st.session_state[k] = val
        else:
            # 백업이 없으면 리뷰 중 생성된 값일 수 있으니 제거
            st.session_state.pop(k, None)

    st.session_state.pop("_data_input_seeded", None)

    # 2) 상위 단계(기본정보/주제선택)에서 들어왔을 수 있는 값도 정리
    #    - 백업이 있으면 복원, 없으면 제거해서 가드가 제대로 걸리게 함
    upstream_keys = ["name", "student_id", "school", "date", "subject", "subject_saved"]
    for k in upstream_keys:
        bk = f"_backup_{k}"
        if bk in st.session_state:
            st.session_state[k] = st.session_state.pop(bk)
        else:
            st.session_state.pop(k, None)

    st.rerun()


# ---------------- 페이지 전용 심사용 씨딩 + 복원 ----------------
_SEED_ROWS = [
    (2008, 12.5),(2009, 12.8),(2010, 13.0),(2011, 13.2),(2012, 13.5),
    (2013, 13.7),(2014, 14.0),(2015, 14.2),(2016, 14.3),(2017, 14.4),
    (2018, 14.5),(2019, 14.7),(2020, 15.0),(2021, 15.2),(2022, 15.3),
]
DEFAULT_X_LABEL = "연도"
DEFAULT_Y_LABEL = "인구 1000명당 병상수"

# 심사용: 이 페이지에서 아직 씨딩 안 했으면 1회 무조건 주입
if review_mode and not st.session_state.get("_data_input_seeded"):
    # 원 상태 백업(없을 때만)
    for k in ["table_data","x_label","y_label","show_plot","x_values","y_values","analysis_text"]:
        bk = f"_backup_{k}"
        if bk not in st.session_state:
            st.session_state[bk] = st.session_state.get(k, None)

    # 예시 데이터 주입
    st.session_state.table_data = pd.DataFrame(_SEED_ROWS, columns=["x","y"])
    st.session_state.x_label = DEFAULT_X_LABEL
    st.session_state.y_label = DEFAULT_Y_LABEL
    st.session_state.show_plot = True
    st.session_state.x_values = st.session_state.table_data["x"].tolist()
    st.session_state.y_values = st.session_state.table_data["y"].tolist()
    st.session_state.analysis_text = (
        "2008년부터 2022년까지 우리나라 병상 수는 꾸준히 증가한 것으로 보인다. "
        "2008년 1000명 당 12.5개였던 병상 수는 해마다 늘어나서 2022년에는 15.3개에 도달했다. "
        "2008년부터 2014년까지는 빠른 증가세를 보였고 2015년부터는 증가폭이 완만해졌으나 "
        "그 이후에도 여전히 상승을 유지하고 있다."
    )

    st.session_state["_data_input_seeded"] = True
    st.toast("🧪 예시 데이터가 자동으로 채워졌어요.", icon="✅")
    st.rerun()

# ---------------- 안내 ----------------
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
# ---------------- 축 라벨 입력 ----------------
default_x_ph = "예: 공부 시간"
default_y_ph = "예: 성적"

# 1) 위젯은 key만 쓰고, value는 세션 보조로만 사용
input_x_label = st.text_input("x축 이름",
                              key="input_x_label",
                              value=st.session_state.get("input_x_label", st.session_state.get("x_label", "")),
                              placeholder=default_x_ph)
input_y_label = st.text_input("y축 이름",
                              key="input_y_label",
                              value=st.session_state.get("input_y_label", st.session_state.get("y_label", "")),
                              placeholder=default_y_ph)

# 2) 사용자가 타이핑 중인 값(공백제거)
typed_x = (input_x_label or "").strip()
typed_y = (input_y_label or "").strip()

# 3) 표에 표시할 컬럼 라벨: 타이핑 값이 있으면 그걸 쓰고, 없으면 "현재 저장된 라벨(또는 임시 소문자)"
saved_x = st.session_state.get("x_label", "")
saved_y = st.session_state.get("y_label", "")
display_x_label = typed_x if typed_x else (saved_x if saved_x != "" else "x")
display_y_label = typed_y if typed_y else (saved_y if saved_y != "" else "y")

# 4) 일반 모드에서는 x/y 둘 다 비어있으면 아직 표를 안 보여줌
if not review_mode and (typed_x == "" or typed_y == "") and (saved_x == "" or saved_y == ""):
    st.markdown("✅ x/y축 이름을 입력하면 아래에 표가 나타납니다.")
    st.stop()

# ---------------- 데이터 편집 표 ----------------
if "table_data" not in st.session_state:
    st.session_state.table_data = pd.DataFrame({"x": [0.0] * 10, "y": [0.0] * 10})

display_data = st.session_state.table_data.rename(columns={"x": display_x_label, "y": display_y_label})
edited_data = st.data_editor(
    display_data,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        display_x_label: st.column_config.NumberColumn(label=display_x_label, width="small"),
        display_y_label: st.column_config.NumberColumn(label=display_y_label, width="small")
    },
    key="data_editor"
)

# ---------------- 컨트롤 버튼 ----------------
if "show_plot" not in st.session_state:
    st.session_state.show_plot = False

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("💾 데이터 저장"):
        st.info("📌 저장 후 [📊 산점도 보기]를 눌러야 다음 단계로 이동할 수 있습니다.")
        try:
            # ⬇⬇⬇ 저장 시점에만 세션 라벨을 업데이트
            if typed_x != "":
                st.session_state.x_label = typed_x
            elif saved_x == "":
                st.session_state.x_label = "x"

            if typed_y != "":
                st.session_state.y_label = typed_y
            elif saved_y == "":
                st.session_state.y_label = "y"

            # data_editor 결과를 원래 키로 되돌려 저장
            st.session_state.table_data = edited_data.rename(
                columns={display_x_label: "x", display_y_label: "y"}
            )
            st.success("✅ 데이터가 저장되었습니다!")
        except Exception as e:
            st.warning("저장 중 오류: " + str(e))

with col2:
    if st.button("📊 산점도 보기"):
        st.session_state.show_plot = True

with col3:
    if st.button("🔄 데이터 초기화"):
        st.session_state.table_data = pd.DataFrame({"x": [0.0]*10, "y": [0.0]*10})
        st.session_state.show_plot = False
        st.success("모든 데이터가 초기화되었습니다.")
        st.rerun()

# ---------------- 산점도 & 분석 입력 ----------------
plot_ready = False
if st.session_state.show_plot:
    try:
        # ✅ 그래프 라벨 확정(타이핑중이면 typed 값, 아니면 저장된 값, 그것도 없으면 화면 라벨)
        plot_x_label = (typed_x or saved_x or display_x_label or "x")
        plot_y_label = (typed_y or saved_y or display_y_label or "y")

        df = st.session_state.table_data.dropna()
        xs = df["x"].tolist()
        ys = df["y"].tolist()
        valid_data = [(x, y) for x, y in zip(xs, ys) if x != 0 or y != 0]

        if len(valid_data) < 2:
            st.warning("⚠️ 데이터는 2쌍 이상 필요해요.")
        else:
            x_valid, y_valid = zip(*valid_data)
            plot_ready = True

        if plot_ready:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(x_valid, y_valid)

            # ✅ 여기서 더 이상 x_label / y_label을 쓰지 않습니다.
            if font_prop:
                ax.set_xlabel(plot_x_label, fontproperties=font_prop)
                ax.set_ylabel(plot_y_label, fontproperties=font_prop)
                ax.set_title("산점도 확인하기", fontproperties=font_prop)
            else:
                ax.set_xlabel(plot_x_label)
                ax.set_ylabel(plot_y_label)
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
            if review_mode and not st.session_state.get("analysis_text"):
                st.session_state.analysis_text = (
                    "2008년부터 2022년까지 우리나라 병상 수는 꾸준히 증가한 것으로 보인다. "
                    "2008년 1000명 당 12.5개였던 병상 수는 해마다 늘어나서 2022년에는 15.3개에 도달했다. "
                    "2008년부터 2014년까지는 빠른 증가세를 보였고 2015년부터는 증가폭이 완만해졌으나 "
                    "그 이후에도 여전히 상승을 유지하고 있다."
                )
            analysis_input = st.text_area(
                "📌 분석 내용",
                value=st.session_state.get("analysis_text", ""),
                placeholder="예: 공부 시간이 많을수록 성적이 높아지는 경향이 보입니다.",
                height=150
            )
            st.session_state.analysis_text = analysis_input
            st.success("✅ 다음 단계로 이동 가능해요.")
    except Exception as e:
        st.error("산점도 오류: " + str(e))

# ---------------- 다음/이전 ----------------
def _can_go_next():
    return ("x_values" in st.session_state and "y_values" in st.session_state)

colA, colB, colC = st.columns([3, 15, 3])
with colA:
    if st.button("⬅️ 이전"):
        st.switch_page("pages/9_data_analysis_2_topic_selection.py")
with colC:
    if _can_go_next() and st.button("➡️ 다음"):
        st.switch_page("pages/11_data_analysis_4_prediction.py")
