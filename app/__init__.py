import re
import logging
import datetime

from cachetools.func import ttl_cache
from flask import Flask, current_app, has_app_context
from flask_cors import CORS

from .index import index


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
    le_app = Flask(__name__)
    CORS(le_app, origins=o)
    le_app.register_blueprint(index)
    return le_app
