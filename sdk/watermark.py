import hashlib
import hmac
import json
import io
from PIL import Image

# Secret key for demo HMAC signature (in production, each AI model would have its own key)
SECRET_KEY = b"reke_demo_secret_key"


def _hmac_sig(content_hash: str) -> str:
    """Generate HMAC signature for the given hash."""
    return hmac.new(SECRET_KEY, content_hash.encode(), hashlib.sha256).hexdigest()


def embed_watermark(image_path: str, ai_generator: str) -> bytes:
    """
    Simulate embedding Tree-Ring invisible watermark.
    Stores a lightweight manifest in PNG metadata.
    """
    img = Image.open(image_path).convert("RGB")
    content_hash = hashlib.sha256(img.tobytes()).hexdigest()

    manifest = {
        "generator": ai_generator,
        "version": "0.1-demo",
        "content_hash": content_hash,
        "sig": _hmac_sig(content_hash)
    }

    # Store manifest in image metadata (PNG format)
    meta = PngInfo()
    meta.add_text("reke_manifest", json.dumps(manifest))

    # Save to bytes
    output = io.BytesIO()
    img.save(output, format="PNG", pnginfo=meta)
    return output.getvalue()


def verify_image_bytes(image_bytes: bytes):
    """
    Verify manifest. Simplified for demo:
    - If a valid REKE manifest exists and signature matches -> AI Generated.
    - Otherwise -> Real (No watermark detected).
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
    except Exception:
        return "Unknown", None, False

    manifest = None
    sig_ok = False

    # Check manifest (PNG tEXt field)
    if img.format == "PNG":
        m = img.info.get("reke_manifest")
        if m:
            try:
                manifest = json.loads(m)
            except Exception:
                manifest = None
        if manifest and "content_hash" in manifest and "sig" in manifest:
            expected = _hmac_sig(manifest["content_hash"])
            if expected == manifest.get("sig"):
                sig_ok = True

    if sig_ok and manifest:
        # ✅ AI watermarked image detected
        return "AI Generated", manifest, True

    # ✅ No manifest → Real
    return "Real", None, False


# Helper for local file verification (used in reke_api.py)
def verify_local_image(file_path: str):
    with open(file_path, "rb") as f:
        img_bytes = f.read()
    return verify_image_bytes(img_bytes)
