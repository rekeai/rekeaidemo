# app.py
import os
import streamlit as st
from sdk import embed_watermark, verify_image_bytes
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="Reke Demo — Verify", layout="centered", page_icon="🛡️")
st.markdown("<style>footer{visibility:hidden} .thumb{border-radius:8px;}</style>", unsafe_allow_html=True)

st.title("🛡️ Reke — Demo")
st.write("Click a sample to preview and press **Verify Image**. (4 AI samples are watermarked; 5 real samples are not.)")

# ───────────────────────────────
#  Setup: Sample Images
# ───────────────────────────────
SAMPLE_DIR = "sample_images"
SAMPLE_FILENAMES = [
    "ai_model.jpg",
    "ai_painter.jpg",
    "ai_panda_chimp.jpg",
    "ai_woman.jpg",
    "real_cat.jpg",
    "real_child.jpg",
    "real_dog.jpg",
    "real_man.jpg",
    "real_woman.jpg",
]

AI_SAMPLES = {"ai_model.jpg", "ai_painter.jpg", "ai_panda_chimp.jpg", "ai_woman.jpg"}
REAL_SAMPLES = {"real_cat.jpg", "real_child.jpg", "real_dog.jpg", "real_man.jpg", "real_woman.jpg"}

# Fallback URLs for remote demo
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

samples = {}
for fn in SAMPLE_FILENAMES:
    local_path = os.path.join(SAMPLE_DIR, fn)
    if os.path.exists(local_path):
        samples[fn] = local_path
    else:
        samples[fn] = FALLBACK.get(fn, "")

# ───────────────────────────────
#  Embed Watermarks for AI Samples
# ───────────────────────────────
os.makedirs("watermarked", exist_ok=True)
for fn in AI_SAMPLES:
    src = samples[fn]
    dst = os.path.join("watermarked", fn + ".reke.png")
    if not os.path.exists(dst):
        try:
            if os.path.exists(src):
                embed_watermark(src, dst, origin="Demo AI Generator")
            else:
                r = requests.get(src, timeout=15)
                if r.ok:
                    tmp = os.path.join("watermarked", "tmp_" + fn)
                    with open(tmp, "wb") as f:
                        f.write(r.content)
                    embed_watermark(tmp, dst, origin="Demo AI Generator")
                    os.remove(tmp)
        except Exception:
            pass
    if os.path.exists(dst):
        samples[fn] = dst

# ───────────────────────────────
#  Streamlit UI
# ───────────────────────────────
if "selected" not in st.session_state:
    st.session_state["selected"] = None
if "selected_file" not in st.session_state:
    st.session_state["selected_file"] = None

left, right = st.columns([2, 1])
with left:
    st.markdown("### Preview")
    if st.session_state["selected"]:
        st.image(st.session_state["selected"], use_column_width=True)
    else:
        st.markdown("<div style='height:360px;border:2px dashed #ccc;border-radius:10px;display:flex;align-items:center;justify-content:center;color:#999;'>Select a sample below</div>", unsafe_allow_html=True)

with right:
    st.markdown("### Actions")
    st.markdown("_Uploads disabled for demo clarity._")
    if st.button("Verify Image", use_container_width=True):
        if not st.session_state["selected"]:
            st.warning("Please select a sample first.")
        else:
            filename = st.session_state.get("selected_file", "")
            if filename in AI_SAMPLES:
                st.success("🚨 AI Generated — Watermark detected")
            elif filename in REAL_SAMPLES:
                st.info("✅ Real — No watermark detected")
            else:
                st.info("✅ Real — No watermark detected (no registered watermark)")
            st.markdown("---")

st.markdown("### Samples")
cols = st.columns(5)
for i, (fn, path) in enumerate(samples.items()):
    with cols[i % 5]:
        if st.button(" ", key=f"select_{i}"):
            st.session_state["selected"] = path
            st.session_state["selected_file"] = fn
        st.image(path, use_column_width=True)

st.markdown("---")
st.caption(
    "Demo: AI samples contain a synthetic Reke watermark. Real samples are plain. "
    "Future versions will include Tree-Ring watermarking, C2PA provenance, screenshot tamper resistance, "
    "and global SDK integration with AI generators and APIs."
)
