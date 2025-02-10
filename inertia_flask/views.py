from http import HTTPStatus
from typing import Any, Dict

from flask import Response, abort, current_app, jsonify, render_template, request

from .version import get_asset_version


def render_inertia(
    component_name: str,
    props: Dict[str, Any] = {},
    view_data: Dict[str, Any] = {},
) -> Response:
    """Method to use instead of Flask `render_template`.

    Returns either a JSON response or a HTML response including a JSON encoded inertia
    page object according to Inertia request headers.

    .. code-block:: python

       from flask_inertia import render_inertia

       app = Flask(__name__)

       @app.route("/")
       def index():
           data = {
               "username": "foo",
               "login": "bar",
           }
           return render_inertia(
               component_name="Index",  # this must exists in your frontend
               props=data,  # optional
               view_data={"description": "FooBar"},  # optional
           )

    :param component_name: The component name used in your frontend framework
    :param props: A dict of properties used in your component
    :param view_data: A dict of data that will not be sent to your JavaScript component
    """
    inertia_template = current_app.config.get("INERTIA_TEMPLATE")
    if inertia_template is None:
        abort(
            400,
            "No Inertia template found. Set INERTIA_TEMPLATE in config",
        )

    inertia_version = get_asset_version()
    refresh_props = request.headers.getlist("X-Inertia-Partial-Data")
    if len(refresh_props) == 1 and "," in refresh_props[0]:
        refresh_props = list(
            filter(
                None, request.headers.get("X-Inertia-Partial-Data", "").split(",")
            )
        )
    if (
        refresh_props
        and request.headers.get("X-Inertia-Partial-Component", "") == component_name
    ):
        props = {
            key: value
            for key, value in props.items()
            if key in refresh_props or isinstance(value, AlwaysProp)
        }
    else:
        props = {
            key: value
            for key, value in props.items()
            if not callable(value) or not isinstance(value, LazyProp)
        }

    extension = current_app.extensions["inertia"]
    merged_props = {**props, **extension._shared_data}
    for key, value in merged_props.items():
        if callable(value):
            merged_props[key] = value()
        else:
            merged_props[key] = value

    if request.headers.get("X-Inertia", False):
        response = jsonify(
            {
                "component": component_name,
                "props": merged_props,
                "version": inertia_version,
                "url": request.url,
            }
        )
        response.headers["X-Inertia"] = True
        response.headers["Vary"] = "Accept"
        return response

    context = {
        "view_data": view_data,
        "page": {
            "version": inertia_version,
            "url": request.url,
            "component": component_name,
            "props": merged_props,
        },
    }

    return render_template(inertia_template, **context)


def inertia_location(location: str) -> Response:
    """Redirects to an external website, or even another non-Inertia endpoint.

    Returns a server-side initiated window.location visit.

    This method will generate a 409 Conflict response and include the destination
    URL in the X-Inertia-Location header. When this response is received
    client-side, Inertia will automatically perform a window.location = url visit.

    .. code-block:: python

       from flask_inertia import inertia_location

       app = Flask(__name__)

       @app.route("/")
       def index():
           return inertia_location("http"//www.foobar.com/")

    :param location: External location
    """
    response = Response("Inertia server side redirect", status=HTTPStatus.CONFLICT)
    response.headers["X-Inertia-Location"] = location
    return response