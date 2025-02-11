from .utils import InertiaJsonEncoder


class Settings(object):
    INERTIA_LAYOUT = None
    INERTIA_JSON_ENCODER = InertiaJsonEncoder
    INERTIA_ENCRYPT_HISTORY = False


settings = Settings()
