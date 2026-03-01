import streamlit as st
import numpy as np
import cv2
import av
import time
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="RUZE.AI | INDUSTRIAL TERMINAL", layout="wide")

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY"))

MODELS = {
    "Llama 4 Maverick": "meta-llama/llama-4-maverick-17b-128e-instruct",
    "Llama 4 Scout": "meta-llama/llama-4-scout-17b-16e-instruct",
    "GPT OSS 120B": "openai/gpt-oss-120b"
}

# --- 2. ENHANCED TERMINAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Base robotic theme */
    html, body, [class*="st-"] {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #050505;
        color: #e0e0e0;
    }

    /* Enhanced Codebox / Terminal Container */
    .terminal-container {
        background-color: #000000;
        border: 1px solid #1a1a1a;
        border-left: 4px solid #00ffcc;
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
        /* Critical for no squishing: */
        white-space: pre-wrap;       
        word-wrap: break-word;       
        font-size: 0.9rem;
        color: #00ffcc;
        box-shadow: inset 0 0 10px rgba(0, 255, 204, 0.05);
    }

    .log-timestamp { color: #555; font-size: 0.75rem; margin-right: 8px; }
    .log-tag { color: #fff; font-weight: bold; margin-right: 5px; }
    
    /* Clean Video Container */
    .stVideo { border-radius: 8px; border: 1px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIC ---
if "system_log" not in st.session_state:
    st.session_state.system_log = [{"tag": "SYS", "msg": "RUZE_OS LOADED", "time": time.strftime('%H:%M:%S')}]

def ruze_analyze(user_input):
    t = time.strftime('%H:%M:%S')
    st.session_state.system_log.append({"tag": "REQ", "msg": user_input, "time": t})
    try:
        resp = client.chat.completions.create(
            model=MODELS[st.session_state.active_engine],
            messages=[
                {"role": "system", "content": "You are RUZE.AI, an expert Industrial Engineering Intelligence. Ruzan Daruwalla is the operator. Be technical and precise."},
                {"role": "user", "content": user_input}
            ]
        )
        st.session_state.system_log.append({"tag": "RES", "msg": resp.choices[0].message.content, "time": t})
    except:
        st.session_state.system_log.append({"tag": "ERR", "msg": "LINK_FAILED", "time": t})

# --- 4. SIDEBAR ---
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.write("---")
    st.session_state.active_engine = st.selectbox("ENGINE SELECT", list(MODELS.keys()))
    st.markdown(f"**OPERATOR:** RUZAN DARUWALLA")
    st.markdown(f"**STATUS:** <span style='color:#00ff88'>SYNCED</span>", unsafe_allow_html=True)

# --- 5. MAIN DISPLAY ---
st.title(" RUZE.AI")

# Optional Video Expander
with st.expander("VISUAL FEED", expanded=False):
    webrtc_streamer(
        key="industrial-stream",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    )

# The Better Codebox Interface
for item in st.session_state.system_log[-10:]:
    st.markdown(f"""
    <div class="terminal-container">
        <span class="log-timestamp">[{item['time']}]</span>
        <span class="log-tag">{item['tag']} >></span>
        {item['msg']}
    </div>
    """, unsafe_allow_html=True)

if prompt := st.chat_input("ENTER COMMAND..."):
    ruze_analyze(prompt)
    st.rerun()
