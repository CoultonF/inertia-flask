from functools import wraps
from http import HTTPStatus
import json
from flask import request, Response, render_template, session, url_for
from .helpers import deep_transform_callables, validate_type
from .settings import settings


INERTIA_REQUEST_ENCRYPT_HISTORY = "_inertia_encrypt_history"
INERTIA_SESSION_CLEAR_HISTORY = "_inertia_clear_history"
INERTIA_TEMPLATE = "inertia.html"


class DeferredProp:
    def __init__(self, value, group="default"):
        self.value = value
        self.group = group

class IgnoreOnFirstLoadProp:
    def __init__(self, value):
        self.value = value

class MergeableProp:
    def __init__(self, value, merge=True):
        self.value = value
        self._merge = merge

    def should_merge(self):
        return self._merge

class InertiaRequest:
    def __init__(self, flask_request):
        self.flask_request = flask_request
        
    @property
    def headers(self):
        return self.flask_request.headers

    @property
    def inertia(self):
        return getattr(self.flask_request, 'inertia', {})

    def is_a_partial_render(self, component):
        return (
            "X-Inertia-Partial-Data" in self.headers and
            self.headers.get("X-Inertia-Partial-Component", "") == component
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
        return self.flask_request.full_path

class BaseInertiaResponseMixin:
    def page_data(self):
        clear_history = session.pop(INERTIA_SESSION_CLEAR_HISTORY, False)

        _page = {
            "component": self.component,
            "props": self.build_props(),
            "url": self.request.get_full_path(),
            "version": settings.INERTIA_VERSION,
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
        return render_template(
            INERTIA_TEMPLATE,
            inertia_layout=settings.INERTIA_LAYOUT,
            page=data,
            **self.template_data
        )

class InertiaResponse(BaseInertiaResponseMixin, Response):
    def __init__(self, request, component, props=None, template_data=None, headers=None, *args, **kwargs):
        self.request = InertiaRequest(request)
        self.component = component
        self.props = props or {}
        self.template_data = template_data or {}
        self.json_encoder = settings.INERTIA_JSON_ENCODER
        _headers = headers or {}

        data = json.dumps(self.page_data(), cls=self.json_encoder)
        
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
            props = f(*args, **kwargs)
            
            # If something other than a dict is returned, return it directly
            if not isinstance(props, dict):
                return props
                
            return InertiaResponse(request, component, props)
        return decorated_function
    return decorator

def render(request, component, props=None, template_data=None):
    return InertiaResponse(request, component, props or {}, template_data or {})

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