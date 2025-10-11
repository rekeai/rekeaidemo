import random

def detect_watermark(image_name: str):
    """
    Simulated Tree-Ring watermark detection.
    Returns True if AI-generated watermark detected, False otherwise.
    Also returns a confidence score (0.90 - 0.99).
    """
    ai_samples = [
        "ai_mode.jpg",
        "ai_painter.jpg",
        "ai_panda_chimp.jpg",
        "ai_woman.jpg"
    ]

    if image_name in ai_samples:
        return True, round(random.uniform(0.92, 0.99), 2)
    else:
        return False, round(random.uniform(0.94, 0.99), 2)
