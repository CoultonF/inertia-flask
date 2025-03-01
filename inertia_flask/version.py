import hashlib
import os

from flask import current_app


def get_asset_version(blueprint=None) -> str:
    # TODO make compatible with blueprints
    """Calculate asset version to allow Inertia to automatically make a full page visit in case of changes."""
    template_folder = current_app.template_folder
    root_path = current_app.root_path
    if blueprint is not None:
        template_folder = current_app[blueprint].template_folder
        root_path = current_app[blueprint].root_path

    template_path = os.path.join(
        root_path,
        template_folder,
        current_app.config["INERTIA_TEMPLATE"],
    )
    with open(template_path, "rb") as template_file:
        bytes_content = template_file.read()

    return hashlib.sha256(bytes_content).hexdigest()
