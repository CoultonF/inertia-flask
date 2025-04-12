from .utils import InertiaJsonEncoder


class Settings:
    """Default Inertia Flask settings.
    These settings can be overridden by setting them in your Flask app's config.
    """

    INERTIA_JSON_ENCODER = InertiaJsonEncoder
    INERTIA_ENCRYPT_HISTORY = False
    INERTIA_SSR_ENABLED = False
    INERTIA_SSR_URL = "http://localhost:13714"
    INERTIA_ROOT = "app"
    INERTIA_STATIC_ENDPOINT = "static"
    INERTIA_VITE_ORIGIN = "http://localhost:5173"
    INERTIA_VITE_MANIFEST_PATH = None
    INERTIA_VITE_SSR_MANIFEST_PATH = None
    INERTIA_VITE_DIR = "inertia"


def init_settings(app):
    """Initialize Inertia settings while preserving existing app configurations."""
    defaults = {
        key: value for key, value in vars(Settings).items() if not key.startswith("_")
    }

    # Only set values that aren't already in app.config
    for key, value in defaults.items():
        if key not in app.config:
            app.config[key] = value
