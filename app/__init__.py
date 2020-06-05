from flask import Flask

from .extensions import db, migrate
from .index import index
from .models import Account

__all__ = ["Account"]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate.init_app(
        app,
        db,
        # literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    app.register_blueprint(index)
    return app
