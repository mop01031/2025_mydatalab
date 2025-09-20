import streamlit as st
from PIL import Image
from datetime import date as _date  # (선택) 날짜 파싱에 필요하면 유지


st.set_page_config(
    page_title="데이터분석 (1) 기본 정보 입력",
    page_icon="📊",
    layout="centered"
)
# ✅ 날짜 안전 변환 헬퍼 (문자열/None도 받아서 date로 보정)
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

# ✅ 예시 모드에서 돌아왔거나, 데모 위젯/데모 값이 남아있으면 모두 초기화
reset_needed = st.session_state.pop("came_from_demo", False) or any(
    k in st.session_state for k in (
        # demo 위젯 키
        "input_name_demo", "input_id_demo", "input_school_demo", "input_date_demo",
        # demo 값 키
        "demo_name", "demo_student_id", "demo_school", "demo_date",
    )
)
if reset_needed:
    for k in (
        # 실제 값 키
        "name", "student_id", "school", "date",
        # 일반 위젯 키
        "input_name", "input_id", "input_school", "input_date",
        # 데모 위젯 키
        "input_name_demo", "input_id_demo", "input_school_demo", "input_date_demo",
        # 데모 값 키
        "demo_name", "demo_student_id", "demo_school", "demo_date",
    ):
        st.session_state.pop(k, None)
    st.rerun()

# --- 기본 사이드바 숨기기 ---
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
# --- 예시 모드 안내 & 버튼 줄 ---
c1, c2 = st.columns(2, gap="small")
with c1:
    if st.button("🧪 예시 모드 보기", use_container_width=True, key="btn_demo_view"):
        st.session_state["demo_basic_active"] = True   # ← 예시 모드 진입 플래그
        st.switch_page("pages/13_data_analysis_1_basic_info_2.py")
with c2:
    if st.button("🚫 예시 모드 종료", use_container_width=True, key="btn_demo_exit"):
        # 필요시 입력 값/위젯 키 초기화
        for k in ("name","student_id","school","date",
                  "input_name","input_id","input_school","input_date",
                  "input_name_demo","input_id_demo","input_school_demo","input_date_demo",
                  "demo_basic_active","came_from_demo"):
            st.session_state.pop(k, None)
        st.rerun()

# --- 배너 이미지 ---
banner = Image.open("images/(8)title_basic_info.png")
st.image(banner, use_container_width=True)



# --- 입력 폼 ---
name = st.text_input("이름", value=st.session_state.get("name", ""), key="input_name")
student_id = st.text_input("학번", value=st.session_state.get("student_id", ""), key="input_id")
school = st.text_input("학교", value=st.session_state.get("school", ""), key="input_school")
date = st.date_input("날짜 선택", value=st.session_state.get("date"), key="input_date")

if st.button("✅ 저장하기"):
    if name and student_id and school:
        st.session_state.name = name
        st.session_state.student_id = student_id
        st.session_state.school = school
        st.session_state.date = str(date)
        st.success("✅ 정보가 저장되었습니다! 왼쪽 메뉴에서 다음 단계로 이동하세요.")
    else:
        st.warning("⚠️ 모든 항목을 입력해주세요.")

if "name" in st.session_state:
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

# --- 챗봇 마운트 ---
import chatdog_mount
chatdog_mount.mount()
