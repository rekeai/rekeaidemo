# Simulated C2PA manifest verification
def verify_c2pa_manifest(image_id: str):
    """
    Mock C2PA manifest reader — placeholder for future integration.
    """
    if "ai" in image_id:
        return {
            "verified": True,
            "source": "C2PA Manifest (Simulated)",
            "creator": "AI Generator Model v1.3"
        }
    else:
        return {
            "verified": False,
            "source": None,
            "creator": None
        }
