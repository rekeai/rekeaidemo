# app.py
import os
import random
import streamlit as st
from sdk import embed_watermark
from PIL import Image
import requests

st.set_page_config(page_title="Reke Demo — Verify", layout="centered", page_icon="🛡️")
st.markdown(
    """
    <style>
    footer{visibility:hidden}
    .sample-grid img{
        border-radius:8px;
        cursor:pointer;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 0 0 2px transparent;
    }
    .sample-grid img:hover{
        transform: scale(1.03);
        box-shadow: 0 0 0 2px #00b4d8;
    }
    .selected{
        box-shadow: 0 0 0 3px #00b4d8 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛡️ Reke — Live Demo")
st.write("Select an image below to preview, then click **Verify Image**.")

# ──────────── Setup
SAMPLE_FILENAMES = [
    "ai_model.jpg", "ai_painter.jpg", "ai_panda_chimp.jpg", "ai_woman.jpg",
    "real_cat.jpg", "real_child.jpg", "real_dog.jpg", "real_man.jpg", "real_woman.jpg",
]
AI_SAMPLES = {"ai_model.jpg", "ai_painter.jpg", "ai_panda_chimp.jpg", "ai_woman.jpg"}
REAL_SAMPLES = {"real_cat.jpg", "real_child.jpg", "real_dog.jpg", "real_man.jpg", "real_woman.jpg"}
FALLBACK = {
    "ai_model.jpg": "https://ul.postcrest.com/90uqa61eksfuzyj8uppr50be8tsj.png?format=webp&width=1664",
    "ai_painter.jpg": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-nxue8y4zt9be1.png?width=1080&crop=smart&auto=webp",
    "ai_panda_chimp.jpg": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-sejwvqqzt9be1.png?width=1080&crop=smart&auto=webp",
    "ai_woman.jpg": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-l2zp3ra0u9be1.png?width=1080&crop=smart&auto=webp",
    "real_cat.jpg": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?auto=format&fit=crop&w=800&q=80",
    "real_child.jpg": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=crop&w=800&q=80",
    "real_dog.jpg": "https://cdn.sanity.io/images/4ij0poqn/production/3806e8982db7e74f828bb2039e6394cf0139b4d0-800x600.jpg",
    "real_man.jpg": "https://img.freepik.com/free-photo/side-view-man-painting-canvas_23-2150170489.jpg",
    "real_woman.jpg": "https://img.freepik.com/free-photo/portrait-young-attractive-emotional-girl-dressed-trendy-blue-denim-coat_1153-3942.jpg",
}

samples = FALLBACK.copy()
os.makedirs("watermarked", exist_ok=True)
for fn in AI_SAMPLES:
    dst = os.path.join("watermarked", fn + ".reke.png")
    if not os.path.exists(dst):
        try:
            r = requests.get(samples[fn], timeout=15)
            if r.ok:
                tmp = os.path.join("watermarked", fn)
                with open(tmp, "wb") as f: f.write(r.content)
                embed_watermark(tmp, dst)
                os.remove(tmp)
        except Exception:
            pass
    if os.path.exists(dst):
        samples[fn] = dst

# Randomize sample order
sample_items = list(samples.items())
random.shuffle(sample_items)

# ──────────── Session
if "selected" not in st.session_state:
    st.session_state["selected"] = None
if "selected_file" not in st.session_state:
    st.session_state["selected_file"] = None

# ──────────── UI
preview_col, action_col = st.columns([2, 1])
with preview_col:
    st.markdown("### Preview")
    if st.session_state["selected"]:
        st.image(st.session_state["selected"], use_column_width=True)
    else:
        st.markdown(
            "<div style='height:360px;border:2px dashed #ccc;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#999;'>Select a sample below</div>",
            unsafe_allow_html=True,
        )

with action_col:
    st.markdown("### Actions")
    if st.button("Verify Image", use_container_width=True):
        if not st.session_state["selected"]:
            st.warning("Please select an image first.")
        else:
            fn = st.session_state["selected_file"]
            if fn in AI_SAMPLES:
                st.success("🚨 AI Generated — Watermark detected")
            elif fn in REAL_SAMPLES:
                st.info("✅ Real — No watermark detected")
            else:
                st.info("✅ Real — No watermark detected (no registered watermark)")
        st.markdown("---")

# ──────────── Sample grid
st.markdown("### Samples")
cols = st.columns(5)
for i, (fn, path) in enumerate(sample_items):
    with cols[i % 5]:
        if st.button(f"select_{i}", label_visibility="collapsed", key=f"img_{i}"):
            st.session_state["selected"] = path
            st.session_state["selected_file"] = fn
        if st.session_state.get("selected_file") == fn:
            st.markdown(f'<img src="{path}" class="selected" width="100%">', unsafe_allow_html=True)
        else:
            st.markdown(f'<img src="{path}" width="100%">', unsafe_allow_html=True)

# ──────────── Footer
st.markdown("---")
st.markdown(
    """
    **Demo:**  
    AI samples contain a synthetic Reke watermark. Real samples are plain.  
    Future versions will include Tree-Ring watermarking, C2PA provenance, screenshot tamper resistance,  
    and global SDK integration with AI Generators and APIs adopted by Platforms.
    """
)
