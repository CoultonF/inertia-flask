"A blueprint template example"

from flask import Blueprint

from inertia_flask import Inertia, inertia

# Create blueprint
bp = Blueprint("bp", __name__, template_folder="templates")
inertia_ext = Inertia()
inertia_ext.init_app(bp)


@bp.route("/blueprint")
@inertia("component")
def dashboard():
    "Example blueprint route"
    return {"message": "Welcome to the blueprint!"}
