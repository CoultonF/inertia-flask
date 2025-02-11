from flask import Flask
from inertia_flask import inertia_middleware, inertia

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for session
app.config["INERTIA_TEMPLATE"] = "base.html"
inertia_middleware(app)


@app.route("/")
@inertia("component")
def hello_world():
    return {"value": 1}


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
