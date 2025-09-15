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
st.session_state.review_mode = review_mode

# --- 심사용 배지 & 토글 버튼 ---
badge_css = """
<style>
.badge-review{
  position: fixed; top: 14px; right: 18px; z-index: 9999;
  background: #ffed4a; color: #111; padding: 6px 10px;
  border: 1px solid #f6c800; border-radius: 999px; font-weight: 800;
  box-shadow: 0 2px 8px rgba(0,0,0,.08);
}
</style>
"""
st.markdown(badge_css, unsafe_allow_html=True)

if review_mode:
    st.markdown('<div class="badge-review">🧪 심사용</div>', unsafe_allow_html=True)
    if st.button("🚫 심사용 종료"):
        _set_query_params()
        st.session_state.review_mode = False
        st.rerun()
else:
    if st.button("🧪 심사용 모드로 보기"):
        _set_query_params(review="1")
        st.session_state.review_mode = True
        st.rerun()

# --- 기본 사이드바 숨기기 ---
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)

# --- 배너 ---
banner = Image.open("images/(8)title_basic_info.png")
st.image(banner, use_container_width=True)

# --- 입력값 (날짜 안전 변환 포함) ---
_default_date = st.session_state.get("date")
if isinstance(_default_date, str):
    try:
        y, m, d = map(int, _default_date.split("-"))
        _default_date = _date(y, m, d)
    except Exception:
        _default_date = _date.today()

name = st.text_input("이름", value=st.session_state.get("name", ""), key="input_name")
student_id = st.text_input("학번", value=st.session_state.get("student_id", ""), key="input_id")
school = st.text_input("학교", value=st.session_state.get("school", ""), key="input_school")
date_value = st.date_input("날짜 선택", value=_default_date or _date.today(), key="input_date")

# --- 저장 버튼 ---
if st.button("✅ 저장하기"):
    if name and student_id and school:
        st.session_state.name = name
        st.session_state.student_id = student_id
        st.session_state.school = school
        st.session_state.date = str(date_value)
        st.success("✅ 정보가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
    else:
        st.warning("⚠️ 모든 항목을 입력해주세요.")

# --- 다음 버튼 조건 ---
def _can_go_next():
    if review_mode:
        return True
    return bool(st.session_state.get("name")) and bool(st.session_state.get("student_id")) and bool(st.session_state.get("school"))

if review_mode:
    st.info("🧪 **심사용 모드**입니다. 입력 없이도 ‘다음’으로 이동할 수 있어요.")

if _can_go_next():
    col1, col2, col3 = st.columns([3, 1, 1])
    with col3:
        if st.button("➡️ 다음"):
            st.switch_page("pages/9_data_analysis_2_topic_selection.py")

# --- 사이드바 ---
with st.sidebar:
    st.page_link("pages/1_home.py", label="HOME", icon="🏠")
    st.page_link("app.py", label="소개하기", icon="🐶")
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

# 챗봇 마운트
import chatdog_mount
chatdog_mount.mount()
