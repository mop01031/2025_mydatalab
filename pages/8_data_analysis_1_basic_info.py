import streamlit as st
from PIL import Image
from datetime import date as _date

st.set_page_config(
    page_title="데이터분석 (1) 기본 정보 입력",
    page_icon="📊",
    layout="centered"
)

# --- 심사용 모드 감지 & 토글 유틸 ---
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
# 엣지 감지 (False->True / True->False)
_prev = st.session_state.get("_prev_review_mode", False)
entered_review = (review_mode and not _prev)
exited_review  = ((not review_mode) and _prev)
st.session_state["_prev_review_mode"] = review_mode
st.session_state.review_mode = review_mode

# --- 기본 사이드바 숨기기 ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- 심사용 상단 토글 바(버튼 2개 위쪽, 안내 메시지 아래쪽) ---
st.markdown("""
<style>
.topbar-box {
  background: #fff7cc;
  border: 1px solid #f6c800;
  border-radius: 10px;
  padding: 10px 14px;
  margin-bottom: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,.06);
}
.topbar-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}
.topbar-msg {
  font-weight: 700;
  color: #4a3d00;
  font-size: 15px;
  line-height: 1.3;
}
.topbar-btn .stButton > button {
  height: 40px;
  padding: 0 16px;
  font-weight: 700;
  border-radius: 8px;
  white-space: nowrap;
  word-break: keep-all;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="topbar-box">', unsafe_allow_html=True)

    # ① 버튼 줄
    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown('<div class="topbar-btn">', unsafe_allow_html=True)
        if st.button("🧪 예시 모드 보기", use_container_width=True):
            _set_query_params(review="1")
            st.session_state.review_mode = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="topbar-btn">', unsafe_allow_html=True)
        if st.button("🚫 예시 모드 종료", use_container_width=True):
            _set_query_params()
            st.session_state.review_mode = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ② 메시지 줄
    msg = ("🧪 예시 모드입니다. 입력 없이도 ‘다음’으로 이동할 수 있어요."
           if review_mode else
           "🧪 예시 모드로 전환하면, 기본값과 빠른 진행이 활성화됩니다.")
    st.markdown(f'<div class="topbar-msg">{msg}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# --- 배너 ---
banner = Image.open("images/(8)title_basic_info.png")
st.image(banner, use_container_width=True)

# --- 날짜 문자열을 date 객체로 안전 변환 ---
_default_date = st.session_state.get("date")
if isinstance(_default_date, str):
    try:
        y, m, d = map(int, _default_date.split("-"))
        _default_date = _date(y, m, d)
    except Exception:
        _default_date = _date.today()

# --- 백업/복원 대상 키 정의 ---
_REVIEW_INPUT_KEYS = ["input_name", "input_id", "input_school", "input_date", "basic_info_seeded"]
_PERSIST_KEYS = ["name", "student_id", "school", "date"]
_ALL_KEYS = _REVIEW_INPUT_KEYS + _PERSIST_KEYS

def _backup_current_values():
    for k in _ALL_KEYS:
        bk = f"_backup_{k}"
        if bk not in st.session_state:
            st.session_state[bk] = st.session_state.get(k, None)

def _restore_backup_values():
    for k in _ALL_KEYS:
        bk = f"_backup_{k}"
        if bk in st.session_state:
            val = st.session_state[bk]
            if val is None:
                st.session_state.pop(k, None)
            else:
                st.session_state[k] = val
            st.session_state.pop(bk, None)
        else:
            # 백업이 없으면 리뷰 중 만든 값은 제거
            st.session_state.pop(k, None)

# --- 진입/이탈 처리 ---
if entered_review:
    _backup_current_values()
    # 심사용 기본값 주입 (위젯 키 기준)
    st.session_state["input_name"] = "홍길동"
    st.session_state["input_id"] = "20000"
    st.session_state["input_school"] = "OO고등학교"
    st.session_state["input_date"] = _date.today()
    # 다음 단계 대비 저장 필드(없을 때만 기본값)
    st.session_state.setdefault("name", "홍길동")
    st.session_state.setdefault("student_id", "20000")
    st.session_state.setdefault("school", "OO고등학교")
    st.session_state.setdefault("date", str(_date.today()))
    st.session_state["basic_info_seeded"] = True
    st.rerun()

if exited_review:
    _restore_backup_values()
    st.rerun()

# --- 일반 모드: 위젯 초기 동기화(최초 1회만) ---
if not review_mode:
    if "input_name" not in st.session_state:
        st.session_state["input_name"] = st.session_state.get("name", "")
    if "input_id" not in st.session_state:
        st.session_state["input_id"] = st.session_state.get("student_id", "")
    if "input_school" not in st.session_state:
        st.session_state["input_school"] = st.session_state.get("school", "")
    if "input_date" not in st.session_state:
        st.session_state["input_date"] = _default_date or _date.today()

# --- 입력 위젯 (value 주지 말고 key만!) ---
name = st.text_input("이름", key="input_name")
student_id = st.text_input("학번", key="input_id")
school = st.text_input("학교", key="input_school")
date_value = st.date_input("날짜 선택", key="input_date")

# --- 저장 버튼 ---
if st.button("✅ 저장하기"):
    # 위젯 값은 세션에 들어있음
    name = st.session_state.get("input_name", "")
    student_id = st.session_state.get("input_id", "")
    school = st.session_state.get("input_school", "")
    date_value = st.session_state.get("input_date", _date.today())

    if name and student_id and school:
        st.session_state.name = name
        st.session_state.student_id = student_id
        st.session_state.school = school
        st.session_state.date = str(date_value)  # 다음 단계에서 문자열 사용
        st.success("✅ 정보가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
    else:
        st.warning("⚠️ 모든 항목을 입력해주세요.")

# --- 다음 버튼 조건 ---
def _can_go_next():
    if review_mode:
        return True
    return bool(st.session_state.get("name")) and bool(st.session_state.get("student_id")) and bool(st.session_state.get("school"))

if _can_go_next():
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

# 챗봇 마운트
import chatdog_mount
chatdog_mount.mount()
