# SDK package initializer for Reke.
# This allows importing as `from sdk import ...`
# and ensures the watermark and C2PA modules are recognized.

from .watermark import detect_watermark
from .c2pa_manifest import get_c2pa_metadata
