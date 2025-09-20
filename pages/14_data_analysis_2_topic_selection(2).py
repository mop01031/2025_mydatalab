# pages/14_data_analysis_2_topic_selection(2).py
import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="데이터분석 (2) 분석 주제 선택 - 예시 모드",
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

# --- 상단: 예시 모드 종료 (배너 위) ---
col_left, col_right = st.columns([3, 1])
with col_right:
    if st.button("🚫 예시 모드 종료", use_container_width=True, key="btn_exit_demo_topic"):
        st.switch_page("pages/13_data_analysis_1_basic_info(2).py")

# --- 배너 ---
banner = Image.open("images/(9)title_select_topic.png")
st.image(banner, use_container_width=True)

# --- 사이드바 (새 구조) ---
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
    st.page_link("pages/13_data_analysis_1_basic_info(2).py", label="(1) 기본 정보 입력 - 예시")
    st.page_link("pages/14_data_analysis_2_topic_selection(2).py", label="(2) 분석 주제 선택 - 예시")

# --- 선행 단계 확인 (원본과 동일 로직) ---
if "name" not in st.session_state:
    st.warning("이전 단계에서 데이터를 먼저 입력해 주세요.")
    st.stop()

# --- 기본 주제 (미리 작성된 상태) ---
DEFAULT_SUBJECT = " 우리나라 병상 수는 앞으로도 계속 늘어날까? "

# --- 주제 입력(예시값 기본) ---
subject = st.text_area(
    "📌 국가통계포털을 이용해 분석하고 싶은 데이터를 찾아보고, 주제를 작성하세요!",
    value=st.session_state.get("demo_subject", st.session_state.get("subject", DEFAULT_SUBJECT)),
    placeholder="예: 공부시간에 대한 성적 예측하기",
    key="input_subject_demo"   # 데모 전용 위젯 키
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
            st.session_state.subject = subject            # 실제 값에도 저장 (다음 단계 사용)
            st.session_state.demo_subject = subject       # 데모 기본값 유지
            st.session_state.subject_saved = True
        else:
            st.warning("⚠️ 주제를 입력해주세요.")

if st.session_state.get("subject_saved"):
    st.success("✅ 주제가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")

# --- 이전/다음 이동 (원본과 동일 UI) ---
if "subject" in st.session_state or subject.strip():
    # 주제가 비어있지 않으면 다음/이전 버튼 노출
    col1, col2, col3 = st.columns([3, 15, 3])
    with col1:
        if st.button("⬅️ 이전", key="btn_prev_demo"):
            # 데모 플로우에서는 이전을 예시 1단계로
            st.switch_page("pages/13_data_analysis_1_basic_info(2).py")
    with col3:
        if st.button("➡️ 다음", key="btn_next_demo"):
            # 저장 안 눌렀어도 값 반영 후 다음 단계로
            st.session_state.subject = subject if subject.strip() else DEFAULT_SUBJECT
            st.session_state.demo_subject = st.session_state.subject
            st.session_state.subject_saved = True
            st.switch_page("pages/10_data_analysis_3_data_input.py")

# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
