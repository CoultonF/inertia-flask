from .utils import InertiaCsrf, InertiaJsonEncoder


class Settings:
    INERTIA_JSON_ENCODER = InertiaJsonEncoder
    INERTIA_ENCRYPT_HISTORY = False
    INERTIA_CSRF_CLASS = InertiaCsrf


settings = Settings()
