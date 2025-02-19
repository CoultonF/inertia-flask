import hashlib
import hmac
import os
from typing import Optional
from urllib.parse import urlparse

from flask import request, session
from itsdangerous import BadData, SignatureExpired, URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest


class InertiaCsrf:
    """CSRF protection for Inertia requests."""

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Initialize CSRF protection for the Flask app."""
        app.config.setdefault("INERTIA_CSRF_ENABLED", True)
        app.config.setdefault(
            "INERTIA_CSRF_METHODS", {"POST", "PUT", "PATCH", "DELETE"}
        )
        app.config.setdefault("INERTIA_CSRF_SESSION_KEY", "csrf_token")
        app.config.setdefault("INERTIA_CSRF_HEADER", "X-CSRF-Token")
        app.config.setdefault("INERTIA_CSRF_TIME_LIMIT", 3600)
        app.config.setdefault("INERTIA_CSRF_SSL_STRICT", True)

        self.app = app

    def generate_csrf_token(self) -> str:
        """Generate a new CSRF token and store in session."""
        session_key = self.app.config["INERTIA_CSRF_SESSION_KEY"]

        if session_key not in session:
            session[session_key] = hashlib.sha1(os.urandom(64)).hexdigest()

        s = URLSafeTimedSerializer(
            self.app.config["SECRET_KEY"], salt="inertia-csrf-token"
        )

        return s.dumps(session[session_key])

    def validate_csrf_token(self, token: Optional[str] = None) -> bool:
        """Validate the CSRF token from the request."""
        if not self.app.config["INERTIA_CSRF_ENABLED"]:
            return True

        if request.method not in self.app.config["INERTIA_CSRF_METHODS"]:
            return True

        token = token or request.headers.get(self.app.config["INERTIA_CSRF_HEADER"])

        if not token:
            raise CSRFError("Missing CSRF token")

        session_key = self.app.config["INERTIA_CSRF_SESSION_KEY"]
        if session_key not in session:
            raise CSRFError("CSRF session token is missing")

        try:
            s = URLSafeTimedSerializer(
                self.app.config["SECRET_KEY"], salt="inertia-csrf-token"
            )

            token_value = s.loads(
                token, max_age=self.app.config["INERTIA_CSRF_TIME_LIMIT"]
            )
        except SignatureExpired as exc:
            raise CSRFError("CSRF token has expired") from exc
        except BadData as exc:
            raise CSRFError("Invalid CSRF token") from exc

        if not hmac.compare_digest(session[session_key], token_value):
            raise CSRFError("CSRF token mismatch")

        if request.is_secure and self.app.config["INERTIA_CSRF_SSL_STRICT"]:
            self._validate_ssl()

        return True

    def _validate_ssl(self):
        """Validate SSL requirements for CSRF protection."""
        if not request.referrer:
            raise CSRFError("Referrer header is missing")

        good_referrer = f"https://{request.host}/"
        if not self._same_origin(request.referrer, good_referrer):
            raise CSRFError("Referrer does not match host")

    def _same_origin(self, current_uri: str, compare_uri: str) -> bool:
        """Check if two URIs have the same origin."""
        current = urlparse(current_uri)
        compare = urlparse(compare_uri)

        return (
            current.scheme == compare.scheme
            and current.hostname == compare.hostname
            and current.port == compare.port
        )


class CSRFError(BadRequest):
    """Exception raised for CSRF validation failures."""

    description = "CSRF validation failed"
