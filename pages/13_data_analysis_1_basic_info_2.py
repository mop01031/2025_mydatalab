# pages/13_data_analysis_1_basic_info(2).py
import streamlit as st
from PIL import Image
from datetime import date as _date

st.set_page_config(
    page_title="데이터분석 (1) 기본 정보 입력 - 예시 모드",
    page_icon="🧪",
    layout="centered"
)

# --- 기본 사이드바 숨기기 + 상단 스타일 ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    .topbar-row { margin: 8px 0 2px 0; }
    .topbar-box {
      background: #fff7cc; border: 1px solid #f6c800; border-radius: 10px;
      padding: 10px 12px; margin: 6px 0 10px 0; box-shadow: 0 2px 8px rgba(0,0,0,.06);
      font-weight: 700; color: #4a3d00; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- 상단: 예시 모드 버튼 줄 (배너 위, 8페이지와 동일 위치) ---
# 보기 버튼은 '예시 모드 중'이므로 비활성화
c1, c2 = st.columns(2, gap="small")
with c1:
    st.button("🧪 예시 모드 보기", use_container_width=True, disabled=True, key="btn_demo_view_disabled")
with c2:
    if st.button("🚫 예시 모드 종료", use_container_width=True, key="btn_demo_exit_on_13"):
        # 8로 복귀 + 초기화 트리거
        st.session_state["came_from_demo"] = True
        st.session_state.pop("demo_basic_active", None)
        st.switch_page("pages/8_data_analysis_1_basic_info.py")

# --- 배너 ---
banner = Image.open("images/(8)title_basic_info.png")
st.image(banner, use_container_width=True)
# --- 안내 박스 ---
st.markdown('<div class="topbar-box">🧪 예시 모드: 기본값이 채워져 있지만 자유롭게 수정할 수 있어요.</div>', unsafe_allow_html=True)
# --- 기본 예시값 ---
example = {
    "name": "홍길동",
    "student_id": "30000",
    "school": "OO고등학교",
    "date": _date.today(),
}

# --- 날짜 보정 헬퍼 ---
def _coerce_date(v, default=None):
    if default is None:
        default = _date.today()
    if v is None:
        return default
    if isinstance(v, _date):
        return v
    if isinstance(v, str):
        try:
            return _date.fromisoformat(v)
        except Exception:
            return default
    return default

# --- 입력 폼 (모두 demo_* 키로 분리) ---
name_demo = st.text_input(
    "이름",
    value=st.session_state.get("demo_name", example["name"]),
    key="input_name_demo",
)
student_id_demo = st.text_input(
    "학번",
    value=st.session_state.get("demo_student_id", example["student_id"]),
    key="input_id_demo",
)
school_demo = st.text_input(
    "학교",
    value=st.session_state.get("demo_school", example["school"]),
    key="input_school_demo",
)

date_demo_value = _coerce_date(st.session_state.get("demo_date", example["date"]))
date_demo = st.date_input(
    "날짜 선택",
    value=date_demo_value,
    key="input_date_demo",
)

# --- demo_* 값 유지(재실행 시 위젯 기본값으로 사용) ---
st.session_state.demo_name = name_demo
st.session_state.demo_student_id = student_id_demo
st.session_state.demo_school = school_demo
st.session_state.demo_date = str(date_demo)

st.success("✅ 예시 정보가 준비되었습니다. 수정하거나 그대로 ‘다음’으로 이동할 수 있어요.")

# --- 다음 버튼: 이때만 실제 키로 복사 → 다음 단계에서 사용 가능 ---
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    if st.button("➡️ 다음", key="btn_next_demo"):
        st.session_state.name = name_demo
        st.session_state.student_id = student_id_demo
        st.session_state.school = school_demo
        st.session_state.date = str(date_demo)
        st.session_state.demo_active = True  # (선택) 이후 단계에서 '예시 진행 중' 판단용
        st.switch_page("pages/14_data_analysis_2_topic_selection_2.py")

# --- 사이드바 (예시 모드 섹션만) ---
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
    st.markdown("## 📊 데이터분석(예시 모드)")
    st.page_link("pages/13_data_analysis_1_basic_info_2.py", label="(1) 기본 정보 입력")
    st.page_link("pages/14_data_analysis_2_topic_selection_2.py", label="(2) 분석 주제 선택")
    st.page_link("pages/15_data_analysis_3_data_input_2.py", label="(3) 데이터 입력")


# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
