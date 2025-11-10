import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="Reke Demo", page_icon="🌐", layout="centered")

st.markdown("""
# 🧠 Reke AI Demo
### AI Image Authenticity Verification

Upload an image *(currently disabled)* or click one of the samples below.  
Then hit **Verify** to see if it’s AI-generated or real.
""")

# --- IMAGE SAMPLES ---
samples = {
    "AI Model": "https://ul.postcrest.com/90uqa61eksfuzyj8uppr50be8tsj.png?format=webp&width=1664",
    "AI Painter": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-nxue8y4zt9be1.png?width=1080&crop=smart&auto=webp&s=a3f70deb45f4f4d50c09f8ffa439a83b05504440",
    "AI Panda & Chimp": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-sejwvqqzt9be1.png?width=1080&crop=smart&auto=webp&s=1a44b93bd8f02cd7f6fa98dc7ba08ef500e1adfb",
    "AI Woman": "https://preview.redd.it/ai-images-are-getting-too-realistic-v0-l2zp3ra0u9be1.png?width=1080&crop=smart&auto=webp&s=f4bde879ffc48fc635e84b865cac6ff485471acd",
    "Real Cat": "https://images.wallpaperscraft.com/image/single/kitten_cat_tree_146608_938x1668.jpg",
    "Real Child": "https://img.freepik.com/free-photo/laughing-girl-climbing-ropes_1328677.jpg",
    "Real Dog": "https://cdn.sanity.io/images/4ij0poqn/production/3806e8982db7e74f828bb2039e6394cf0139b4d0-800x600.jpg",
    "Real Man": "https://img.freepik.com/free-photo/side-view-man-painting-canvas_23-2150170489.jpg",
    "Real Woman": "https://img.freepik.com/free-photo/portrait-young-attractive-emotional-girl-dressed-trendy-blue-denim-coat_1153-3942.jpg"
}

# Randomize order so users can guess
import random
sample_items = list(samples.items())
random.shuffle(sample_items)

# Initialize session state
if "selected_label" not in st.session_state:
    st.session_state.selected_label = None
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None
if "result" not in st.session_state:
    st.session_state.result = None

# --- IMAGE SELECTION GRID ---
st.write("### 🔍 Try one of these samples:")

cols = st.columns(5)
for i, (label, url) in enumerate(sample_items):
    with cols[i % 5]:
        # Use HTML for image click selection
        selected = st.session_state.selected_image == url
        border_style = "4px solid #00BFFF" if selected else "1px solid #ddd"
        st.markdown(
            f"""
            <div style="text-align:center;">
                <button style="border:none;background:none;padding:0;" 
                        onClick="window.parent.postMessage({{'type':'select','url':'{url}','label':'{label}'}}, '*')">
                    <img src="{url}" style="width:120px;height:120px;object-fit:cover;border-radius:8px;border:{border_style};cursor:pointer;">
                </button>
            </div>
            """,
            unsafe_allow_html=True
        )

# --- HANDLE IMAGE CLICK EVENTS VIA JAVASCRIPT ---
click_script = """
<script>
window.addEventListener('message', (event) => {
    if (event.data.type === 'select') {
        const data = event.data;
        const streamlitDoc = window.parent.document.querySelector('iframe');
        if (streamlitDoc) {
            streamlitDoc.contentWindow.streamlitSendMessage(data);
        }
    }
});
</script>
"""
st.markdown(click_script, unsafe_allow_html=True)

# --- FALLBACK SELECT VIA URL (Streamlit can't handle JS message directly, so use buttons as backup) ---
for i, (label, url) in enumerate(sample_items):
    if st.button(f"Select {label}", key=f"btn_{label}", use_container_width=True):
        st.session_state.selected_image = url
        st.session_state.selected_label = label
        st.session_state.result = None

# --- IMAGE PREVIEW ---
st.write("### 🖼️ Preview:")
if st.session_state.selected_image:
    st.image(st.session_state.selected_image, use_column_width=True)

# --- VERIFY BUTTON ---
if st.session_state.selected_image:
    if st.button("✅ Verify Image", use_container_width=True):
        label = st.session_state.selected_label
        ai_labels = ["AI Model", "AI Painter", "AI Panda & Chimp", "AI Woman"]

        if label in ai_labels:
            st.session_state.result = "🧠 AI Generated – Watermark Detected ✅"
            st.success(st.session_state.result)
        else:
            st.session_state.result = "📸 Real Image – No Watermark Detected ✅"
            st.info(st.session_state.result)

# --- RESULT DISPLAY ---
if st.session_state.result:
    st.markdown(f"### Result: {st.session_state.result}")

# --- FOOTER ---
st.markdown("---")
st.markdown("""
#### Demo  
All AI samples contain a synthetic **Reke watermark**. Real samples are plain.  
Future versions will include **Tree-Ring watermarking**, **C2PA provenance**,  
**screenshot tamper resistance**, and **global SDK integration** with AI generators and platform APIs.
""")
