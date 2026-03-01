import streamlit as st
import numpy as np
import cv2
import av
import time
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. OPTIMIZED CONFIG ---
st.set_page_config(page_title="RUZE.AI", layout="wide")

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY"))

MODELS = {
    "Llama 4 Maverick": "meta-llama/llama-4-maverick-17b-128e-instruct",
    "Llama 4 Scout": "meta-llama/llama-4-scout-17b-16e-instruct",
    "GPT OSS 120B": "openai/gpt-oss-120b"
}

# --- 2. ANTI-SQUISH CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Reset layout for mobile */
    .block-container { padding: 1rem 1rem !important; max-width: 100% !important; }
    
    html, body, [class*="st-"] {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #050505;
        color: #e0e0e0;
    }

    /* The Terminal Box: Forces text to wrap, not squish */
    .terminal-output {
        background: #000;
        border-left: 3px solid #00ffcc;
        padding: 15px;
        margin: 12px 0;
        font-size: 0.95rem;
        line-height: 1.6;
        /* Essential properties for mobile: */
        white-space: pre-wrap;       
        word-wrap: break-word;       
        overflow-wrap: anywhere;
    }

    .tag-blue { color: #00ffcc; font-weight: bold; }
    .tag-grey { color: #666; font-size: 0.8rem; }

    /* Hide the camera by default to save space */
    .stExpander { border: 1px solid #333 !important; background: #0a0a0a !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ANALYTICS ---
if "history" not in st.session_state:
    st.session_state.history = []

def run_engine(prompt):
    t = time.strftime('%H:%M')
    try:
        resp = client.chat.completions.create(
            model=MODELS[st.session_state.engine],
            messages=[{"role": "system", "content": "Industrial Intelligence Ruze.ai. Be technical."},
                      {"role": "user", "content": prompt}]
        )
        # Store as dict for clean rendering
        st.session_state.history.append({"time": t, "type": "USER", "content": prompt})
        st.session_state.history.append({"time": t, "type": st.session_state.engine, "content": resp.choices[0].message.content})
    except:
        st.error("SYSTEM LINK OFFLINE")

# --- 4. INTERFACE ---
with st.sidebar:
    st.image("logo.png", use_container_width=True)
    st.session_state.engine = st.selectbox("CORE ENGINE", list(MODELS.keys()))
    st.caption(f"Operator: Ruzan Daruwalla")
    if st.button("CLEAR LOG"):
        st.session_state.history = []
        st.rerun()

st.title(" RUZE.AI ")

# Camera - Tucked away so it doesn't squish text
with st.expander("🎥 OPEN VISUAL SENSOR"):
    webrtc_streamer(key="cam", mode=WebRtcMode.SENDRECV)

# The Main Text Stream (Reverse order so newest is at the top/bottom as per preference)
for entry in st.session_state.history:
    st.markdown(f"""
    <div class="terminal-output">
        <span class="tag-grey">[{entry['time']}]</span> 
        <span class="tag-blue">{entry['type']} >></span><br>
        {entry['content']}
    </div>
    """, unsafe_allow_html=True)

# Fixed input at bottom
if prompt := st.chat_input("ENTER COMMAND..."):
    run_engine(prompt)
    st.rerun()
