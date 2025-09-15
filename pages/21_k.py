import streamlit as st
from pathlib import Path
from PIL import Image
import importlib.util

st.set_page_config(
    page_title="경사하강법 (1) 최적화란?",
    page_icon="📖",
    layout="centered"
)


banner = Image.open("images/(2)title_optimization.png")  
st.image(banner, use_container_width=True)

col1, col2 = st.columns([14,3])  
with col2:
    if st.button("🏠 홈으로"):
        st.switch_page("app.py")    


st.markdown("""
### 🧠 최적화란?

- 최적화는 어떤 문제에서 **가장 좋은 결과(최댓값 또는 최솟값)를 찾는 과정**이에요.
- 예를 들어, 공부 시간에 따른 성적을 예측할 때,
  `가장 좋은 공부 시간`을 찾는 것도 일종의 최적화 문제입니다.

---

### 📉 경사하강법이란?

- 최적화 과정에서 사용하는 알고리즘 중 하나로,
  **기울기(경사)를 따라 조금씩 이동하면서 최소값을 찾아가는 방법**이에요.
- 함수의 기울기를 계산해서 **조금씩 이동하며 손실을 줄여가는 반복적인 방법**이죠.

---

### 💡 핵심 용어 정리

- **기울기(Gradient)**: 함수가 증가하거나 감소하는 방향과 속도
- **학습률(Learning Rate)**: 한 번에 이동하는 거리
- **반복 횟수(Epoch)**: 이 과정을 몇 번 반복할 것인지

""")


# 루트의 chatdog_mount.py 로드 (pages 밖에 있어서 동적 import)
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chatdog_mount", str(ROOT / "chatdog_mount.py"))
chatdog_mount = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(chatdog_mount)

chatdog_mount.mount()  # ← 우하단 FAB + 패널 장착