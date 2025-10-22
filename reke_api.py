# reke_api.py
from sdk.watermark import detect_watermark
from sdk.c2pa_manifest import get_c2pa_metadata

def verify(file_name: str):
    """Simulated Reke API endpoint"""
    detected, confidence = detect_watermark(file_name)
    meta = get_c2pa_metadata(file_name)

    if detected:
        status = "⚠️ AI Generated Image — Watermark Detected"
        verified = False
    else:
        status = "✅ Real Image — No Watermark Detected"
        verified = True

    return {
        "filename": file_name,
        "verified": verified,
        "status": status,
        "confidence": confidence,
        "metadata": meta
    }
