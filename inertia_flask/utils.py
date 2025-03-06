import json
import warnings

from flask import current_app
from jinja2 import TemplateNotFound

from .prop_classes import DeferredProp, MergeProp, OptionalProp


class InertiaJsonEncoder(json.JSONEncoder):
    def default(self, value):
        return super().default(value)


def lazy(prop):
    warnings.warn(
        "lazy is deprecated and will be removed in a future version. Please use optional instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return optional(prop)


def optional(prop):
    return OptionalProp(prop)


def defer(prop, group="default", merge=False):
    return DeferredProp(prop, group=group, merge=merge)


def merge(prop):
    return MergeProp(prop)


def template_exists(template_name):
    try:
        current_app.jinja_env.get_template(template_name)
        return True
        # Try to get the template
    except TemplateNotFound:
        return False


def get_template_name(blueprint=None):
    if blueprint is not None:
        bp_template = current_app.config.get(
            f"{str(blueprint.name).upper() + '_' if blueprint is not None else ''}INERTIA_TEMPLATE",
        ) or current_app.config.get("INERTIA_TEMPLATE")
        if template_exists(bp_template):
            return bp_template
        else:
            return current_app.config.get("INERTIA_TEMPLATE")
    else:
        return current_app.config.get("INERTIA_TEMPLATE")
