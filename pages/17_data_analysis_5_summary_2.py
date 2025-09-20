# pages/17_data_analysis_5_summary_2.py
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import platform
import matplotlib.font_manager as fm
import matplotlib
import os
import numpy as np
from PIL import Image

st.set_page_config(
    page_title="데이터분석 (5) 요약 결과 - 예시 모드",
    page_icon="🧪",
    layout="centered"
)

# ------------------ 폰트 설정 ------------------
font_path = os.path.join("fonts", "NotoSansKR-Regular.ttf")
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    matplotlib.rcParams["font.family"] = font_prop.get_name()
else:
    if platform.system() == "Darwin":
        matplotlib.rcParams["font.family"] = "AppleGothic"
    elif platform.system() == "Windows":
        matplotlib.rcParams["font.family"] = "Malgun Gothic"
    else:
        matplotlib.rcParams["font.family"] = "DejaVu Sans"
    font_prop = None
matplotlib.rcParams["axes.unicode_minus"] = False

# ------------------ 기본 사이드바 숨기기 + 인쇄 최적화 CSS ------------------
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], .main, .block-container {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
        }
        [data-testid="stVerticalBlock"] { overflow: visible !important; }
        .stButton button { margin-top: 12px; }
        @media print {
            html, body {
                height: auto !important; overflow: visible !important;
                margin: 0 !important; padding: 0 !important; zoom: 85%;
            }
            .element-container { page-break-inside: avoid; break-inside: avoid; }
            .stButton, .stSidebar { display: none !important; }
            .main { padding: 0 !important; }
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] { display: none; }
    </style>
""", unsafe_allow_html=True)

# --- 상단: 예시 모드 종료 ---
col_left, col_right = st.columns([3, 1])
with col_right:
    if st.button("🚫 예시 모드 종료", use_container_width=True, key="btn_exit_demo_summary"):
        # 일반 모드 초기화를 트리거
        st.session_state["came_from_demo"] = True
        # 데모 관련 키 모두 정리
        for k in (
            "demo_active","demo_subject","input_subject_demo",
            "demo_x_label","demo_y_label","demo_table_data",
            "demo_x_values","demo_y_values","demo_analysis_text",
            "demo_lr_value","demo_epochs_value","demo_predict_requested",
            "demo_attempt_count","demo_history","demo_selected_model_indices",
            "demo_predict_summary","demo_next_x"
        ):
            st.session_state.pop(k, None)
        st.switch_page("pages/8_data_analysis_1_basic_info.py")

# ------------------ 배너 ------------------
banner = Image.open("images/(12)title_summary_result.png")
st.image(banner, use_container_width=True)

# ------------------ 챗봇 마운트 ------------------
import chatdog_mount
chatdog_mount.mount()

# ------------------ 사이드바(예시 모드 네비) ------------------
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
    st.page_link("pages/16_data_analysis_4_prediction_2.py", label="(4) 예측 실행")
    st.page_link("pages/17_data_analysis_5_summary_2.py", label="(5) 요약 결과")

# ------------------ 상단 요약(이름/학번/학교/날짜) ------------------
with st.container():
    info_data = {
        "이름": st.session_state.get("name", "정보 없음"),
        "학번": st.session_state.get("student_id", "정보 없음"),
        "학교": st.session_state.get("school", "정보 없음"),
        "날짜": st.session_state.get("date", "정보 없음"),
    }
    cols = st.columns(4)
    for i, (label, value) in enumerate(info_data.items()):
        with cols[i]:
            st.markdown(f"""
            <div style='background-color: #f3f4f6; padding: 12px 15px; border-radius: 8px;
                        font-size: 15px; color: #1f2937;'>
                <div style='font-weight: 700; font-size: 16px;'>{label}</div>
                <div style='margin-top: 5px; font-size: 15px;'>{value}</div>
            </div>
            """, unsafe_allow_html=True)

# ------------------ 선택 주제 ------------------
with st.container():
    st.markdown("### 🔵 선택한 분석 주제")
    subject = st.session_state.get('demo_subject', '정보 없음')  # ✅ 데모 키 우선
    st.markdown(f"""
    <div style='background-color: #f3f4f6; color: #111827;
                padding: 15px 20px; border-radius: 10px;
                font-size: 17px; margin-top: 8px; margin-bottom: 0px;'>
        \U0001F4CC <strong>주제:</strong> {subject}
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ------------------ 산점도 & 분석 텍스트 (demo_*만 사용) ------------------
if 'demo_x_values' in st.session_state and 'demo_y_values' in st.session_state:
    st.markdown("### 🟣 산점도 그래프 & 분석 내용")
    col1, col2 = st.columns([3, 2])

    with col1:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        ax.scatter(st.session_state.demo_x_values, st.session_state.demo_y_values, color='blue')
        if font_prop:
            ax.set_xlabel(st.session_state.get("demo_x_label", "x"), fontproperties=font_prop)
            ax.set_ylabel(st.session_state.get("demo_y_label", "y"), fontproperties=font_prop)
        else:
            ax.set_xlabel(st.session_state.get("demo_x_label", "x"))
            ax.set_ylabel(st.session_state.get("demo_y_label", "y"))
        st.pyplot(fig)

    with col2:
        if 'demo_analysis_text' in st.session_state:
            st.markdown(f"""
            <div style='background-color: #f9fafb; padding: 18px 20px; border-radius: 10px;
                        font-size: 16px; line-height: 1.6; color: #111827;
                        border: 1px solid #e5e7eb;margin-top: 32px;'>
                <div style='font-weight: 600; font-size: 18px; margin-bottom: 10px;'>✏️ 분석 내용</div>
                {st.session_state.demo_analysis_text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("분석 내용이 없습니다.")
else:
    st.info("산점도 데이터가 없습니다. (15번 페이지에서 데이터를 저장하고 산점도를 확인하세요.)")

st.divider()

# ------------------ 최종 예측 요약(히스토리 기반, demo_*만 사용) ------------------
with st.container():
    st.markdown("### 🟢 최종 예측 요약")

    if 'demo_history' in st.session_state and st.session_state.get('demo_selected_model_indices'):
        final_idx = st.session_state.demo_selected_model_indices[-1]
        model = st.session_state.demo_history[final_idx]

        # 정확도 계산 (12와 동일 컨셉)
        y_true = np.array(st.session_state.get('demo_y_values', []))
        y_fit = np.array(model.get('y_pred', []))
        if len(y_true) > 0 and len(y_fit) >= len(y_true):
            y_pred = y_fit[-len(y_true):]
            ss_total = np.sum((y_true - np.mean(y_true))**2)
            ss_res = np.sum((y_true - y_pred)**2)
            accuracy = model.get("accuracy", round((1 - ss_res / ss_total) * 100, 2))
        else:
            accuracy = model.get("accuracy", None)

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown("#### 📈 예측 결과 그래프")
            fig, ax = plt.subplots(figsize=(6, 4))
            xv = st.session_state.get("demo_x_values", [])
            yv = st.session_state.get("demo_y_values", [])
            ax.scatter(xv, yv, label="입력 데이터", color="blue")
            ax.plot(model.get("x_plot", []), model.get("y_pred", []), label="예측 선", color="red")
            if font_prop:
                ax.set_xlabel(st.session_state.get("demo_x_label", "x"), fontproperties=font_prop)
                ax.set_ylabel(st.session_state.get("demo_y_label", "y"), fontproperties=font_prop)
            else:
                ax.set_xlabel(st.session_state.get("demo_x_label", "x"))
                ax.set_ylabel(st.session_state.get("demo_y_label", "y"))
            ax.legend()
            st.pyplot(fig)

        theme = st.get_option("theme.base")
        text_color = "#111827" if theme == "light" else "#f9fafb"

        with col2:
            acc_color = "red" if (accuracy is not None and accuracy >= 90) else "gray"
            acc_weight = "bold" if (accuracy is not None and accuracy >= 90) else "normal"

            st.markdown(f"""
            <div style="margin-top: 80px; line-height: 1.8; font-size: 18px; color:{text_color};">
                <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">🧮 예측 수식</div>
                <div style="font-size: 18px; margin-bottom: 16px;">{model.get('label','(수식 정보 없음)')}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""<span style="font-size: 18px;font-weight: bold;">🔍 <strong>예측 시도 횟수:</strong> {model.get('attempt_count','-')}회</span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size: 18px;font-weight: bold;">📘 <strong>학습률:</strong> {model.get('lr','-')}</span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size: 18px;font-weight: bold;">🔁 <strong>반복 횟수:</strong> {model.get('epoch','-')}</span>""", unsafe_allow_html=True)

            if accuracy is not None:
                st.markdown(f"""
                    <span style="font-size: 18px;">
                    🎯 <strong>정확도:</strong>
                    <span style="color:{acc_color}; font-weight:{acc_weight};">{accuracy:.2f}%</span>
                    </span>
                """, unsafe_allow_html=True)
            else:
                st.markdown("🎯 정확도: -")

    else:
        st.info("최종 예측 정보가 없습니다. (16번 페이지에서 예측 실행을 완료하세요.)")

    # 예측 결과 해석(텍스트) → demo_* 사용
    theme = st.get_option("theme.base")
    if theme == "dark":
        summary_bg = "#374151"; summary_border = "#6b7280"; summary_text = "#f9fafb"
    else:
        summary_bg = "#fefce8"; summary_border = "#fde68a"; summary_text = "#111827"

    if 'demo_predict_summary' in st.session_state:
        st.markdown(f"""
        <div style='background-color: {summary_bg}; padding: 18px 20px; border-radius: 10px;
                    border: 1px solid {summary_border}; margin-top: 20px; color: {summary_text};'>
            <div style='font-weight: 600; font-size: 17px;'>✏️ 예측 결과 해석</div>
            <div>{st.session_state.demo_predict_summary}</div>
        </div>
        """, unsafe_allow_html=True)

# ------------------ PDF로 저장 ------------------
st.markdown("""
    <style>
        @media print { .no-print { display: none !important; } }
    </style>
    <div class="no-print" style="margin-top: 40px; display: flex; justify-content: flex-start;">
        <form>
            <input type="submit" value="📄 PDF로 저장하기" formaction="javascript:window.print()" style="
                background-color: #93c5fd;
                color: black;
                padding: 12px 24px;
                font-size: 16px;
                border: 1px solid #111;
                border-radius: 8px;
                cursor: pointer;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
                font-weight: bold;
            ">
        </form>
    </div>
""", unsafe_allow_html=True)
