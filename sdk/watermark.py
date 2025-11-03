# sdk.py
from PIL import Image
import numpy as np
import io

# Simple invisible watermark embedder for demo (not real cryptographic watermark)
def embed_watermark(input_image_path, output_image_path, origin="Reke AI Generator"):
    """
    Simulates embedding an invisible watermark into an image.
    For demo purposes only — not a secure or production watermark.
    """
    try:
        img = Image.open(input_image_path).convert("RGB")
        arr = np.array(img).astype(np.uint16)

        # Embed a faint repeating pattern in the blue channel
        # (This is only for visualization in concept demos)
        watermark_strength = 3
        pattern = np.tile(np.array([[0, 1], [1, 0]]), (arr.shape[0] // 2, arr.shape[1] // 2))
        arr[..., 2] = np.clip(arr[..., 2] + (pattern[:arr.shape[0], :arr.shape[1]] * watermark_strength), 0, 255)

        Image.fromarray(arr.astype(np.uint8)).save(output_image_path, "PNG")
    except Exception as e:
        print(f"Watermark embed failed for {input_image_path}: {e}")

def verify_image_bytes(image_bytes):
    """
    Simulates verifying watermark presence.
    Returns:
        dict: { "watermark_detected": bool, "origin": str }
    """
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        arr = np.array(img).astype(np.int16)

        # Detect the faint pattern in the blue channel
        mean_blue = arr[..., 2].mean()
        diff = np.abs(arr[..., 2] - mean_blue)
        pattern_signal = (diff > 2).mean()

        if pattern_signal > 0.15:
            return {"watermark_detected": True, "origin": "Reke AI Generator"}
        else:
            return {"watermark_detected": False, "origin": None}
    except Exception:
        return {"watermark_detected": False, "origin": None}
