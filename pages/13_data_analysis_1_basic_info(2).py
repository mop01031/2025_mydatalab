# pages/13_data_analysis_1_basic_info(2).py
import streamlit as st
from PIL import Image
from datetime import date as _date

st.set_page_config(
    page_title="데이터분석 (1) 기본 정보 입력 - 예시 모드",
    page_icon="🧪",
    layout="centered"
)

# --- 기본 사이드바 숨기기 (기본 네이티브 네비게이션) ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- 배너 ---
banner = Image.open("images/(8)title_basic_info.png")
st.image(banner, use_container_width=True)

# --- 예시 모드 안내 박스 ---
st.markdown("""
<div style="
  background:#fff7cc; border:1px solid #f6c800; border-radius:10px;
  padding:12px 14px; margin-bottom:12px; box-shadow:0 2px 8px rgba(0,0,0,.06);
  font-weight:700; color:#4a3d00; text-align:center;">
🧪 예시 모드입니다. 입력값이 미리 채워져 있으며, 바로 ‘다음’으로 이동할 수 있어요.
</div>
""", unsafe_allow_html=True)

# --- 예시값 세팅 (세션에 주입) ---
example = {
    "name": "홍길동",
    "student_id": "2025-20123",
    "school": "이음고등학교",
    "date": _date.today(),
}

# 세션에 없으면 예시값으로 채움 (있어도 예시 모드에서는 예시값으로 덮어씀)
st.session_state.name = example["name"]
st.session_state.student_id = example["student_id"]
st.session_state.school = example["school"]
st.session_state.date = str(example["date"])

# --- 입력 폼 (예시 모드: 읽기 전용) ---
colA, colB = st.columns([1,1])
with colA:
    st.text_input("이름", value=st.session_state["name"], key="input_name_demo", disabled=True)
    st.text_input("학교", value=st.session_state["school"], key="input_school_demo", disabled=True)
with colB:
    st.text_input("학번", value=st.session_state["student_id"], key="input_id_demo", disabled=True)
    st.date_input("날짜 선택", value=_date.fromisoformat(st.session_state["date"]), key="input_date_demo", disabled=True)

st.success("✅ 예시 정보가 설정되었습니다. 바로 다음 단계로 이동할 수 있어요.")

# --- 다음 버튼: 실제 다음 단계로 이동 ---
if st.button("➡️ 다음 (분석 주제 선택으로 이동)"):
    st.switch_page("pages/9_data_analysis_2_topic_selection.py")

# --- 사이드바 (고정 네비게이션) ---
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

# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
