# app.py
import streamlit as st
from reke_api import verify

st.set_page_config(page_title="Reke Demo", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1 {
    text-align: center;
    font-weight: 700;
}
.sample-thumb {
    border-radius: 10px;
    cursor: pointer;
    transition: 0.3s;
}
.sample-thumb:hover {
    transform: scale(1.05);
}
.result-box {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.markdown("# 🛡️ Reke AI Verification Demo")
st.write("**Select an image below to test the Reke API.** The system detects Tree-Ring watermarks to verify if content is AI-generated or real.")

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

# Thumbnails section
cols = st.columns(5)
selected_image = st.session_state.get("selected_image")

for i, (label, filename) in enumerate(samples.items()):
    with cols[i % 5]:
        if st.button(label, key=filename):
            st.session_state["selected_image"] = filename
            st.session_state["selected_label"] = label

# Center Display
st.markdown("---")

if "selected_image" in st.session_state:
    filename = st.session_state["selected_image"]
    st.image(f"sample_images/{filename}", caption=st.session_state["selected_label"], use_container_width=True)
    if st.button("🔍 Verify"):
        result = verify(filename)
        st.session_state["result"] = result

if "result" in st.session_state:
    res = st.session_state["result"]
    st.markdown("---")
    st.markdown("### ✅ Verification Result")
    st.markdown(f"<div class='result-box'><b>{res['status']}</b><br>Confidence: {res['confidence']}</div>", unsafe_allow_html=True)
    st.json(res["metadata"])
