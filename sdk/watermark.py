# Simulated Tree-Ring Watermark detection for demo purposes
import random

def detect_watermark(image_id: str):
    """
    Simulated watermark detection — in production this would
    call Reke's deep model or Tree-Ring detection SDK.
    """
    if "ai" in image_id:
        return {
            "detected": True,
            "confidence": round(random.uniform(0.94, 0.99), 2),
            "method": "Tree-Ring watermark pattern"
        }
    else:
        return {
            "detected": False,
            "confidence": round(random.uniform(0.88, 0.96), 2),
            "method": "No watermark found"
        }
