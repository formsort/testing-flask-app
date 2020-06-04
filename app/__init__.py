import re
import logging
import datetime

from cachetools.func import ttl_cache
from flask import Flask, has_app_context

from .extensions import db, cors, migrate
from .index import index
from .models import Account  # noqa


logger = logging.getLogger("origins")


@ttl_cache(maxsize=1, ttl=5)
def o():
    if not has_app_context():
        logger.warn("=== PROBLEM")
    now = datetime.datetime.now()
    if now.second % 10 < 5:
        logger.warn("origins b")
        return [re.compile(r"http://b\.formsort\.local:[0-9]+$")]
    logger.warn("origins a")
    return [re.compile(r"http://a\.formsort\.local:[0-9]+$")]


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    cors.init_app(app, origins=o)
    migrate.init_app(
        app,
        db,
        # literal_binds=True,
        compare_type=True,
        compare_server_default=True,
    )
    app.register_blueprint(index)
    return app
