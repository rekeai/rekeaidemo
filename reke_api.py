# Mock Reke API — connects Streamlit frontend with SDK backend.
from sdk import detect_watermark, verify_c2pa_manifest

def verify(image_id: str):
    """
    Simulates Reke's verification API combining Tree-Ring + C2PA results.
    """
    watermark_result = detect_watermark(image_id)
    c2pa_result = verify_c2pa_manifest(image_id)

    if watermark_result["detected"]:
        status = "🧠 AI-Generated Image — Watermark Detected"
    else:
        status = "📸 Real Image — No Watermark Detected"

    return {
        "status": status,
        "confidence": watermark_result["confidence"],
        "metadata": {
            "tree_ring_method": watermark_result["method"],
            "c2pa_verified": c2pa_result["verified"],
            "c2pa_source": c2pa_result["source"],
            "creator": c2pa_result["creator"]
        }
    }
