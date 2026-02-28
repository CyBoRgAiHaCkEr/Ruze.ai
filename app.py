import streamlit as st
import numpy as np
import cv2
import av
import time
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="RUZE.AI", layout="wide")

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY"))

# Model Dictionary for 2026
MODELS = {
    "Llama 4 Maverick (Flagship)": "meta-llama/llama-4-maverick-17b-128e-instruct",
    "Llama 4 Scout (Speed/Context)": "meta-llama/llama-4-scout-17b-16e-instruct",
    "GPT OSS 120B (Reasoning)": "openai/gpt-oss-120b"
}

# --- 2. ROBOTIC UI STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    html, body, [class*="st-"] { font-family: 'JetBrains Mono', monospace !important; background-color: #050505; color: #e0e0e0; }
    .stSelectbox label { color: #00ffcc !important; font-weight: bold; }
    .terminal-block { border-left: 2px solid #00ffcc; padding: 15px; background: #0a0a0a; margin-bottom: 20px; font-size: 14px; }
    b { color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: OPERATOR & MODEL SELECTOR ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.subheader("💎 RUZE.AI")
    
    st.markdown("---")
    st.write("**OPERATOR:** RUZAN DARUWALLA")
    
    # THE SWITCHER
    selected_label = st.selectbox("CORE ENGINE SELECT:", list(MODELS.keys()))
    ACTIVE_MODEL = MODELS[selected_label]
    
    st.info(f"STATUS: {selected_label.split(' ')[0]} ONLINE")
    st.markdown("---")

# --- 4. ANALYTICS LOGIC ---
if "system_log" not in st.session_state:
    st.session_state.system_log = [f"[{time.strftime('%H:%M:%S')}] RUZE_OS: INITIALIZED"]

def ruze_analyze(user_input):
    timestamp = time.strftime('%H:%M:%S')
    st.session_state.system_log.append(f"[{timestamp}] COMMAND >> {user_input}")
    try:
        resp = client.chat.completions.create(
            model=ACTIVE_MODEL,
            messages=[
                {"role": "system", "content": "You are RUZE.AI. Industrial Engineering Intelligence for Ruzan Daruwalla. Provide precise, technical, and data-driven analysis."},
                {"role": "user", "content": user_input}
            ]
        )
        st.session_state.system_log.append(f"[{timestamp}] {selected_label.upper()} >> {resp.choices[0].message.content}")
    except Exception as e:
        st.session_state.system_log.append(f"[{timestamp}] ERR >> ENGINE_LINK_FAILURE")

# --- 5. VISION & LAYOUT ---
st.title(" RUZE.AI")

with st.expander("", expanded=False):
    webrtc_streamer(
        key="multi-stream",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=lambda f: av.VideoFrame.from_ndarray(f.to_ndarray(format="bgr24"), format="bgr24"),
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    )

# Main Display
for log in st.session_state.system_log[-10:]:
    st.markdown(f"<div style='margin-bottom: 10px;'>{log}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("ENTER PARAMETERS..."):
    ruze_analyze(prompt)
    st.rerun()

