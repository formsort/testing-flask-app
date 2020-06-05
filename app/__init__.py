from flask import Flask

from .extensions import db
from .index import index
from .models import Account

__all__ = ["Account"]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    app.register_blueprint(index)
    return app
