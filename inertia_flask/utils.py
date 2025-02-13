import json
import warnings

from sqlalchemy.ext.declarative import DeclarativeMeta

from .prop_classes import DeferredProp, MergeProp, OptionalProp


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # Convert SQLAlchemy model to dictionary
            fields = {}
            for field in [
                x for x in dir(obj) if not x.startswith("_") and x != "metadata"
            ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            return fields
        return json.JSONEncoder.default(self, obj)


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
