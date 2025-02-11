import warnings

# from django.core.serializers.json import DjangoJSONEncoder
# from django.db import models
# from django.db.models.query import QuerySet
# from django.forms.models import model_to_dict as base_model_to_dict

from dataclasses import is_dataclass, asdict
from json import JSONEncoder
from .prop_classes import DeferredProp, MergeProp, OptionalProp


class InertiaJsonEncoder(JSONEncoder):
    def default(self, value):
        if is_dataclass(value):
            return asdict(value)

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