from http import HTTPStatus
from typing import Any, Optional

from flask import Blueprint, Flask, Response, current_app, request
from flask.app import App
from flask.blueprints import BlueprintSetupState
from werkzeug.exceptions import BadRequest

from .version import get_asset_version


class Inertia:
    """Inertia Plugin for Flask."""

    def __init__(self, app: Optional[Flask | Blueprint] = None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask | Blueprint):
        """Init as an app extension

        * Register before_request hook
        * Register after_request hook
        * Set context processor to have an `inertia` value in templates
        """
        self.app = app
        self._shared_data = {}
        if isinstance(app, Flask):
            self._init_extension(app)
        elif isinstance(app, Blueprint):
            blueprint = app
            # Register the extension once the blueprint is registered
            blueprint.record_once(self.register_blueprint)
        app.context_processor(self.context_processor)
        app.before_request(self.process_incoming_inertia_requests)
        app.after_request(self.update_redirect)

    def register_blueprint(self, state: BlueprintSetupState):
        """Register a blueprint."""
        self._init_extension(state.app)

    def _init_extension(self, app: App):
        """Store a reference to the extension in the app's extensions."""
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["inertia"] = self

    def process_incoming_inertia_requests(self) -> Optional[Response]:
        """Process incoming Inertia requests.

        AJAX requests must be forged by Inertia.

        Whenever an Inertia request is made, Inertia will include the current asset
        version in the X-Inertia-Version header. If the asset versions are the same,
        the request simply continues as expected. However, if they are different,
        the server immediately returns a 409 Conflict response (only for GET request),
        and includes the URL in a X-Inertia-Location header.
        """
        # request is ajax
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return None

        # check if send with Inertia
        if not request.headers.get("X-Inertia"):
            raise BadRequest("Inertia headers not found")

        # check inertia version
        server_version = get_asset_version()
        inertia_version = request.headers.get("X-Inertia-Version")
        if (
            request.method == "GET"
            and inertia_version
            and inertia_version != server_version
        ):
            response = Response(
                "Inertia versions does not match", status=HTTPStatus.CONFLICT
            )
            response.headers["X-Inertia-Location"] = request.full_path
            return response

        return None

    def update_redirect(self, response: Response) -> Response:
        """Update redirect to set 303 status code.

        409 conflict responses are only sent for GET requests, and not for
        POST/PUT/PATCH/DELETE requests. That said, they will be sent in the
        event that a GET redirect occurs after one of these requests. To force
        Inertia to use a GET request after a redirect, the 303 HTTP status is used

        :param response: The generated response to update
        """
        if (
            request.method in ["PUT", "PATCH", "DELETE"]
            and response.status_code == HTTPStatus.FOUND  # 302
        ):
            response.status_code = HTTPStatus.SEE_OTHER  # 303

        return response

    def share(self, key: str, value: Any):
        """Preassign shared data for each request.

        Sometimes you need to access certain data on numerous pages within your
        application. For example, a common use-case for this is showing the
        current user in the site header. Passing this data manually in each
        response isn't practical. In these situations shared data can be useful.

        :param key: Data key to share between requests
        :param value: Data value or Function returning the data value
        """
        self._shared_data[key] = value

    @staticmethod
    def context_processor():
        """Add an `inertia` directive to Jinja2 template to allow router inclusion

        .. code-block:: html

           <head>
             <script lang="javascript">
               {{ inertia.include_router() }}
             </script>
           </head>
        """
        return {
            "inertia": current_app.extensions["inertia"],
        }
