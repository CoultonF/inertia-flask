from flask import Flask, render_template
from ..inertia_flask import  inertia_middleware, Inertia, render_inertia

app = Flask(__name__)
Inertia(app)
app.secret_key = 'your-secret-key'  # Required for session
app.config['INERTIA_TEMPLATE'] = "base.html"
inertia_middleware(app)
@app.route("/")
def hello_world():
    return render_inertia('component')

@app.route("/test")
def test():
	return render_template("test.html")