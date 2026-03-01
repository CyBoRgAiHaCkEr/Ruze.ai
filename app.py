import streamlit as st
import numpy as np
import cv2
import av
import time
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. CONFIGURATION & STATE INITIALIZATION ---
st.set_page_config(page_title="RUZE.AI ", layout="wide")

# Initialize Session State "Vault" to prevent forgetting
if "history" not in st.session_state:
    st.session_state.history = []
if "active_engine" not in st.session_state:
    st.session_state.active_engine = "Llama 4 Maverick"
if "operator" not in st.session_state:
    st.session_state.operator = "Ruzan Daruwalla"

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY"))

MODELS = {
    "Llama 4 Maverick": "meta-llama/llama-4-maverick-17b-128e-instruct",
    "Llama 4 Scout": "meta-llama/llama-4-scout-17b-16e-instruct",
    "GPT OSS 120B": "openai/gpt-oss-120b"
}

# --- 2. FLUID TERMINAL CSS (NO SQUISHING) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {{
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #050505;
        color: #e0e0e0;
    }}

    .terminal-entry {{
        background: #000;
        border-left: 4px solid #00ffcc;
        padding: 18px;
        margin: 15px 0;
        white-space: pre-wrap;       
        word-wrap: break-word;       
        font-size: 1rem;
        line-height: 1.6;
    }}

    .meta {{ color: #555; font-size: 0.8rem; margin-bottom: 5px; }}
    .source {{ color: #00ffcc; font-weight: bold; text-transform: uppercase; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. ANALYTICS ENGINE ---
def run_analysis(user_input):
    # Save user input immediately
    t = time.strftime('%H:%M:%S')
    st.session_state.history.append({"time": t, "source": st.session_state.operator, "content": user_input})
    
    try:
        resp = client.chat.completions.create(
            model=MODELS[st.session_state.active_engine],
            messages=[
                {"role": "system", "content": "You are RUZE.AI. Robotic, intelligent Industrial Engineering assistant for Ruzan Daruwalla."},
                {"role": "user", "content": user_input}
            ]
        )
        # Save AI response immediately
        st.session_state.history.append({"time": t, "source": st.session_state.active_engine, "content": resp.choices[0].message.content})
    except:
        st.session_state.history.append({"time": t, "source": "SYSTEM", "content": "CRITICAL: UPLINK FAILED"})

# --- 4. SIDEBAR (CONTROLS) ---
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.markdown("---")
    # Link selectbox directly to session state
    st.session_state.active_engine = st.selectbox("CORE ENGINE", list(MODELS.keys()), index=list(MODELS.keys()).index(st.session_state.active_engine))
    
    if st.button("♻️ RESET TERMINAL"):
        st.session_state.history = []
        st.rerun()

# --- 5. MAIN DISPLAY ---
st.title(" RUZE Ai")

with st.expander("🎥 SENSOR FEED"):
    webrtc_streamer(key="industrial-cam", mode=WebRtcMode.SENDRECV)

# Render history from memory
for entry in st.session_state.history:
    st.markdown(f"""
    <div class="terminal-entry">
        <div class="meta">[{entry['time']}] <span class="source">{entry['source']}</span></div>
        {entry['content']}
    </div>
    """, unsafe_allow_html=True)

# Command Input
if prompt := st.chat_input("ENTER ENGINEERING PARAMETERS..."):
    run_analysis(prompt)
    st.rerun()
