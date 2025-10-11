from sdk.watermark import detect_watermark
from sdk.c2pa_manifest import get_c2pa_metadata

def verify(file_name: str):
    """
    Simulated Stripe-style Reke verification API.
    Combines Tree-Ring watermark detection and C2PA metadata.
    """
    detected, confidence = detect_watermark(file_name)
    meta = get_c2pa_metadata(file_name)

    if detected:
        status = "⚠️ AI-Generated"
    else:
        status = "✅ Real Content"

    return {
        "filename": file_name,
        "verified": not detected,
        "status": status,
        "confidence": confidence,
        "metadata": meta
    }
