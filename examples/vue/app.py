from flask import Flask
from inertia_flask import Inertia, inertia

inertia_ext = Inertia()
app = Flask(__name__, 
            static_folder="public",
            template_folder="templates", 
            static_url_path="/public")
app.secret_key = "your-secret-key" 
app.config["INERTIA_TEMPLATE"] = "base.html"
app.config["INERTIA_VITE_CLIENT"] = "client"
app.config["INERTIA_VITE_SERVER"] = "server"
app.config["INERTIA_VITE_STATIC"] = "static"
app.config["INERTIA_VITE_DIR"] = "vue"

app.config.from_object(__name__)
inertia_ext.init_app(app)

@app.route("/")
@inertia("Index")
def index():
    return {"data": 42}

@app.route("/about")
@inertia("About")
def about():
    return {
        "version": "1.0.0"
    }

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
