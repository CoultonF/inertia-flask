from flask import Flask

from inertia_flask import inertia, inertia_middleware


def create_app():
    app = Flask(__name__)
    app.config["TESTING"] = True  # Enable testing mode
    app.config["SECRET_KEY"] = "your-secret-key"  # Required for session
    app.config["INERTIA_TEMPLATE"] = "base.html"
    inertia_middleware(app)

    # Register routes
    @app.route("/")
    @inertia("component")
    def home():
        return {"name": "John Doe"}

    return app


def run_app():
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    run_app()
