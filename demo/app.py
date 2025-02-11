from flask import Flask, jsonify
from inertia_flask import inertia_middleware, inertia, defer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from typing import Optional
from pydantic import BaseModel,  ConfigDict, Field
from sqlalchemy import select, inspect


class Base(DeclarativeBase):
    """subclasses will be converted to dataclasses"""
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = "your-secret-key"  # Required for session
app.config["INERTIA_TEMPLATE"] = "base.html"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///demo.db"
db.init_app(app)
inertia_middleware(app)

class PostsSchema(BaseModel):
    config: ConfigDict = ConfigDict(from_attributes=True)
    post_id: int = Field("id")
    title: str = Field("title")
    content: str = Field("content")
    created_at: datetime = Field("created_at")

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
                content="This is a test post stored in our SQLite database!"
            )
            db.session.add(sample_post)
            db.session.commit()


@app.route("/")
@inertia("component")
def hello_world():
    def get_posts():
        posts = Posts.query.all()
        return [{"post_id": post.post_id} for post in posts]
    # post = Posts.query.first()
    return {"value": 1, "defer": defer(get_posts)}


def main():
    init_db()
    app.run(debug=True)


if __name__ == "__main__":
    main()
