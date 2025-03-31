from time import sleep

from flask import Blueprint, Flask

from inertia_flask import Inertia, clear_history, defer, encrypt_history, inertia, merge
from tests.testapp.blueprint.bp import bp


def create_blueprint():
    app = Flask(__name__)
    app.config["TESTING"] = True  # Enable testing mode
    app.config["SECRET_KEY"] = "your-secret-key"  # Required for session
    app.config["INERTIA_TEMPLATE"] = "base.html"
    app.config["BP_INERTIA_TEMPLATE"] = "blueprint.html"
    app.register_blueprint(bp)

    return app


def create_share_app():
    inertia_ext = Inertia()
    app = Flask(__name__)
    app.config["TESTING"] = True  # Enable testing mode
    app.config["SECRET_KEY"] = "your-secret-key"  # Required for session
    app.config["INERTIA_TEMPLATE"] = "base.html"
    inertia_ext.init_app(app)
    inertia_ext.share("auth", lambda: {"user_id": "123"})

    def get_email():
        sleep(0.1)
        return "alice@wonderland.com"

    @app.route("/share")
    @inertia("component")
    def defer_page():
        return {"name": "Alice", "email": defer(get_email)}

    return app


def create_app():
    inertia_ext = Inertia()
    app = Flask(__name__)
    app.config["TESTING"] = True  # Enable testing mode
    app.config["SECRET_KEY"] = "your-secret-key"  # Required for session
    app.config["INERTIA_TEMPLATE"] = "base.html"
    inertia_ext.init_app(app)

    # Register routes

    inertia_ext.add_shorthand_route(app, "/shorthand", "component")

    def get_email():
        sleep(0.1)
        return "alice@wonderland.com"

    def get_phone():
        sleep(0.1)
        return "1234567890"

    @app.route("/")
    @inertia("component")
    def root():
        return {"name": "Alice"}

    @app.route("/defer")
    @inertia("component")
    def defer_page():
        return {"name": "Alice", "email": defer(get_email)}

    @app.route("/group")
    @inertia("component")
    def deferred_group():
        return {
            "name": "Alice",
            "email": defer(get_email, group="contact"),
            "phone": defer(get_phone, group="contact"),
        }

    @app.route("/defer-merge")
    @inertia("defer-merge")
    def deferred_merge():
        return {
            "name": "Jane Doe",
            "defer-merge": defer(lambda: ["1"], merge=True),
        }

    @app.route("/merge")
    @inertia("component")
    def merge_props():
        return {
            "numbers": merge([1]),
        }

    @app.route("/encrypt-decorator")
    @inertia("component", encrypt=True)
    def encrypt_decorator():
        return {}

    @app.route("/clear-function")
    @inertia("component")
    def clear_function():
        clear_history()
        return {}

    @app.route("/clear-decorator")
    @inertia("component", clear=True)
    def clear_decorator():
        return {}

    @app.route("/encrypt-function")
    @inertia("component")
    def encrypt_function():
        encrypt_history()
        return {}

    bp_flask = Blueprint("bp", __name__, template_folder="templates")

    @bp_flask.route("/blueprint")
    @inertia("component")
    def bp_page():
        return {"page": "blueprint"}

    return app


def run_app():
    app = create_app()
    app.run(debug=True)


def run_blueprint():
    app = create_blueprint()
    app.run(debug=True)


if __name__ == "__main__":
    run_blueprint()
