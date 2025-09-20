# pages/14_data_analysis_2_topic_selection(2).py
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="데이터분석 (2) 분석 주제 선택",
    page_icon="🧪",
    layout="centered"
)

# --- 기본 사이드바 숨기기 + 상단 스타일 ---
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    .topbar-row { margin: 8px 0 2px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 예시 모드 고정 주제 ---
DEFAULT_SUBJECT = " 우리나라 병상 수는 앞으로도 계속 늘어날까? "

# ✅ 9번에서 '예시 모드 보기'를 누르고 왔으면 예시 모드 활성화 + 기본 주제로 강제 설정
if st.session_state.pop("demo_force", False):
    st.session_state["demo_active"] = True
    st.session_state["demo_subject"] = DEFAULT_SUBJECT
    st.session_state.pop("input_subject_demo", None)  # 위젯 값 초기화

# --- 상단: 예시 모드 종료(배너 위) ---
col_left, col_right = st.columns([3, 1])
with col_right:
    if st.button("🚫 예시 모드 종료", use_container_width=True, key="btn_exit_demo_topic"):
        # 예시 모드 종료시 1단계(예시)로 이동
        st.session_state["came_from_demo"] = True
        st.session_state.pop("demo_active", None)
        st.switch_page("pages/8_data_analysis_1_basic_info.py")

# --- 배너 ---
banner = Image.open("images/(9)title_select_topic.png")
st.image(banner, use_container_width=True)

# --- 사이드바 (예시 섹션 포함) ---
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
# --- 선행 단계 확인 (예시 모드가 아니면 체크, 예시 모드면 우회) ---
if not st.session_state.get("demo_active", False) and "name" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# --- 주제 입력(예시 모드에서는 항상 기본문구를 우선) ---
subject = st.text_area(
    "📌 국가통계포털을 이용해 분석하고 싶은 데이터를 찾아보고, 주제를 작성하세요!",
    value=st.session_state.get("demo_subject", DEFAULT_SUBJECT),
    placeholder="예: 공부시간에 대한 성적 예측하기",
    key="input_subject_demo"
)
st.markdown("[🔎 국가통계포털 바로가기](https://kosis.kr/index/index.do)", unsafe_allow_html=True)

# --- 예시 데이터 다운로드 + 저장 버튼 ---
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
        st.info("⚠️ 예시 파일(data/sample data.xlsx)을 찾을 수 없습니다. 경로를 확인해주세요.")

with col_right:
    if st.button("✅ 주제 저장", use_container_width=True, key="btn_save_demo"):
        if subject.strip():
            st.session_state.subject = subject            # 실제 키에도 저장(다음 단계 사용)
            st.session_state.demo_subject = subject       # 데모 기본값 업데이트
            st.session_state.subject_saved = True
        else:
            st.warning("⚠️ 주제를 입력해주세요.")

if st.session_state.get("subject_saved"):
    st.success("✅ 주제가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")

# --- 이전/다음 이동 ---
if subject.strip():
    col1, col2, col3 = st.columns([3, 15, 3])
    with col1:
        if st.button("⬅️ 이전", key="btn_prev_demo"):
            st.switch_page("pages/13_data_analysis_1_basic_info_2.py")
    with col3:
        if st.button("➡️ 다음", key="btn_next_demo"):
            st.session_state.subject = subject
            st.session_state.subject_saved = True
            st.switch_page("pages/15_data_analysis_3_data_input_2.py")

# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
