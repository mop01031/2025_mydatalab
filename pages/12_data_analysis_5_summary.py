import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator, ScalarFormatter, FormatStrFormatter
import platform
import matplotlib.font_manager as fm
import matplotlib
import os
import numpy as np
from PIL import Image


st.set_page_config(
    page_title="데이터분석 (6) 요약 결과",
    page_icon="📊",
    layout="centered"
)

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

st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"], .main, .block-container {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
        }

        [data-testid="stVerticalBlock"] {
            overflow: visible !important;
        }

        .stButton button {
            margin-top: 12px;
        }

        /* ✅ 페이지 인쇄 시 최적화 설정 */
        @media print {
            html, body {
                height: auto !important;
                overflow: visible !important;
                margin: 0 !important;
                padding: 0 !important;
                zoom: 85%;  /* ✅ 한 페이지에 맞추기 위한 축소 */
            }

            .element-container {
                page-break-inside: avoid;
                break-inside: avoid;
            }

            .stButton, .stSidebar {
                display: none !important;  /* 버튼, 사이드바 숨김 */
            }

            .main {
                padding: 0 !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

hide_default_sidebar = """
    <style>
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
"""
st.markdown(hide_default_sidebar, unsafe_allow_html=True)
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

banner = Image.open("images/(12)title_summary_result.png")  
st.image(banner, use_container_width=True)

import chatdog_mount
chatdog_mount.mount()

with st.container():
    info_data = {
        "이름": st.session_state.get("name", "정보 없음"),
        "학번": st.session_state.get("student_id", "정보 없음"),
        "학교": st.session_state.get("school", "정보 없음"),
        "날짜": st.session_state.get("date", "정보 없음")
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

with st.container():
    st.markdown("### 🔵 선택한 분석 주제")
    subject = st.session_state.get('subject', '정보 없음')
    st.markdown(f"""
    <div style='background-color: #f3f4f6; color: #111827;
                padding: 15px 20px; border-radius: 10px;
                font-size: 17px; margin-top: 8px; margin-bottom: 0px;'>
        \U0001F4CC <strong>주제:</strong> {subject}
    </div>
    """, unsafe_allow_html=True)

st.divider()

if 'x_values' in st.session_state and 'y_values' in st.session_state:
    st.markdown("### 🟣 산점도 그래프 & 분석 내용")

    col1, col2 = st.columns([3, 2])  


    with col1:
        fig, ax = plt.subplots(figsize=(5.5, 4))
        ax.scatter(st.session_state.x_values, st.session_state.y_values, color='blue')
        if font_prop:
            ax.set_xlabel(st.session_state.get("x_label", "x"), fontproperties=font_prop)
            ax.set_ylabel(st.session_state.get("y_label", "y"), fontproperties=font_prop)
        else:
            ax.set_xlabel(st.session_state.get("x_label", "x"))
            ax.set_ylabel(st.session_state.get("y_label", "y"))
        st.pyplot(fig)


    with col2:
        if 'analysis_text' in st.session_state:
            st.markdown(f"""
            <div style='background-color: #f9fafb; padding: 18px 20px; border-radius: 10px;
                        font-size: 16px; line-height: 1.6; color: #111827;
                        border: 1px solid #e5e7eb;margin-top: 32px;'>
                <div style='font-weight: 600; font-size: 18px; margin-bottom: 10px;'>✏️ 분석 내용</div>
                {st.session_state.analysis_text}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("분석 내용이 없습니다.")

st.divider()
with st.container():
    st.markdown("### 🟢 최종 예측 요약")

    if 'history' in st.session_state and 'selected_model_indices' in st.session_state:
        final_idx = st.session_state.selected_model_indices[-1]
        model = st.session_state.history[final_idx]

      
        y_true = np.array(st.session_state.y_values)
        y_pred = np.array(model['y_pred'][-len(y_true):])
        ss_total = np.sum((y_true - np.mean(y_true))**2)
        ss_res = np.sum((y_true - y_pred)**2)
        accuracy = model.get("accuracy", round((1 - ss_res / ss_total) * 100, 2))

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown("#### 📈 예측 결과 그래프")
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.scatter(st.session_state.x_values, st.session_state.y_values, label="입력 데이터", color="blue")
            ax.plot(model["x_plot"], model["y_pred"], label="예측 선", color="red")
            if font_prop:
                ax.set_xlabel(st.session_state.get("x_label", "x"), fontproperties=font_prop)
                ax.set_ylabel(st.session_state.get("y_label", "y"), fontproperties=font_prop)
            else:
                ax.set_xlabel(st.session_state.get("x_label", "x"))
                ax.set_ylabel(st.session_state.get("y_label", "y"))
            ax.legend()
            st.pyplot(fig)
        theme = st.get_option("theme.base")
        text_color ="#111827" if theme == "light" else "#f9fafb"
        with col2:
            theme = st.get_option("theme.base")
            text_color = "#111827" if theme == "light" else "#f9fafb"

            acc_color = "red" if accuracy >= 90 else "gray"
            acc_weight = "bold" if accuracy >= 90 else "normal"

            
            st.markdown(f"""
            <div style="margin-top: 80px; line-height: 1.8; font-size: 18px;">
                <div style="font-size: 18px; font-weight: bold; margin-bottom: 10px;">
                    🧮 예측 수식
                </div>
                <div style="font-size: 18px; margin-bottom: 16px;">
                    {model['label']}
                </div>
            </div>
            """, unsafe_allow_html=True)



            st.markdown(f"""<span style="font-size: 18px;font-weight: bold;">🔍 <strong>예측 시도 횟수:</strong> {model['attempt_count']}회</span>""", unsafe_allow_html=True)

            st.markdown(f"""<span style="font-size: 18px;font-weight: bold;">📘 <strong>학습률:</strong> {model['lr']}</span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size: 18px;font-weight: bold;">🔁 <strong>반복 횟수:</strong> {model['epoch']}</span>""", unsafe_allow_html=True)
            st.markdown(f"""
                <span style="font-size: 18px;">
                🎯 <strong>정확도:</strong>
                <span style="color:{acc_color}; font-weight:{acc_weight};">{accuracy:.2f}%</span>
                </span>
            """, unsafe_allow_html=True)


    else:
        st.info("최종 예측 정보가 없습니다.")
    theme = st.get_option("theme.base")

    if theme == "dark":
        summary_bg = "#374151"        
        summary_border = "#6b7280"    
        summary_text = "#f9fafb"      
    else:
        summary_bg = "#fefce8"        
        summary_border = "#fde68a"
        summary_text = "#111827"
    if 'predict_summary' in st.session_state:
        st.markdown(f"""
        <div style='background-color: {summary_bg}; padding: 18px 20px; border-radius: 10px;
                    border: 1px solid {summary_border}; margin-top: 20px; color: {summary_text};'>
            <div style='font-weight: 600; font-size: 17px;'>✏️ 예측 결과 해석</div>
            <div>{st.session_state.predict_summary}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
    <style>
        @media print {
            .no-print { display: none !important; }
        }
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

