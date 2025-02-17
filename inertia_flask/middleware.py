import secrets
from typing import Optional

from flask import Blueprint, Flask, request, session
from flask.app import App
from flask.blueprints import BlueprintSetupState
from werkzeug.wrappers import Response

from .http import render
from .version import get_asset_version


class Inertia:
    def __init__(self, app: Optional[Flask] = None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        if isinstance(app, Flask):
            self._init_extension(app)
        elif isinstance(app, Blueprint):
            blueprint = app
            # Register the extension once the blueprint is registered
            blueprint.record_once(self.register_blueprint)
        app.before_request(self.before_request)
        app.after_request(self.after_request)

    def register_blueprint(self, state: BlueprintSetupState):
        self._init_extension(state.app)

    def _init_extension(self, app: App):
        """Store a reference to the extension in the app's extensions."""
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["inertia"] = self

    def before_request(self):
        # Generate CSRF token if it doesn't exist
        if "csrf_token" not in session:
            session["csrf_token"] = self.generate_csrf_token()

    def after_request(self, response):
        if not self.is_inertia_request():
            return response

        if self.is_non_post_redirect(response):
            response.status_code = 303

        if self.is_stale():
            return self.force_refresh()

        return response

    def is_non_post_redirect(self, response):
        return self.is_redirect_request(response) and request.method in [
            "PUT",
            "PATCH",
            "DELETE",
        ]

    def is_inertia_request(self):
        return "X-Inertia" in request.headers

    def is_redirect_request(self, response):
        return response.status_code in [301, 302]

    def is_stale(self):
        return (
            request.headers.get("X-Inertia-Version", get_asset_version())
            != get_asset_version()
        )

    def is_stale_inertia_get(self):
        return request.method == "GET" and self.is_stale()

    def force_refresh(self):
        # Store flash messages for the next request
        if "messages" in session:
            session["_messages"] = session["messages"]
            del session["messages"]

        return Response("", status=409, headers={"X-Inertia-Location": request.url})

    def generate_csrf_token(self):
        # Generate a random token - in a real app you might want to use
        # Flask-WTF or another CSRF library

        return secrets.token_hex(32)

    def add_shorthand_route(
        self, url: str, component_name: str, endpoint: Optional[str] = None
    ) -> None:
        """Connect a URL rule to a frontend component that does not need a controller.

        This url does not have dedicated python source code but is linked to a JS component,
        (i.e. a frontend component which does not need props nor view_data).

        :param url: The URL rule as string as used in ``flask.add_url_rule``
        :param component_name: Your frontend component name
        :param endpoint: The endpoint for the registered URL rule. (by default
        ``component_name`` in lower case)
        """
        if not self.app:
            raise RuntimeError("Extension has not been initialized correctly.")

        self.app.add_url_rule(
            url,
            endpoint or component_name.lower(),
            lambda: render(request, component_name),
        )


# Example usage of flash messages helper
def add_message(category, message):
    """
    Helper function to add flash messages that persist across Inertia requests
    """
    if "messages" not in session:
        session["messages"] = []
    session["messages"].append({"category": category, "message": message})
