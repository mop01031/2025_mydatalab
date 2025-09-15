# pages/4_chatdogai.py
import streamlit as st
from pathlib import Path
import importlib.util

st.set_page_config(page_title="오른쪽 패널 챗봇", layout="wide")
st.title("오른쪽 패널 챗봇 스모크 테스트")
st.write("우하단 강아지 버튼을 눌러보세요!")

# 루트의 chatdog_mount.py 로드 (pages 밖에 있어서 동적 import)
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("chatdog_mount", str(ROOT / "chatdog_mount.py"))
chatdog_mount = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(chatdog_mount)

chatdog_mount.mount()  # ← 우하단 FAB + 패널 장착
