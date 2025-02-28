import json
import os
from typing import Optional, Union

import requests
from flask import Blueprint, Flask, current_app, request, session, url_for
from flask.app import App
from flask.blueprints import BlueprintSetupState
from werkzeug.wrappers import Response

from .cli import InertiaCommands
from .http import encrypt_history, render
from .settings import Settings
from .version import get_asset_version


class Inertia:
    def __init__(self, app: Optional[Union[Flask, Blueprint]] = None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app, encrypt=False):
        self.app = app
        self.encrypt = encrypt
        if isinstance(app, Flask):
            cli = InertiaCommands(self)
            app.config.from_object(Settings)
            self._init_extension(app)
            cli.register_as_flask(app)
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
        state.app.config.from_object(Settings)
        cli = InertiaCommands(self, state.app)
        self._init_extension(state.app)
        cli.register_as_blueprint(self.app)

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
        flask_debug = current_app.config.get("DEBUG", False)
        vite_origin = current_app.config.get("VITE_ORIGIN", "http://localhost:5173")
        vite_static = current_app.config.get("VITE_STATIC", "static")
        vite_client = current_app.config.get("VITE_CLIENT", "client")
        vite_manifest = current_app.config.get("VITE_MANIFEST", "manifest.json")
        is_debug = flask_debug is True
        ssr_enabled = current_app.config.get("INERTIA_SSR_ENABLED", False)

        # Detect if Vite dev server is running
        vite_dev_server_running = False
        if is_debug:
            try:
                response = requests.get(f"{vite_origin}/@vite/client", timeout=0.1)
                vite_dev_server_running = response.status_code == 200
            except:
                vite_dev_server_running = False

        def dev_asset(file_path, _=None):
            return f"{vite_origin}/{file_path}"

        def prod_asset(file_path, manifest_path=None):
            manifest = {}
            manifest_path = os.path.join(
                self.app.root_path, vite_static, vite_client, vite_manifest
            )

            try:
                with open(f"{manifest_path}", encoding="utf-8") as content:
                    manifest = json.load(content)
                    if file_path in manifest:
                        url_path = manifest[file_path]["file"]
                        return url_for(
                            vite_static, filename=f"{vite_client}/{url_path}"
                        )
                    else:
                        current_app.logger.warning(
                            f"Asset {file_path} not found in manifest"
                        )
                        return url_for(
                            vite_static, filename=f"{vite_client}/{file_path}"
                        )
            except OSError as exception:
                current_app.logger.error(
                    f"Manifest file not found at {manifest_path}. Run `npm run build`."
                )
                # Fallback to direct path in development
                if is_debug:
                    return url_for(vite_static, filename=f"{vite_client}/{file_path}")
                raise OSError(
                    "Manifest file not found. Run `npm run build`."
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

        def vite_inertia(entry_file, manifest_path=None):
            output = ""
            if is_debug and vite_dev_server_running:
                output += vite_react_refresh()
                output += vite_hmr()
                output += f"""
                <script type="module" src="{dev_asset(entry_file, manifest_path)}">
                </script>
                """
            else:
                # Use production assets even in debug mode if Vite server isn't running
                css_files = []
                try:
                    manifest_path = os.path.join(
                        self.app.root_path, vite_static, vite_client, vite_manifest
                    )
                    with open(f"{manifest_path}", encoding="utf-8") as content:
                        manifest = json.load(content)
                        if entry_file in manifest and "css" in manifest[entry_file]:
                            css_files = manifest[entry_file]["css"]
                except:
                    pass

                # Include CSS files
                for css_file in css_files:
                    output += f"""
                    <link rel="stylesheet" href="{url_for(vite_static, filename=f"{vite_client}/{css_file}")}">
                    """

                # Include JS
                output += f"""
                <script type="module" src="{prod_asset(entry_file, manifest_path)}"></script>
                """

            return output

        return {
            "vite_inertia": vite_inertia,
            "vite_hmr": vite_hmr
            if is_debug and vite_dev_server_running
            else lambda: "",
            "vite_react_refresh": vite_react_refresh
            if is_debug and vite_dev_server_running
            else lambda: "",
            "vite_asset": dev_asset
            if is_debug and vite_dev_server_running
            else prod_asset,
            "vite_is_debug": is_debug,
            "vite_dev_server_running": vite_dev_server_running,
        }


# Example usage of flash messages helper
def add_message(category, message):
    """
    Helper function to add flash messages that persist across Inertia requests
    """
    if "messages" not in session:
        session["messages"] = []
    session["messages"].append({"category": category, "message": message})
