def get_c2pa_metadata(image_name: str):
    """
    Simulated C2PA metadata output.
    Returns provenance-style info based on image origin.
    """
    if "ai_" in image_name:
        return {
            "generator": "Reke Demo AI",
            "version": "0.1-prototype",
            "timestamp": "2025-10-05",
            "verified_by": "Reke Demo SDK"
        }
    else:
        return {
            "generator": "None",
            "version": "Original",
            "timestamp": "Unknown",
            "verified_by": "Reke Demo SDK"
        }
