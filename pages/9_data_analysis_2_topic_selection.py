import streamlit as st
from PIL import Image
from datetime import date as _date

st.set_page_config(
    page_title="데이터분석 (2) 분석 주제 선택",
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
banner = Image.open("images/(9)title_select_topic.png")  
st.image(banner, use_container_width=True)
# --- 사이드바 ---
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

# --- 이전 단계(기본정보) 확인: 심사용이면 우회 ---
if not review_mode and "name" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# --- 주제 입력 ---
subject = st.text_area(
    "📌 국가통계포털을 이용해 분석하고 싶은 데이터를 찾아보고, 주제를 작성하세요!",
    value=st.session_state.get("subject", ""),
    placeholder="예: 공부시간에 대한 성적 예측하기",
    key="input_subject"  
)
st.markdown("[🔎 국가통계포털 바로가기](https://kosis.kr/index/index.do)", unsafe_allow_html=True)

# --- 예시 데이터 다운로드 ---
col_left, col_right = st.columns([3, 1])
with col_left:
    try:
        with open("data/sample data.xlsx", "rb") as file:
            st.download_button(
                label="📥 예시 주제 및 데이터 다운로드",
                data=file,
                file_name="2008~2022년의 인구 1000명당 병상수.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except FileNotFoundError:
        st.caption("⚠️ `data/sample data.xlsx` 파일을 찾을 수 없습니다. 경로를 확인하세요.")

# --- 저장 버튼 ---
with col_right:
    if st.button("✅ 주제 저장", use_container_width=True):
        if subject.strip():
            st.session_state.subject = subject
            st.session_state.subject_saved = True
            st.success("✅ 주제가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
        else:
            st.warning("⚠️ 주제를 입력해주세요.")

# --- 다음/이전 이동 조건 (심사용이면 우회) ---
def _can_go_next():
    if review_mode:
        return True
    return bool(st.session_state.get("subject_saved"))

if review_mode:
    st.info("🧪 **심사용 모드**입니다. 주제를 저장하지 않아도 ‘다음’으로 이동할 수 있어요.")

# --- 하단 네비게이션 ---
if True:  # 항상 노출되게
    col1, _, col3 = st.columns([3, 15, 3])
    with col1:
        if st.button("⬅️ 이전"):
            # 실제 파일명으로 맞추세요 (영문 파일명 기준)
            st.switch_page("pages/8_data_analysis_1_basic_info.py")
    with col3:
        if _can_go_next() and st.button("➡️ 다음"):
            # 실제 파일명으로 맞추세요 (영문 파일명 기준)
            st.switch_page("pages/10_data_analysis_3_data_input.py")


# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
