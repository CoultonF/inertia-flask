from flask import Blueprint

bp = Blueprint("simple_page", __name__, template_folder="templates")


@bp.route("/bp")
def bp_page():
    return {"page": "blueprint"}
