import streamlit as st
import numpy as np
import cv2
import av
import time
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- SYSTEM CONFIGURATION ---
st.set_page_config(page_title="RUZE.AI | INDUSTRIAL INTELLIGENCE", layout="wide")

# Groq Llama 4 Maverick
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY"))
MAVERICK_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

# --- ROBOTIC / INDUSTRIAL INTERFACE STYLING ---
st.markdown("""
    <style>
    /* Global Robotic Font */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    html, body, [class*="st-"] {
        font-family: 'JetBrains Mono', 'Courier New', monospace !important;
        background-color: #0d0d0d;
        color: #00ffcc;
    }

    .main { background-color: #0d0d0d; }
    
    /* Industrial Data Cards */
    .data-card { 
        border: 1px solid #00ffcc; 
        padding: 12px; 
        background: rgba(0, 255, 204, 0.05); 
        border-left: 5px solid #00ffcc;
        margin-bottom: 10px;
    }

    /* Terminal-style input */
    .stChatInputContainer {
        border: 1px solid #00ffcc !important;
        background-color: #000 !important;
    }
    
    /* Header styling */
    h1, h2, h3 {
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #fff;
        text-shadow: 0 0 10px #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

if "system_log" not in st.session_state:
    st.session_state.system_log = [f"[{time.strftime('%H:%M:%S')}] RUZE.AI INIT: RUZAN DARUWALLA AUTHENTICATED"]

# --- INTELLIGENT ADAPTIVE ANALYSIS ---
def ruze_analyze(user_input):
    st.session_state.system_log.append(f"SYS_IN>> {user_input.upper()}")
    try:
        resp = client.chat.completions.create(
            model=MAVERICK_MODEL,
            messages=[
                {"role": "system", "content": "You are RUZE.AI. Your voice is robotic, precise, and highly intelligent. You assist Ruzan Daruwalla in Industrial Engineering. Use data-driven language and adaptive logic."},
                {"role": "user", "content": user_input}
            ]
        )
        ans = resp.choices[0].message.content
        st.session_state.system_log.append(f"SYS_OUT>> {ans}")
    except:
        st.session_state.system_log.append("SYS_ERR>> DATA LINK SEVERED")

# --- ROBOTIC VISION OVERLAY ---
def industrial_vision_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    h, w = img.shape[:2]
    
    # Robotic Scanning Lines
    color = (204, 255, 0) # Cyan-Green (BGR)
    cv2.line(img, (0, int(time.time() * 50) % h), (w, int(time.time() * 50) % h), (0, 255, 204), 1)
    
    # Angular Brackets (Robotic Target)
    length = 40
    thickness = 2
    # Top Left
    cv2.line(img, (30, 30), (30+length, 30), color, thickness)
    cv2.line(img, (30, 30), (30, 30+length), color, thickness)
    # Bottom Right
    cv2.line(img, (w-30, h-30), (w-30-length, h-30), color, thickness)
    cv2.line(img, (w-30, h-30), (w-30, h-30-length), color, thickness)
    
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- INTERFACE ---
st.title("⚙️ RUZE.AI | MAVERICK v4.0")

col1, col2 = st.columns([2, 1])

with col1:
    webrtc_streamer(
        key="industrial-stream",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=industrial_vision_callback,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    )

with col2:
    st.markdown("<div class='data-card'><b>OPERATOR:</b> RUZAN DARUWALLA<br><b>DEPT:</b> INDUSTRIAL ENGINEERING<br><b>STATUS:</b> ADAPTIVE MODE ACTIVE</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.write("**COMMAND STREAM**")
    for log in st.session_state.system_log[-6:]:
        st.code(log, language="bash")

if prompt := st.chat_input("ENTER COMMAND..."):
    ruze_analyze(prompt)
    st.rerun()
