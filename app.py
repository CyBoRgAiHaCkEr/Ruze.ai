import streamlit as st
import numpy as np
import cv2
import av
import time
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# --- 1. CORE SYSTEM CONFIG ---
st.set_page_config(page_title="RUZE.AI | INDUSTRIAL INTELLIGENCE", layout="wide")

# Connection to Llama 4 Maverick
client = Groq(api_key=st.secrets.get("GROQ_API_KEY", "YOUR_KEY"))
MAVERICK_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

# --- 2. ROBOTIC UI STYLING (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* Force Robotic Monospaced Font */
    html, body, [class*="st-"], .stMarkdown {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: #050505;
        color: #00ffcc;
    }
    
    /* Sidebar Industrial Look */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #00ffcc;
    }

    /* Terminal Log Styling */
    .stCodeBlock { border: 1px solid #00ffcc !important; }
    
    /* Glow effect for Headers */
    h1, h2 {
        color: #fff;
        text-shadow: 0 0 12px #00ffcc;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR: LOGO & TELEMETRY ---
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.subheader("💎 RUZE.AI")
    
    st.markdown("---")
    st.markdown("### 📊 SYSTEM STATUS")
    st.write(f"**OPERATOR:** RUZAN DARUWALLA")
    st.write(f"**CORE:** MAVERICK v4.0")
    st.write(f"**STATUS:** <span style='color:#00ff88'>ADAPTIVE_ACTIVE</span>", unsafe_allow_html=True)
    st.write(f"**LATENCY:** 14ms")
    st.markdown("---")
    st.caption("Industrial Engineering Logic Engine")

# --- 4. LOGIC & DATA STREAM ---
if "system_log" not in st.session_state:
    st.session_state.system_log = [f"[{time.strftime('%H:%M:%S')}] RUZE.AI: UPLINK ESTABLISHED"]

def ruze_analyze(user_input):
    st.session_state.system_log.append(f"REQ>> {user_input.upper()}")
    try:
        resp = client.chat.completions.create(
            model=MAVERICK_MODEL,
            messages=[
                {"role": "system", "content": "You are RUZE.AI. You are an expert Industrial Engineering Intelligence. Your tone is robotic, technical, and precise. Assist Ruzan Daruwalla with intelligent, adaptive solutions."},
                {"role": "user", "content": user_input}
            ]
        )
        ans = resp.choices[0].message.content
        st.session_state.system_log.append(f"RES>> {ans}")
    except:
        st.session_state.system_log.append("ERR>> DATA_LINK_TIMEOUT")

# --- 5. VISION SYSTEM (ROBOTIC HUD) ---
def industrial_vision_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    h, w = img.shape[:2]
    
    # Scanning Line Effect
    scan_y = int(time.time() * 60) % h
    cv2.line(img, (0, scan_y), (w, scan_y), (0, 255, 204), 1)
    
    # Targeting Brackets
    color = (204, 255, 0) # Cyan in BGR
    l = 40
    # Corner markings
    cv2.line(img, (40, 40), (40+l, 40), color, 2)
    cv2.line(img, (40, 40), (40, 40+l), color, 2)
    cv2.line(img, (w-40, h-40), (w-40-l, h-40), color, 2)
    cv2.line(img, (w-40, h-40), (w-40, h-40-l), color, 2)
    
    return av.VideoFrame.from_ndarray(img, format="bgr24")

# --- 6. MAIN INTERFACE ---
st.title("🛡️ RUZE INDUSTRIAL HUD")

col_vid, col_log = st.columns([2, 1])

with col_vid:
    webrtc_streamer(
        key="industrial-stream",
        mode=WebRtcMode.SENDRECV,
        video_frame_callback=industrial_vision_callback,
        media_stream_constraints={"video": True, "audio": False},
        rtc_configuration=RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
    )

with col_log:
    st.write("**COMMAND STREAM**")
    for log in st.session_state.system_log[-8:]:
        st.code(log, language="bash")

if prompt := st.chat_input("ENTER SYSTEM COMMAND..."):
    ruze_analyze(prompt)
    st.rerun()
