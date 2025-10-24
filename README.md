https://rekeai.github.io/rekeaidemo/

# Reke Demo — Investor Prototype

Single-page Streamlit demo showcasing Reke watermark SDK + verification flow.

Run:
1. pip install -r requirements.txt
2. streamlit run app.py

Place sample images in `sample_images/` or rely on built-in web fallbacks.

What it shows:
- AI sample images are watermarked by the demo SDK (rings + manifest + pixel pattern).
- Verify button detects watermark (AI) or not (Real).
- Upload any image: non-watermarked images will register as Real (and you can demonstrate 'proactive' next steps).

Notes:
This is a demo/prototype. Production requires research-grade Tree-Ring implementations, C2PA integration, distributed keys, and hardened detection.
