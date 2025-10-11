import streamlit as st
import os  # Add this for debugging

# --- Streamlit Page Config ---
st.set_page_config(page_title="Reke Demo", page_icon="🛡️", layout="wide")

# --- Header / Intro ---
st.markdown("""
# 🛡️ Reke Demo — Verify AI or Real  
**The Stripe-style prototype for AI verification**

Choose a sample image and see how Reke’s verification API detects AI-generated content in real-time.
""")

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
for label, filename in samples.items():
    with cols[index % 3]:
        image_path = f"sample_images/{filename}"
        exists = os.path.exists(image_path)
        st.write(f"Debug: Path '{image_path}' exists? {exists}")  # Debug line
        if not exists:
            st.error(f"Missing: {image_path}")
        st.image(image_path, caption=label, use_container_width=True)  # Fixed indent
        if st.button(f"Verify {label}", key=filename):
            result = verify(filename)
            st.session_state["result"] = result
    index += 1

# --- Display Results ---
if "result" in st.session_state:
    res = st.session_state["result"]
    st.markdown("---")
    st.subheader("🔍 Verification Result")
    st.write(f"**File:** {res['filename']}")
    st.write(f"**Status:** {res['status']}")
    st.write(f"**Confidence:** {res['confidence']}")
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
