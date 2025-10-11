import streamlit as st
from reke_api import verify

# --- Streamlit Page Config ---
st.set_page_config(page_title="Reke Demo", page_icon="🛡️", layout="wide", initial_sidebar_state="collapsed")

# --- Styling for Clean, Modern UI (Inspired by remove.bg) ---
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9ff;
        }
        .main-header {
            text-align: center;
            color: #1e3a8a;
            font-size: 2.5em;
            margin-bottom: 0.5em;
            font-weight: bold;
        }
        .sub-header {
            text-align: center;
            color: #4b5563;
            font-size: 1.1em;
            margin-bottom: 2.5em;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .stButton > button {
            background-color: #1e3a8a;
            color: white;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-size: 1em;
            font-weight: 500;
            border: none;
            transition: background-color 0.3s ease;
            width: 100%;
            margin-top: 0.5em;
        }
        .stButton > button:hover {
            background-color: #1d4ed8;
        }
        .image-container {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 12px;
            background-color: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
            transition: box-shadow 0.3s ease;
        }
        .image-container:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }
        .result-box {
            background-color: white;
            border-radius: 12px;
            padding: 24px;
            margin-top: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-left: 4px solid #1e3a8a;
        }
        .status-ai { color: #ef4444; font-weight: bold; }
        .status-real { color: #10b981; font-weight: bold; }
        .confidence-bar {
            background-color: #e5e7eb;
            border-radius: 6px;
            height: 8px;
            margin-top: 4px;
        }
        .confidence-fill {
            height: 100%;
            border-radius: 6px;
            background-color: #10b981;
        }
    </style>
""", unsafe_allow_html=True)

# --- Header / Intro ---
st.markdown("""
    <div class="main-header">🛡️ Reke Demo</div>
    <div class="sub-header">Choose a sample image and verify with Reke's API whether it's real or AI-generated. See real-time detection in action.</div>
""", unsafe_allow_html=True)

# --- Sample Images ---
samples = {
    "AI Mode": "ai_mode.jpg",
    "AI Painter": "ai_painter.jpg",
    "AI Panda-Chimp": "ai_panda_chimp.jpg",
    "AI Woman": "ai_woman.jpg",
    "Real Cat": "real_cat.jpg",
    "Real Child": "real_child.jpg",
    "Real Dog": "real_dog.jpg",
    "Real Man": "real_man.jpg",
    "Real Woman": "real_woman.jpg"
}

cols = st.columns(3)
index = 0

# --- Display Images + Buttons ---
st.markdown('<div style="display: flex; justify-content: center; gap: 20px; flex-wrap: wrap;">', unsafe_allow_html=True)
for label, filename in samples.items():
    with cols[index % 3]:
        st.markdown(f'<div class="image-container">', unsafe_allow_html=True)
        image_path = f"sample_images/{filename}"
        st.image(image_path, caption=label, use_container_width=True)
        if st.button(f"🔍 Verify with Reke", key=filename):
            with st.spinner("Verifying..."):
                result = verify(filename)
                st.session_state["result"] = result
        st.markdown('</div>', unsafe_allow_html=True)
    index += 1
st.markdown('</div>', unsafe_allow_html=True)

# --- Display Results ---
if "result" in st.session_state:
    res = st.session_state["result"]
    st.markdown('<div class="result-box">', unsafe_allow_html=True)
    st.subheader("🔍 Verification Result")
    
    # Status with color
    status_class = "status-ai" if "AI-Generated" in res['status'] else "status-real"
    st.markdown(f'<p class="{status_class}">**Status:** {res["status"]}</p>', unsafe_allow_html=True)
    
    # Confidence with progress bar
    st.write(f"**Confidence:** {res['confidence'] * 100:.0f}%")
    st.markdown(f"""
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: {res['confidence'] * 100}%;"></div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write(f"**File:** {res['filename']}")
    st.markdown("**Metadata:**")
    st.json(res["metadata"])
    
    st.markdown("### 🧩 Example API Call")
    st.code(f"""
import requests

url = "https://api.reke-platform.com/verify"
headers = {{"X-API-Key": "YOUR_API_KEY"}}
files = {{"file": open("{res['filename']}", "rb")}}
response = requests.post(url, headers=headers, files=files)
print(response.json())
""", language="python")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer for Polish ---
st.markdown("---")
st.markdown('<div style="text-align: center; color: #6b7280; font-size: 0.9em;">Powered by Reke API | Demo for Investors</div>', unsafe_allow_html=True)
