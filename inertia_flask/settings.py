import json

class Settings:
    def __init__(self):
        self.INERTIA_VERSION = "1.0"
        self.INERTIA_LAYOUT = None
        self.INERTIA_JSON_ENCODER = json.JSONEncoder
        self.INERTIA_ENCRYPT_HISTORY = False

settings = Settings()