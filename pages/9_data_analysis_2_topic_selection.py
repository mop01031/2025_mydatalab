import streamlit as st
from PIL import Image
from datetime import date as _date  # (향후 확장 대비)

st.set_page_config(
    page_title="데이터분석 (2) 분석 주제 선택",
    page_icon="📊",
    layout="centered"
)

# =========================
# 심사용 모드 감지 & 토글 유틸
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

qp = _get_query_params()
review_mode = (
    (isinstance(qp.get("review"), list) and qp.get("review", ["0"])[0] == "1")
    or (qp.get("review") == "1")
    or st.session_state.get("review_mode", False)
)
st.session_state.review_mode = review_mode

# 엣지(진입/이탈) 감지
_prev = st.session_state.get("_prev_review_mode", False)
entered_review = (review_mode and not _prev)          # False -> True
exited_review  = ((not review_mode) and _prev)        # True -> False
st.session_state["_prev_review_mode"] = review_mode
# 🔧 크로스 페이지 정리 가드 (심사용 아님 + 과거 씨딩 흔적 있으면 정리)
def restore_subject_from_backup():
    if "_backup_subject" in st.session_state:
        st.session_state["subject"] = st.session_state.pop("_backup_subject")
    else:
        st.session_state.pop("subject", None)
    if "_backup_subject_saved" in st.session_state:
        st.session_state["subject_saved"] = st.session_state.pop("_backup_subject_saved")
    else:
        st.session_state.pop("subject_saved", None)
    st.session_state.pop("_topic_seeded", None)
    st.session_state["input_subject"] = st.session_state.get("subject", "")

def restore_upstream_from_backup_or_clear():
    # 리뷰 모드에서만 건드리도록 가드
    if not st.session_state.get("_topic_seeded"):
        return  # 리뷰 모드로 들어간 적 없으면 건드리지 않음

    for k in ["name", "student_id", "school", "date"]:
        bk = f"_backup_{k}"
        if bk in st.session_state:
            # 백업이 있으면 복원
            val = st.session_state.pop(bk)
            if val is None:
                st.session_state.pop(k, None)
            else:
                st.session_state[k] = val
        else:
            # 백업 없으면 제거 → 이건 리뷰 모드에서만 생겼던 값일 때만 해당
            st.session_state.pop(k, None)



# =========================
# 상단 스타일 & 토글 바
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
    msg = (
        "🧪 심사용 모드입니다. 자동으로 입력된 주제를 확인하고 ‘다음’으로 이동해주세요."
        if review_mode else
        "🧪 심사용 모드로 전환하면, 시연용 기본값과 빠른 진행이 활성화됩니다."
    )
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
# 배너
# =========================
banner = Image.open("images/(9)title_select_topic.png")
st.image(banner, use_container_width=True)

# =========================
# 챗봇 마운트
# =========================
import chatdog_mount
chatdog_mount.mount()

# =========================
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
# 이전 단계(기본정보) 확인: 심사용이면 우회
# =========================
if not review_mode and "name" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# =========================
# 리뷰 모드 ON/OFF 시 백업/씨딩/복원
# =========================
DEFAULT_SUBJECT = "우리나라 병상 수는 앞으로도 계속 늘어날까?"

def backup_subject_once():
    if "_backup_subject" not in st.session_state:
        st.session_state["_backup_subject"] = st.session_state.get("subject")
    if "_backup_subject_saved" not in st.session_state:
        st.session_state["_backup_subject_saved"] = st.session_state.get("subject_saved")

def restore_subject_from_backup():
    if "_backup_subject" in st.session_state:
        st.session_state["subject"] = st.session_state.pop("_backup_subject")
    else:
        st.session_state.pop("subject", None)

    if "_backup_subject_saved" in st.session_state:
        st.session_state["subject_saved"] = st.session_state.pop("_backup_subject_saved")
    else:
        st.session_state.pop("subject_saved", None)

    st.session_state.pop("_topic_seeded", None)
    st.session_state["input_subject"] = st.session_state.get("subject", "")
def backup_upstream_once():
    # 기본정보 단계 값들을 한 번만 백업
    for k in ["name", "student_id", "school", "date"]:
        bk = f"_backup_{k}"
        if bk not in st.session_state:
            st.session_state[bk] = st.session_state.get(k)

def restore_upstream_from_backup_or_clear():
    for k in ["name", "student_id", "school", "date"]:
        bk = f"_backup_{k}"
        if bk in st.session_state:
            st.session_state[k] = st.session_state.pop(bk)
        else:
            st.session_state.pop(k, None)

# ✅ 리뷰 ON: 항상(멱등) 예시 주입. 첫 ON에서만 백업+토스트
if review_mode:
    first_seed = not st.session_state.get("_topic_seeded", False)
    if first_seed:
        backup_subject_once()
        backup_upstream_once()       # ← 이 줄 추가!
        st.session_state["_topic_seeded"] = True


    # 멱등 주입 (리뷰 모드 동안에는 항상 예시 값 유지)
    st.session_state["subject"] = DEFAULT_SUBJECT
    st.session_state["subject_saved"] = True
    st.session_state["input_subject"] = DEFAULT_SUBJECT

# ✅ 리뷰 OFF: 어떤 경로로든 OFF가 되면 복원/정리 후 rerun
else:
    if st.session_state.get("_topic_seeded"):
        restore_subject_from_backup()
        restore_upstream_from_backup_or_clear()
        st.rerun()

# 일반 모드: 위젯 키 초기 동기화(최초 1회만)
if not review_mode and "input_subject" not in st.session_state:
    st.session_state["input_subject"] = st.session_state.get("subject", "")

# =========================
# 주제 입력 위젯 (key만 사용)
# =========================
subject = st.text_area(
    "📌 국가통계포털을 이용해 분석하고 싶은 데이터를 찾아보고, 주제를 작성하세요!",
    key="input_subject",
    placeholder="예: 공부시간에 대한 성적 예측하기",
    height=120
)
st.markdown("[🔎 국가통계포털 바로가기](https://kosis.kr/index/index.do)", unsafe_allow_html=True)

# =========================
# 예시 데이터 다운로드
# =========================
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

# =========================
# 저장 버튼
# =========================
with col_right:
    if st.button("✅ 주제 저장", use_container_width=True):
        if subject.strip():
            st.session_state["subject"] = subject.strip()
            st.session_state["subject_saved"] = True
            st.success("✅ 주제가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
        else:
            st.warning("⚠️ 주제를 입력해주세요.")

# =========================
# 다음/이전 이동 조건
# =========================
def _can_go_next():
    if review_mode:
        return True
    return bool(st.session_state.get("subject_saved"))

# =========================
# 하단 네비게이션
# =========================
col1, _, col3 = st.columns([3, 15, 3])
with col1:
    if st.button("⬅️ 이전"):
        st.switch_page("pages/8_data_analysis_1_basic_info.py")
with col3:
    if _can_go_next() and st.button("➡️ 다음"):
        st.switch_page("pages/10_data_analysis_3_data_input.py")
