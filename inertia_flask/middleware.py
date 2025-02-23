import json
from typing import Optional, Union

from flask import Blueprint, Flask, current_app, request, session
from flask.app import App
from flask.blueprints import BlueprintSetupState
from werkzeug.wrappers import Response

from .http import encrypt_history, render
from .settings import Settings
from .version import get_asset_version


class Inertia:
    def __init__(self, app: Optional[Union[Flask, Blueprint]] = None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app, encrypt=False):
        app.config.from_object(Settings)
        self.app = app
        self.encrypt = encrypt
        if isinstance(app, Flask):
            self._init_extension(app)
        elif isinstance(app, Blueprint):
            blueprint = app
            # Register the extension once the blueprint is registered
            blueprint.record_once(self.register_blueprint)
        if encrypt:
            app.before_request(lambda: encrypt_history(encrypt))
        app.context_processor(self.vite_processor)
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
        if self.encrypt:
            encrypt_history(self.encrypt)

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

    def add_shorthand_route(
        self,
        url: str,
        component_name: str,
        endpoint: Optional[str] = None,
        encrypt=None,
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

        def route_render(component_name):
            if encrypt is not None:
                encrypt_history(encrypt)
            return render(request, component_name)

        self.app.add_url_rule(
            url,
            endpoint or component_name.lower(),
            lambda: route_render(component_name),
        )

    def vite_processor(self):
        flask_debug = current_app.config["DEBUG"]
        vite_origin = current_app.config["VITE_ORIGIN"]
        vite_dist = current_app.config["VITE_DIST"]
        is_debug = flask_debug == "1"

        def dev_asset(file_path, _):
            return f"{vite_origin}/{file_path}"

        def prod_asset(file_path, manifest_path):
            manifest = {}
            try:
                with open(manifest_path, encoding="utf-8") as content:
                    manifest = json.load(content)
                return f"{vite_dist}/{manifest[file_path]['file']}"
            except OSError as exception:
                raise OSError(
                    f"Manifest file not found at {manifest_path}. Run `npm run build`."
                ) from exception

        def vite_react_refresh():
            return f"""
                <script type="module">
                import RefreshRuntime from '{vite_origin}/@react-refresh'
                RefreshRuntime.injectIntoGlobalHook(window)
                window.$RefreshReg$ = () => {{}}
                window.$RefreshSig$ = () => (type) => type
                window.__vite_plugin_react_preamble_installed__ = true
                </script>
            """

        def vite_hmr():
            return f"""
                <script type="module" src="{vite_origin}/@vite/client"></script>
            """

        def vite_inertia(entry_file, manifest_path):
            output = ""
            if is_debug:
                output += vite_react_refresh()
                output += vite_hmr()
                output += f"""
                <script type="module" src="{dev_asset(entry_file, manifest_path)}">
                </script>
                """
            else:
                output += f"""
                <script defer src="{prod_asset(entry_file, manifest_path)}"></script>
                """

            return output

        return {
            "vite_inertia": vite_inertia,
            "vite_hmr": vite_hmr if is_debug else "",
            "vite_react_refresh": vite_react_refresh if is_debug else "",
            "vite_asset": dev_asset if is_debug else prod_asset,
            "vite_is_debug": is_debug,
        }


# Example usage of flash messages helper
def add_message(category, message):
    """
    Helper function to add flash messages that persist across Inertia requests
    """
    if "messages" not in session:
        session["messages"] = []
    session["messages"].append({"category": category, "message": message})
