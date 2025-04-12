from datetime import datetime
from random import randint

from flask import Flask
from flask_seasurf import SeaSurf
from flask_sqlalchemy import SQLAlchemy
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from inertia_flask import Inertia, defer, inertia


class Base(DeclarativeBase):
    """subclasses will be converted to dataclasses"""


db = SQLAlchemy(model_class=Base)
inertia_ext = Inertia()
csrf = SeaSurf()
app = Flask(__name__, static_folder="static")
app.secret_key = "your-secret-key"  # Required for session
app.config["INERTIA_TEMPLATE"] = "base.html"
app.config["INERTIA_SSR_TEMPLATE"] = "base.html"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
db.init_app(app)
csrf.init_app(app)
inertia_ext.init_app(app)
inertia_ext.share("auth", lambda: {"user": "John Doe"})
app.config["INERTIA_ROOT"] = "app"
app.config["INERTIA_VITE_STATIC"] = "static"
app.config["INERTIA_VITE_DIR"] = "react"
app.config["INERTIA_SSR_ENABLED"] = True

inertia_ext.add_shorthand_route(app, "/test", "test")


class PostModel(BaseModel):
    post_id: int
    title: str
    content: str
    created_at: datetime
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
@inertia("component")
def hello_world():
    def get_posts():
        posts = db.session.execute(db.select(Posts)).scalars().all()
        return [PostModel.model_validate(post).model_dump() for post in posts]

    # post = Posts.query.first()
    return {
        "value": 1,
        "defer": defer(get_posts, group="test"),
        "other": defer(lambda: [f"{randint(1, 9)}"], group="test", merge=True),
    }


def main():
    init_db()
    app.run(debug=True)


if __name__ == "__main__":
    main()
