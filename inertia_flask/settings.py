from .utils import InertiaJsonEncoder


class Settings:
    INERTIA_JSON_ENCODER = InertiaJsonEncoder
    INERTIA_ENCRYPT_HISTORY = False
    INERTIA_SSR_ENABLED = False
    INERTIA_SSR_URL = "http://localhost:13714"
    INERTIA_ROOT = "app"
    VITE_ORIGIN = "http://localhost:5173"
    VITE_CLIENT = "client"
    VITE_SERVER = "server"
    VITE_MANIFEST = "manifest.json"
    VITE_SSR_MANIFEST = "manifest.json"
    VITE_STATIC = "static"
    VITE_DIR = "inertia"
