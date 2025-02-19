import json
import warnings

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
