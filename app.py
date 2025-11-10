import streamlit as st
from sdk.watermark import verify_image_watermark

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Reke Demo", page_icon="🧠", layout="centered")

st.title("Reke Demo")

# -----------------------------
# STYLING
# -----------------------------
st.markdown("""
    <style>
    /* Make buttons clean and visible */
    div.stButton > button:first-child {
        background-color: white !important;
        color: black !important;
        border: 1px solid black !important;
        border-radius: 6px !important;
        padding: 0.4em 1em !important;
        font-weight: 500 !important;
        transition: all 0.2s ease-in-out !important;
    }
    div.stButton > button:first-child:hover {
        background-color: #f5f5f5 !important;
        border-color: #000 !important;
    }
    div.stButton > button:first-child:active {
        background-color: #eaeaea !important;
        transform: scale(0.98);
    }

    /* Center the verify button */
    .stButton button[kind="primary"] {
        display: block;
        margin: 0 auto;
        font-size: 18px !important;
        padding: 0.6em 2em !important;
    }

    /* Center image preview */
    .main-image {
        display: flex;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# IMAGE SAMPLES
# -----------------------------
samples = {
    # AI Images
    "AI Model": "https://ul.postcrest.com/90uqa61eksfuzyj8uppr50be8tsj.png?format=webp&width=1664",
    "AI Painter": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-nxue8y4zt9be1.png?width=1080&crop=smart&auto=webp&s=a3f70deb45f4f4d50c09f8ffa439a83b05504440",
    "AI Panda & Chimp": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-sejwvqqzt9be1.png?width=1080&crop=smart&auto=webp&s=1a44b93bd8f02cd7f6fa98dc7ba08ef500e1adfb",
    "AI Woman": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-l2zp3ra0u9be1.png?width=1080&crop=smart&auto=webp&s=f4bde879ffc48fc635e84b865cac6ff485471acd",

    # Real Images
    "Real Cat": "https://images.wallpaperscraft.com/image/single/kitten_cat_tree_146608_938x1668.jpg",
    "Real Child": "https://img.freepik.com/free-photo/laughing-girl-climbing-ropes_1328677.jpg",
    "Real Dog": "https://cdn.sanity.io/images/4ij0poqn/production/3806e8982db7e74f828bb2039e6394cf0139b4d0-800x600.jpg",
    "Real Man": "https://img.freepik.com/free-photo/side-view-man-painting-canvas_23-2150170489.jpg",
    "Real Woman": "https://img.freepik.com/free-photo/portrait-young-attractive-emotional-girl-dressed-trendy-blue-denim-coat_1153-3942.jpg"
}

# -----------------------------
# SESSION STATE
# -----------------------------
if "selected_image" not in st.session_state:
    st.session_state["selected_image"] = None
    st.session_state["selected_label"] = None

# -----------------------------
# IMAGE SELECTION AREA
# -----------------------------
st.write("### Select an Image to Verify")

cols = st.columns(5)
i = 0
for label, url in samples.items():
    with cols[i % 5]:
        if st.button("Select", key=f"btn_{label}"):
            st.session_state["selected_image"] = url
            st.session_state["selected_label"] = label
        st.image(url, use_column_width=True)
    i += 1

st.markdown("---")

# -----------------------------
# MAIN PREVIEW + VERIFY BUTTON
# -----------------------------
if st.session_state["selected_image"]:
    st.markdown('<div class="main-image">', unsafe_allow_html=True)
    st.image(st.session_state["selected_image"], use_column_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("Verify Image", type="primary"):
        result = verify_image_watermark(st.session_state["selected_label"])
        st.subheader(result)
else:
    st.info("👆 Select one of the images above to begin verification.")

# -----------------------------
# FUTURE VISION FOOTNOTE
# -----------------------------
st.markdown("---")
st.caption("""
**Demo:**  
AI samples contain a synthetic Reke watermark. Real samples are plain.  

Future versions will include Tree-Ring watermarking, C2PA provenance,  
screenshot tamper resistance, and global SDK integration with AI Generators and APIs adopted by Platforms.
""")
