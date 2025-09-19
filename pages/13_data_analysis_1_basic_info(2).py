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
    .top-actions { display:flex; justify-content:flex-end; gap:8px; margin: 6px 0 6px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 상단 액션: 예시모드 종료 버튼 (배너 위) ---
col_left, col_right = st.columns([3, 1])
with col_right:
    if st.button("🚫 예시 모드 종료", use_container_width=True, key="btn_exit_demo_top"):
        st.switch_page("pages/8_data_analysis_1_basic_info.py")

# --- 안내 박스 ---
st.markdown('<div class="topbar-box">🧪 예시 모드: 기본값이 채워져 있지만 자유롭게 수정할 수 있어요.</div>', unsafe_allow_html=True)

# --- 배너 이미지 ---
banner = Image.open("images/(8)title_basic_info.png")
st.image(banner, use_container_width=True)

# --- 기본 예시값 ---
example = {
    "name": "홍길동",
    "student_id": "30000",
    "school": "OO고등학교",
    "date": _date.today(),
}

# --- 입력 폼 (예시값을 기본값으로 채움, 수정 가능) ---
name = st.text_input("이름", value=st.session_state.get("name", example["name"]), key="input_name_demo")
student_id = st.text_input("학번", value=st.session_state.get("student_id", example["student_id"]), key="input_id_demo")
school = st.text_input("학교", value=st.session_state.get("school", example["school"]), key="input_school_demo")

# 날짜 기본값은 date 객체로 맞춰주기 (세션에 문자열이 들어올 수도 있어 방어코드)
_date_value = st.session_state.get("date", example["date"])
if isinstance(_date_value, str):
    try:
        _date_value = _date.fromisoformat(_date_value)
    except Exception:
        _date_value = example["date"]

date = st.date_input("날짜 선택", value=_date_value, key="input_date_demo")

# --- 세션 저장 (수정해도 반영되도록) ---
st.session_state.name = name
st.session_state.student_id = student_id
st.session_state.school = school
st.session_state.date = str(date)

st.success("✅ 예시 정보가 준비되었습니다. 수정하거나 그대로 ‘다음’으로 이동할 수 있어요.")

# --- 다음 버튼 ---
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    if st.button("➡️ 다음", key="btn_next_demo"):
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
    st.markdown("## 📊 데이터분석(예시 모드)")
    st.page_link("pages/13_data_analysis_1_basic_info(2).py", label="(1) 기본 정보 입력")

# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
