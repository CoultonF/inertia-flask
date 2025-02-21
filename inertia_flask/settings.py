from .utils import InertiaJsonEncoder


class Settings:
    INERTIA_JSON_ENCODER = InertiaJsonEncoder
    INERTIA_ENCRYPT_HISTORY = False
    INERTIA_SSR_ENABLED = False
    INERTIA_SSR_URL = "http://localhost:13714"
