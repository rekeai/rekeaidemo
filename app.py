# app.py
import os
import io
import streamlit as st
from PIL import Image
from sdk.watermark import embed_watermark, verify_image_bytes

# --- Config ---
st.set_page_config(page_title="Reke Demo — Verify AI or Real", layout="centered", page_icon="🛡️")
st.markdown("<style>footer {visibility: hidden;} </style>", unsafe_allow_html=True)

st.title("🛡️ Reke — Demo (Verify AI or Real)")
st.caption("A demonstration prototype. AI samples are watermarked by the Reke demo SDK.")

# sample images (local preferred — fallback to web links if not present)
SAMPLES_LOCAL_DIR = "sample_images"
SAMPLE_FILENAMES = [
    "ai_mode.jpg",
    "ai_painter.jpg",
    "ai_panda_chimp.jpg",
    "ai_woman.jpg",
    "real_cat.jpg",
    "real_child.jpg",
    "real_dog.jpg",
    "real_man.jpg",
    "real_woman.jpg"
]

# helper: build mapping of label->path_or_url
samples = {}
for fn in SAMPLE_FILENAMES:
    local = os.path.join(SAMPLES_LOCAL_DIR, fn)
    if os.path.exists(local):
        samples[fn] = local
    else:
        # fallback web URLs (replace with your public links if desired)
        fallback_map = {
            "ai_mode.jpg": "https://ul.postcrest.com/90uqa61eksfuzyj8uppr50be8tsj.png?format=webp&width=1664",
            "ai_painter.jpg": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-nxue8y4zt9be1.png?width=1080&crop=smart&auto=webp&s=a3f70deb45f4f4d50c09f8ffa439a83b05504440",
            "ai_panda_chimp.jpg": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-sejwvqqzt9be1.png?width=1080&crop=smart&auto=webp&s=1a44b93bd8f02cd7f6fa98dc7ba08ef500e1adfb",
            "ai_woman.jpg": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-l2zp3ra0u9be1.png?width=1080&crop=smart&auto=webp&s=f4bde879ffc48fc635e84b865cac6ff485471acd",
            "real_cat.jpg": "https://images.unsplash.com/photo-1592194996308-7b43878e84a6?auto=format&fit=crop&w=800&q=80",
            "real_child.jpg": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?auto=format&fit=crop&w=800&q=80",
            "real_dog.jpg": "https://cdn.sanity.io/images/4ij0poqn/production/3806e8982db7e74f828bb2039e6394cf0139b4d0-800x600.jpg",
            "real_man.jpg": "https://img.freepik.com/free-photo/side-view-man-painting-canvas_23-2150170489.jpg",
            "real_woman.jpg": "https://img.freepik.com/free-photo/portrait-young-attractive-emotional-girl-dressed-trendy-blue-denim-coat_1153-3942.jpg",
        }
        samples[fn] = fallback_map.get(fn, "")

# Ensure watermarked directory exists and watermark the AI samples on first run
os.makedirs("watermarked", exist_ok=True)
# create watermarked copies for the AI samples (if local exists)
for fn in SAMPLE_FILENAMES[:4]:  # first 4 are AI samples assumed
    src = samples[fn]
    dst = os.path.join("watermarked", fn + ".reke.png")
    if os.path.exists(src) and not os.path.exists(dst):
        try:
            embed_watermark(src, dst, origin="Demo AI Generator")
            # overwrite samples mapping to point to the watermarked version (so UI will detect)
            samples[fn] = dst
        except Exception:
            # fallback: keep original
            pass

# Session state
if "selected" not in st.session_state:
    st.session_state["selected"] = None
if "selected_label" not in st.session_state:
    st.session_state["selected_label"] = None

# Layout: center preview + Verify button
col1, col2 = st.columns([2,1])
with col1:
    st.markdown("### Preview")
    if st.session_state["selected"]:
        # selected can be filepath or url
        try:
            st.image(st.session_state["selected"], caption=st.session_state["selected_label"], use_column_width=True)
        except Exception:
            # if path is bytes, show from bytes
            if isinstance(st.session_state["selected"], bytes):
                st.image(st.session_state["selected"])
            else:
                st.write("Unable to render preview.")
    else:
        st.markdown(
            "<div style='height:360px; display:flex; align-items:center; justify-content:center; border:2px dashed #ddd; border-radius:10px;'>"
            "<div style='text-align:center;color:#777;'>No image selected<br><small>Pick a sample below</small></div></div>",
            unsafe_allow_html=True
        )

with col2:
    st.markdown("### Actions")
    uploaded = st.file_uploader("Or upload your own image (will be detected as Real unless watermarked):", type=["png","jpg","jpeg"], accept_multiple_files=False)
    if uploaded:
        try:
            img_bytes = uploaded.read()
            st.session_state["selected"] = img_bytes
            st.session_state["selected_label"] = uploaded.name
            st.success("Uploaded and selected.")
        except Exception as e:
            st.error("Upload failed: " + str(e))

    if st.button("Verify Image", use_container_width=True):
        if not st.session_state["selected"]:
            st.warning("Please select or upload an image first.")
        else:
            # feed bytes to verify_image_bytes
            try:
                # if selected is bytes (uploaded), use directly
                if isinstance(st.session_state["selected"], bytes):
                    data = st.session_state["selected"]
                else:
                    # path or URL: try to open file
                    sel = st.session_state["selected"]
                    if os.path.exists(sel):
                        with open(sel, "rb") as f:
                            data = f.read()
                    else:
                        # assume URL: fetch it
                        import requests
                        r = requests.get(sel, timeout=15)
                        data = r.content

                status, manifest, sig_ok = verify_image_bytes(data)
                if status == "AI Generated":
                    st.success("🚨 AI Generated — Watermark detected")
                    st.json({"manifest": manifest, "signature_valid": bool(sig_ok)})
                elif status == "Real":
                    st.info("✅ Real — No watermark detected")
                    st.write("Recommendation: if the source is unknown, the platform should run additional proactive scans (e.g., third-party detectors) before accepting content.")
                else:
                    st.warning("❓ Unknown — could not determine")
            except Exception as e:
                st.error("Verification failed: " + str(e))

st.markdown("---")
st.markdown("### Samples (click to select)")
# thumbnails grid
cols = st.columns(5)
i = 0
for label, path in samples.items():
    with cols[i % 5]:
        # display thumbnail
        try:
            st.image(path, caption=label, use_column_width=True)
        except Exception:
            st.text(label)
        if st.button(f"Select {label}", key=f"btn_{label}"):
            st.session_state["selected"] = path
            st.session_state["selected_label"] = label
    i += 1

st.markdown("---")
st.markdown("**Notes (demo):** This prototype embeds a visible tree-ring overlay + a small deterministic pixel pattern and stores a manifest in PNG metadata. In production we'd use research-grade Tree-Ring techniques, robust signing, C2PA packaging, and hardened detection that survives more transformations (screenshots, recompression).")
