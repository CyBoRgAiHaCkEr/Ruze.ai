import streamlit as st
import numpy as np
import cv2
import av
import time
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. SYSTEM INITIALIZATION ---
st.set_page_config(page_title="RUZE.AI | DATA TERMINAL", layout="wide")

client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY"))
MAVERICK_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

# --- 2. MINIMALIST INDUSTRIAL CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #050505;
        color: #e0e0e0; /* Neutral grey for better long-form reading */
    }

    /* Clean Terminal Blocks */
    .terminal-block {
        border-left: 2px solid #00ffcc;
        padding: 20px;
        background: #0a0a0a;
        margin-bottom: 20px;
        font-size: 14px;
        line-height: 1.5;
    }

    .stCodeBlock { border: none !important; background-color: #000 !important; }
    
    /* Shrink Video to be less distracting */
    .stVideo { width: 60% !important; margin: auto; border: 1px solid #333; }
    
    h1 { color: #00ffcc; font-size: 1.2rem; letter-spacing: 3px; }
    b { color: #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

if "system_log" not in st.session_state:
    st.session_state.system_log = [f"[{time.strftime('%H:%M:%S')}] RUZE_OS_V4: READY"]

# --- 3. ANALYTICS ENGINE ---
def ruze_analyze(user_input):
    timestamp = time.strftime('%H:%M:%S')
    st.session_state.system_log.append(f"[{timestamp}] USER_QUERY >> {user_input}")
    try:
        resp = client.chat.completions.create(
            model=MAVERICK_MODEL,
            messages=[
                {"role": "system", "content": "You are RUZE.AI. You provide deep industrial engineering analysis for Ruzan Daruwalla. Avoid conversational fluff. Be technical, data-heavy, and precise."},
                {"role": "user", "content": user_input}
            ]
        )
        st.session_state.system_log.append(f"[{timestamp}] RUZE_ANALYSIS >> {resp.choices[0].message.content}")
    except:
        st.session_state.system_log.append(f"[{timestamp}] ERR >> UPLINK_FAILURE")

# --- 4. SENSOR FEED (NO HUD OVERLAY) ---
def simple_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 5. TEXT-PRIORITY LAYOUT ---
st.title("RUZE.AI // INDUSTRIAL DATA TERMINAL")

# Primary Info Card
st.markdown(f"""
<div class='terminal-block'>
    <b>OPERATOR:</b> RUZAN DARUWALLA<br>
    <b>PRIMARY_TASK:</b> INDUSTRIAL_OPTIMIZATION<br>
    <b>ACTIVE_MODEL:</b> LLAMA_4_MAVERICK_17B
</div>
""", unsafe_allow_html=True)

# Sensor Feed (Smaller, centered)
with st.expander("🎥 VISUAL SENSOR FEED (CLICK TO VIEW)", expanded=False):
    webrtc_streamer(
        key="minimal-stream",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=simple_callback,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    )

st.write("---")

# Data Log (Main focus)
st.write("**FULL SYSTEM LOG**")
# Display logs in reverse (newest at bottom)
for log in st.session_state.system_log:
    st.markdown(f"<div style='margin-bottom: 15px;'>{log}</div>", unsafe_allow_html=True)

# Fixed Input
if prompt := st.chat_input("ENTER PARAMETERS..."):
    ruze_analyze(prompt)
    st.rerun()
