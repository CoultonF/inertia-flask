import json
from functools import wraps
from http import HTTPStatus
from typing import Optional

from flask import (
    Response,
    current_app,
    has_app_context,
    render_template,
    render_template_string,
    request,
    session,
)
from markupsafe import Markup

from .helpers import deep_transform_callables, validate_type
from .prop_classes import DeferredProp, IgnoreOnFirstLoadProp, MergeableProp
from .settings import settings
from .version import get_asset_version

INERTIA_REQUEST_ENCRYPT_HISTORY = "_inertia_encrypt_history"
INERTIA_SESSION_CLEAR_HISTORY = "_inertia_clear_history"
INERTIA_TEMPLATE = "inertia.html"
INERTIA_ROOT = "root"


class InertiaRequest:
    def __init__(self, flask_request):
        self.flask_request = flask_request

    @property
    def headers(self):
        return self.flask_request.headers

    @property
    def inertia(self):
        return getattr(self.flask_request, "inertia", {})

    def is_a_partial_render(self, component):
        return (
            "X-Inertia-Partial-Data" in self.headers
            and self.headers.get("X-Inertia-Partial-Component", "") == component
        )

    def partial_keys(self):
        return self.headers.get("X-Inertia-Partial-Data", "").split(",")

    def reset_keys(self):
        return self.headers.get("X-Inertia-Reset", "").split(",")

    def is_inertia(self):
        return "X-Inertia" in self.headers

    def should_encrypt_history(self):
        return validate_type(
            getattr(
                self.flask_request,
                INERTIA_REQUEST_ENCRYPT_HISTORY,
                settings.INERTIA_ENCRYPT_HISTORY,
            ),
            expected_type=bool,
            name="encrypt_history",
        )

    def get_full_path(self):
        full_path = self.flask_request.full_path
        if full_path.endswith("?"):
            full_path = full_path[:-1]
        return full_path


class BaseInertiaResponseMixin:
    def page_data(self):
        clear_history = session.pop(INERTIA_SESSION_CLEAR_HISTORY, False)

        _page = {
            "component": self.component,
            "props": self.build_props(),
            "url": self.request.get_full_path(),
            "version": get_asset_version(),
            "encryptHistory": self.request.should_encrypt_history(),
            "clearHistory": clear_history,
        }

        _deferred_props = self.build_deferred_props()
        if _deferred_props:
            _page["deferredProps"] = _deferred_props

        _merge_props = self.build_merge_props()
        if _merge_props:
            _page["mergeProps"] = _merge_props

        return _page

    def build_props(self):
        _props = {
            **self.request.inertia,
            **self.props,
        }

        for key in list(_props.keys()):
            if self.request.is_a_partial_render(self.component):
                if key not in self.request.partial_keys():
                    del _props[key]
            else:
                if isinstance(_props[key], IgnoreOnFirstLoadProp):
                    del _props[key]

        return deep_transform_callables(_props)

    def build_deferred_props(self):
        if self.request.is_a_partial_render(self.component):
            return None

        _deferred_props = {}
        for key, prop in self.props.items():
            if isinstance(prop, DeferredProp):
                _deferred_props.setdefault(prop.group, []).append(key)

        return _deferred_props

    def build_merge_props(self):
        return [
            key
            for key, prop in self.props.items()
            if (
                isinstance(prop, MergeableProp)
                and prop.should_merge()
                and key not in self.request.reset_keys()
            )
        ]

    def build_first_load(self, data):
        inertia_div = Markup(
            render_template_string(
                f"""
                <div
                id="{current_app.config.get("INERTIA_ROOT", INERTIA_ROOT)}"
                data-page="{{{{ page|escape }}}}"></div>
                """,
                page=data,
            )
        )
        return render_template(
            current_app.config.get("INERTIA_TEMPLATE", INERTIA_TEMPLATE),
            page=data,
            inertia=inertia_div,
            **self.template_data,
        )


class InertiaResponse(BaseInertiaResponseMixin, Response):
    def __init__(
        self,
        request,
        component,
        props=None,
        template_data=None,
        headers=None,
        *args,
        **kwargs,
    ):
        self.request = InertiaRequest(request)
        self.component = component
        self.props = props or {}
        self.template_data = template_data or {}
        self.json_encoder = settings.INERTIA_JSON_ENCODER
        _headers = headers or {}

        data = json.dumps(self.page_data(), cls=self.json_encoder, default=str)

        if self.request.is_inertia():
            _headers = {
                **_headers,
                "Vary": "X-Inertia",
                "X-Inertia": "true",
                "Content-Type": "application/json",
            }
            content = data
        else:
            content = self.build_first_load(data)

        super().__init__(content, headers=_headers, *args, **kwargs)


def inertia(component):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if the current app has the Inertia middleware initialized
            if not has_app_context() or "inertia" not in current_app.extensions:
                raise RuntimeError(
                    "Inertia middleware is not initialized in the current app context."
                )
            props = f(*args, **kwargs)

            # If something other than a dict is returned, return it directly
            if not isinstance(props, dict):
                return props

            return InertiaResponse(request, component, props)

        return decorated_function

    return decorator


def render(request, component, props=None, template_data=None):
    return InertiaResponse(request, component, props or {}, template_data or {})


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
        lambda: render_inertia(component_name),
    )


def location(url):
    return Response(
        "",
        status=HTTPStatus.CONFLICT,
        headers={"X-Inertia-Location": url},
    )


def encrypt_history(value=True):
    setattr(request, INERTIA_REQUEST_ENCRYPT_HISTORY, value)


def clear_history():
    session[INERTIA_SESSION_CLEAR_HISTORY] = True
