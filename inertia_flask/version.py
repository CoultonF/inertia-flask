import hashlib
import os

from flask import current_app, request


def get_asset_version() -> str:
    """Calculate asset version to allow Inertia to automatically make a full page visit in case of changes."""
    template_path = os.path.join(
        current_app.root_path,
        *(
            current_app.blueprints[request.blueprint].name,
            current_app.blueprints[request.blueprint].template_folder
        ) if request.blueprint is not None
        else current_app.template_folder,
        current_app.config["INERTIA_TEMPLATE"],
    )
    with open(template_path, "rb") as template_file:
        bytes_content = template_file.read()

    return hashlib.sha256(bytes_content).hexdigest()
