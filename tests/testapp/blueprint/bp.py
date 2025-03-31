from flask import Blueprint

from inertia_flask import Inertia, inertia

bp = Blueprint("bp", __name__, template_folder="templates")
inertia_ext = Inertia()
inertia_ext.init_app(bp)


@bp.route("/blueprint")
@inertia("component")
def bp_page():
    return {"page": "blueprint"}
