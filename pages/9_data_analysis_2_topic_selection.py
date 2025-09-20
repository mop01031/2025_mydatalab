import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="데이터분석 (2) 분석 주제 선택",
    page_icon="📊",
    layout="centered"
)
# ✅ 데모에서 돌아왔거나 데모 키가 남아있으면 초기화
reset_needed = st.session_state.pop("came_from_demo", False) or any(
    k in st.session_state for k in ("input_subject_demo", "demo_subject")
)
if reset_needed:
    for k in ("subject", "subject_saved", "input_subject",
              "input_subject_demo", "demo_subject"):
        st.session_state.pop(k, None)
    st.rerun()
# --- 기본 사이드바 숨기기 ---
hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)
# --- 상단: 예시 모드 버튼 줄 (배너 위) ---
c1, c2 = st.columns(2, gap="small")
with c1:
    if st.button("🧪 예시 모드 보기", use_container_width=True):
        # ✅ 예시 페이지가 기본 문구로 뜨도록 강제 플래그 설정 + 데모 키 비우기
        st.session_state["demo_force"] = True
        for k in ("input_subject_demo", "demo_subject"):
            st.session_state.pop(k, None)
        st.switch_page("pages/14_data_analysis_2_topic_selection(2).py")
with c2:
    if st.button("🚫 예시 모드 종료", use_container_width=True):
        # 현재 페이지 값 수동 초기화 후 새로고침
        for k in ("subject", "subject_saved", "input_subject",
                  "input_subject_demo", "demo_subject", "came_from_demo"):
            st.session_state.pop(k, None)
        st.rerun()
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

# --- 선행 단계 확인 ---
if "name" not in st.session_state:
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
    if st.button("✅ 주제 저장", use_container_width=True):
        if subject.strip():
            st.session_state.subject = subject
            st.session_state.subject_saved = True
        else:
            st.warning("⚠️ 주제를 입력해주세요.")

if st.session_state.get("subject_saved"):
    st.success("✅ 주제가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")

# --- 이전/다음 이동 ---
if "subject" in st.session_state:
    col1, col2, col3 = st.columns([3, 15, 3])
    with col1:
        if st.button("⬅️ 이전"):
            st.switch_page("pages/8_data_analysis_1_basic_info.py")
    with col3:
        if st.button("➡️ 다음"):
            st.switch_page("pages/10_data_analysis_3_data_input.py")

# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
