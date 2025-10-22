# sdk/c2pa_manifest.py
def get_c2pa_metadata(image_name: str):
    if "ai_" in image_name:
        return {
            "generator": "Reke Demo AI",
            "version": "0.1-prototype",
            "timestamp": "2025-10-16",
            "provenance": "Tree-Ring watermark embedded"
        }
    else:
        return {
            "generator": "None",
            "version": "Original",
            "timestamp": "Unknown",
            "provenance": "No watermark detected"
        }
