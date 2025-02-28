from flask import Blueprint

from inertia_flask import Inertia, inertia

# Create blueprint
bp = Blueprint("my_blueprint", __name__, url_prefix="/admin")
inertia_ext = Inertia()
inertia_ext.init_app(bp)


@bp.route("/blueprint")
@inertia("test")
def dashboard():
    return {"message": "Welcome to the blueprint!"}
