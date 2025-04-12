from datetime import datetime

from flask import Flask
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from examples.blueprint.blueprints.my_blueprint import bp
from inertia_flask import inertia


class Base(DeclarativeBase):
    """subclasses will be converted to dataclasses"""


db = SQLAlchemy(model_class=Base)
csrf = SeaSurf()
app = Flask(__name__)
app.register_blueprint(bp)
app.secret_key = "your-secret-key"  # Required for session
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
db.init_app(app)
csrf.init_app(app)
app.config["INERTIA_ROOT"] = "app"
app.config["INERTIA_TEMPLATE"] = "base.html"
app.config["BP_INERTIA_TEMPLATE"] = "blueprint.html"
app.config["INERTIA_STATIC_ENDPOINT"] = "bp.static"
app.config["INERTIA_VITE_DIR"] = "react"
app.config["INERTIA_VITE_MANIFEST_PATH"] = "react/dist/manifest.json"


class PostModel(BaseModel):
    post_id: int
    title: str
    content: str
    reated_at: datetime
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class Posts(db.Model):
    __tablename__ = "posts"
    post_id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)


# Create tables and insert sample data
def init_db():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Check if we already have data
        if not Posts.query.first():
            sample_post = Posts(
                title="Hello SQLite",
                content="This is a test post stored in our SQLite database!",
            )
            db.session.add(sample_post)
            db.session.commit()


@app.route("/")
def hello_world():
    return "Hello from Flask!"


@app.route("/nobp")
@inertia("component")
def test_route():
    return {"data": 1}


def main():
    init_db()
    app.run(debug=True)


if __name__ == "__main__":
    main()
