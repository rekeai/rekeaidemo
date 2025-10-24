# sdk/watermark.py
import random

def detect_watermark(image_name: str):
    """Simulated Tree-Ring watermark detection"""
    ai_samples = [
        "ai_model",
        "ai_painter",
        "ai_panda_chimp",
        "ai_woman"
    ]
    if any(ai in image_name for ai in ai_samples):
        return True, round(random.uniform(0.94, 0.99), 2)
    else:
        return False, round(random.uniform(0.94, 0.99), 2)
