# chatdog_mount.py
import streamlit as st
from chatdog_global import mount_chatdog

def mount():
    API_URL = st.secrets.get("chatdog_api_url", "http://127.0.0.1:8503/chatdog")
    API_URL = (API_URL or "").strip()  # ← 혹시 모를 공백/개행 제거

    mount_chatdog(
        dog_image="images/chatdog_with_balloon.png",
        api_url=API_URL,               
        model="gpt-3.5-turbo",         
        temperature=0.6,
        max_tokens=600,
        fab_size_px=250,
        fab_right_px=20, fab_bottom_px=10,
        panel_width_css="clamp(720px, 50vw, 920px)",
        panel_top_css="10dvh",
        panel_height_css="70dvh",
    )
