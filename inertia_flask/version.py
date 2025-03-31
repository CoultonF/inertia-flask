import hashlib
import os

from flask import current_app
from jinja2.exceptions import TemplateNotFound

from .utils import get_template_name


def get_asset_version(blueprint=None) -> str:
    """Calculate asset version to allow Inertia to automatically make a full page visit in case of changes."""
    blueprint_class = (
        current_app.blueprints[blueprint] if blueprint is not None else None
    )
    template_name = get_template_name(blueprint_class)

    try:
        # Method 1: Hash the template source
        loader = current_app.jinja_env.loader
        if loader is None:
            return ""

        # Get the template source and its last modified timestamp
        source, filename, uptodate = loader.get_source(
            current_app.jinja_env, template_name
        )

        # If we have a filename, include its modification time in the hash
        if filename:
            mtime = str(os.path.getmtime(filename))
            content = f"{source}{mtime}"
        else:
            content = source

        # Create hash using both content and modification time
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    except TemplateNotFound as e:
        current_app.logger.error(f"Failed to get template bytes: {e}")
        return ""
