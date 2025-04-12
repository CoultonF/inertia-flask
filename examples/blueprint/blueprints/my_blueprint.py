"A blueprint template example"

from flask import Blueprint

from inertia_flask import Inertia, inertia

# Create blueprint
bp = Blueprint(
    "bp",
    __name__,
    template_folder="bp_templates",
    static_folder="../react/dist",
)
inertia_ext = Inertia()
inertia_ext.init_app(bp)


@bp.route("/blueprint")
@inertia("component")
def dashboard():
    "Example blueprint route"
    return {"value": "1"}
