# sdk/watermark.py
"""
Demo Reke SDK (prototype).
- embed_watermark(input_path, output_path, origin)
- verify_image_bytes(image_bytes) -> (status_str, manifest_or_none, sig_ok_bool)

This is a demo implementation intended for investor demos.
Do NOT treat this as production cryptographic code.
"""

import os
import io
import json
import hmac
import hashlib
from datetime import datetime, timezone
from PIL import Image, ImageDraw, PngImagePlugin

REKE_SECRET = os.getenv("REKE_SECRET", "reke_demo_secret")  # set same on API & generator in deploy

def _now_iso():
    return datetime.now(timezone.utc).isoformat()

def _content_hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def _hmac_sig(content_hash: str) -> str:
    return hmac.new(REKE_SECRET.encode(), content_hash.encode(), hashlib.sha256).hexdigest()

def _build_manifest(origin: str, content_hash: str):
    return {
        "spec": "reke-tree-demo",
        "version": "0.1",
        "timestamp": _now_iso(),
        "reke_origin": origin,
        "content_hash": content_hash,
        "sig": _hmac_sig(content_hash)
    }

def _draw_tree_rings(img: Image.Image, rings=12, ring_alpha=12):
    """
    Draw faint concentric rings on an RGBA overlay and composite it.
    ring_alpha: 0-255 small -> barely visible
    """
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0,0,0,0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = w // 2, h // 2
    max_r = min(w, h) // 3
    for i in range(1, rings+1):
        r = int(max_r * (i / rings))
        alpha = ring_alpha  # faint
        color = (255,255,255,alpha)
        bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(bbox, outline=color, width=1)
    composed = Image.alpha_composite(img.convert("RGBA"), overlay)
    return composed.convert("RGB")

def _embed_pixel_pattern(img: Image.Image, sig_hex: str):
    """
    Deterministic tiny pixel pattern: modifies a small square in upper-left
    based on signature bytes. Used as a simple, detectable pattern (demo).
    """
    w, h = img.size
    px = img.load()
    pattern = bytes.fromhex(sig_hex)[:64]  # take first 64 bytes
    side = min(16, w//10, h//10)
    idx = 0
    # modify the red channel LSBs in a small square
    for y in range(side):
        for x in range(side):
            r,g,b = px[x, y][:3]
            bit = pattern[idx % len(pattern)] & 1
            r = (r & ~1) | bit
            px[x,y] = (r, g, b)
            idx += 1
    return img

def embed_watermark(input_path: str, output_path: str=None, origin: str="Fake AI Generator"):
    """
    Embed demo watermark: draw rings, embed tiny pixel pattern, save manifest in PNG tEXt.
    Returns output_path.
    """
    if output_path is None:
        base, _ = os.path.splitext(input_path)
        output_path = base + ".reke.png"

    img = Image.open(input_path).convert("RGB")
    # draw subtle rings
    watermarked = _draw_tree_rings(img, rings=14, ring_alpha=10)
    # compute content hash of pixels
    pixels = watermarked.convert("RGBA").tobytes()
    content_hash = _content_hash_bytes(pixels)
    sig = _hmac_sig(content_hash)
    # embed pixel pattern
    watermarked = _embed_pixel_pattern(watermarked, sig)
    # manifest
    manifest = _build_manifest(origin, content_hash)
    manifest_json = json.dumps(manifest)
    # save as PNG with tEXt
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("reke_manifest", manifest_json)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    watermarked.save(output_path, "PNG", pnginfo=pnginfo, optimize=True)
    return output_path

def _detect_pixel_pattern(img: Image.Image):
    """
    Demo heuristic to check for the pixel pattern we embedded.
    Reads the small upper-left square and tests whether red channel LSB
    matches a consistent pattern (simple majority).
    Returns True/False.
    """
    w,h = img.size
    side = min(16, w//10, h//10)
    px = img.convert("RGB").load()
    bits = []
    for y in range(side):
        for x in range(side):
            r,g,b = px[x,y]
            bits.append(r & 1)
    if not bits:
        return False
    ones = sum(bits)
    zeros = len(bits) - ones
    # if pattern has clear imbalance (demo): consider detected
    return ones > 3 and zeros > 3 and (ones != zeros)

def verify_image_bytes(image_bytes: bytes):
    """
    Verify manifest and pixel pattern.
    Returns (status_str, manifest_or_none, sig_ok_bool)
    status_str: "AI Generated", "Real", "Unknown"
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
    except Exception:
        return "Unknown", None, False

    manifest = None
    sig_ok = False

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
    else:
        # For non-PNGs, we can't read tEXt reliably; fall back to pattern detect
        manifest = None

    if sig_ok and manifest:
        return "AI Generated", manifest, True

    # If no valid manifest, run pixel-pattern detection heuristic
    # (this will detect our embedded demo pattern in many cases)
    try:
        detected = _detect_pixel_pattern(img)
        if detected:
            # create a fake manifest summary for UI consistency (demo)
            fake = {"note": "pattern-detected-demo"}
            return "AI Generated", fake, False
    except Exception:
        pass

    return "Real", None, False
