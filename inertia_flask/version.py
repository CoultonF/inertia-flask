import hashlib

from flask import current_app

from .utils import get_template_name


def get_asset_version(blueprint=None) -> str:
    """Calculate asset version to allow Inertia to automatically make a full page visit in case of changes."""
    blueprint_class = (
        current_app.blueprints[blueprint] if blueprint is not None else None
    )
    template_name = get_template_name(blueprint_class)
    template = current_app.jinja_env.get_template(template_name)
    try:
        # Get the raw template source without rendering
        template_bytes = template.source.encode("utf-8")
        return hashlib.sha256(template_bytes).hexdigest()
    except Exception as e:
        current_app.logger.error(f"Failed to get template bytes: {e}")
        return ""
