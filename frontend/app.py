import streamlit as st
import requests
import cv2
import numpy as np

st.set_page_config(page_title="Helmet Detection", layout="wide")

# ================================
# CUSTOM STYLING (ANIMASI + GLASS)
# ================================
st.markdown("""
<style>

body {
    background-color: #0f0f0f !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top, #181818 0%, #0f0f0f 70%);
    color: white;
    animation: fadeIn 1s ease-in-out;
}

/* Fade-in */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* Title */
h1 {
    text-align: center;
    font-size: 3rem !important;
    font-weight: 800;
    padding-bottom: 0.3rem;
    background: linear-gradient(90deg, #00f2ff, #b700ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-top: -20px;
}

/* VIDEO WRAPPER */
.video-wrapper {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

/* Video box */
.video-box {
    background: rgba(255,255,255,0.03);
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.1);
    padding: 10px;
    width: 70%; /* bigger */
    margin: auto;
    box-shadow: inset 0 0 40px rgba(0,255,255,0.08);
    transition: 0.3s ease;
}

.video-box:hover {
    box-shadow: inset 0 0 50px rgba(0,255,255,0.15);
}

/* Toggle Button */
.toggle-btn {
    background: linear-gradient(135deg, #1a1a1a, #262626);
    border: 1px solid rgba(255,255,255,0.2);
    padding: 0.9rem 2.2rem;
    font-size: 1.2rem;
    border-radius: 14px;
    text-align: center;
    margin: auto;
    display: block;
    transition: 0.25s ease-in-out;
}

.toggle-btn:hover {
    background: linear-gradient(135deg, #00eaff, #9a00ff);
    box-shadow: 0 0 20px rgba(0,255,255,0.4);
    transform: scale(1.05);
    cursor: pointer;
}

.status-text {
    text-align: center;
    font-size: 1.2rem;
    color: #aaa;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# ================================
# TITLE
# ================================
st.markdown("<h1>🪖</h1>", unsafe_allow_html=True)


# URL BACKEND
BACKEND_VIDEO_URL = "http://localhost:8000/video"


# STATE
if "run" not in st.session_state:
    st.session_state.run = False


# ================================
# VIDEO DISPLAY (CENTERED)
# ================================
st.markdown("<div class='video-wrapper'>", unsafe_allow_html=True)
st.markdown("<div class='video-box'>", unsafe_allow_html=True)

FRAME_WINDOW = st.image([])

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)


# ================================
# TOGGLE BUTTON (START / STOP)
# ================================
button_label = "⏹ Stop Detection" if st.session_state.run else "▶ Start Detection"

if st.button(button_label, key="toggle", help="Start/Stop webcam detection", args=None):
    st.session_state.run = not st.session_state.run


status = "🟢 Running" if st.session_state.run else "🔴 Stopped"
st.markdown(f"<p class='status-text'>{status}</p>", unsafe_allow_html=True)


# ================================
# STREAM READER
# ================================
def read_mjpeg_stream(url):
    stream = requests.get(url, stream=True)
    buff = bytes()
    for chunk in stream.iter_content(chunk_size=1024):
        buff += chunk
        a = buff.find(b'\xff\xd8')
        b = buff.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = buff[a:b+2]
            buff = buff[b+2:]
            frame = cv2.imdecode(np.frombuffer(jpg, np.uint8), cv2.IMREAD_COLOR)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yield frame


# ================================
# RENDER STREAM
# ================================
if st.session_state.run:
    for frame in read_mjpeg_stream(BACKEND_VIDEO_URL):
        FRAME_WINDOW.image(frame)
else:
    FRAME_WINDOW.markdown(
        "<p style='text-align:center;color:#777;'>Start Detection untuk menampilkan feed webcam.</p>",
        unsafe_allow_html=True
    )
