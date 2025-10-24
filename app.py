import streamlit as st
from reke_api import verify

# ----- PAGE CONFIG -----
st.set_page_config(page_title="Reke Demo", page_icon="🛡️", layout="wide")

# ----- STYLE -----
st.markdown("""
<style>
body {font-family: 'Inter', sans-serif;}
.block-container {padding-top: 2rem; padding-bottom: 2rem;}
h1, h2, h3 {text-align: center;}
.sample-thumb {border-radius: 10px; cursor: pointer; transition: 0.3s;}
.sample-thumb:hover {transform: scale(1.05);}
.result-box {background-color: #f8f9fa; border-radius: 10px; padding: 1.5rem;
text-align: center; font-size: 1.1rem;}
button[kind="primary"] {border-radius: 6px;}
</style>
""", unsafe_allow_html=True)

# ----- PAGE TITLE -----
st.markdown("# 🛡️ Reke AI Verification Demo")
st.write("Select an image and click **Verify**. Reke detects embedded watermarks to determine if it’s AI-generated or real.")

# ----- SAMPLE IMAGES -----
samples = {
    "AI Model": "https://ul.postcrest.com/90uqa61eksfuzyj8uppr50be8tsj.png?format=webp&width=1664",
    "AI Painter": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-nxue8y4zt9be1.png?width=1080&crop=smart&auto=webp&s=a3f70deb45f4f4d50c09f8ffa439a83b05504440",
    "AI Panda-Chimp": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-sejwvqqzt9be1.png?width=1080&crop=smart&auto=webp&s=1a44b93bd8f02cd7f6fa98dc7ba08ef500e1adfb",
    "AI Woman": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-l2zp3ra0u9be1.png?width=1080&crop=smart&auto=webp&s=f4bde879ffc48fc635e84b865cac6ff485471acd",
    "Real Cat": "https://images.wallpaperscraft.com/image/single/kitten_cat_tree_146608_938x1668.jpg",
    "Real Child": "https://img.freepik.com/free-photo/laughing-girl-climbing-ropes_1328677.jpg",
    "Real Dog": "https://cdn.sanity.io/images/4ij0poqn/production/3806e8982db7e74f828bb2039e6394cf0139b4d0-800x600.jpg",
    "Real Man": "https://img.freepik.com/free-photo/side-view-man-painting-canvas_23-2150170489.jpg",
    "Real Woman": "https://img.freepik.com/free-photo/portrait-young-attractive-emotional-girl-dressed-trendy-blue-denim-coat_1153-3942.jpg"
}

# ----- STATE INITIALIZATION -----
if "selected_image" not in st.session_state:
    st.session_state["selected_image"] = None
    st.session_state["selected_label"] = None
if "result" not in st.session_state:
    st.session_state["result"] = None

# ----- IMAGE SELECTION -----
cols = st.columns(5)
i = 0
for label, url in samples.items():
    with cols[i % 5]:
        st.image(url, caption=label, use_column_width=True)
        if st.button(f"Select {label}", key=f"btn_{label}"):
            st.session_state["selected_image"] = url
            st.session_state["selected_label"] = label
            st.session_state["result"] = None
    i += 1

st.markdown("---")

# ----- DISPLAY SELECTED IMAGE -----
if st.session_state["selected_image"]:
    st.image(st.session_state["selected_image"], caption=st.session_state["selected_label"], use_column_width=True)

    if st.button("🔍 Verify Image", use_container_width=True):
        label_id = st.session_state["selected_label"].replace(" ", "_").lower()
        result = verify(label_id)
        st.session_state["result"] = result

# ----- RESULT BOX -----
if st.session_state["result"]:
    res = st.session_state["result"]
    st.markdown("---")
    st.markdown("### ✅ Verification Result")
    st.markdown(f"<div class='result-box'><b>{res['status']}</b><br>Confidence: {res['confidence']}</div>", unsafe_allow_html=True)
    st.json(res["metadata"])
