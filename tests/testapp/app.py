from flask import Flask

from inertia_flask import Inertia, defer, inertia


def create_app():
    inertia_ext = Inertia()
    app = Flask(__name__)
    app.config["TESTING"] = True  # Enable testing mode
    app.config["SECRET_KEY"] = "your-secret-key"  # Required for session
    app.config["INERTIA_TEMPLATE"] = "base.html"
    inertia_ext.init_app(app)

    # Register routes

    inertia_ext.add_shorthand_route("/short", "short")

    @app.route("/")
    @inertia("component")
    def root():
        return {"name": "John Doe"}

    @app.route("/defer")
    @inertia("deferred")
    def deferred():
        return {"name": "Jane Doe", "deferred": defer(lambda: "deferred result")}

    @app.route("/defer-group")
    @inertia("defer-group")
    def deferred_group():
        return {
            "name": "Jane Doe",
            "deferred": defer(lambda: "deferred result", group="default"),
            "defer-group-value": defer(lambda: "group result 2", group="group-defer"),
            "defer-group-other": defer(lambda: "other result 2", group="group-defer"),
        }

    @app.route("/defer-merge")
    @inertia("defer-merge")
    def deferred_merge():
        return {
            "name": "Jane Doe",
            "defer-merge": defer(lambda: ["1"], merge=True),
        }

    return app


def run_app():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    run_app()
