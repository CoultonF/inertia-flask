from flask import Flask, render_template
from ..inertia_flask import  inertia_middleware, Inertia

app = Flask(__name__)
Inertia(app)
app.secret_key = 'your-secret-key'  # Required for session
inertia_middleware(app)
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
	return render_template("test.html")