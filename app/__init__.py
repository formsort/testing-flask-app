import re
import struct
import zlib
from binascii import unhexlify
import logging
import datetime

from flask import Flask, current_app, Response
from flask_cors import CORS


logger = logging.getLogger("origins")


def o():
    now = datetime.datetime.now()
    if now.second % 10 < 5:
        logger.warn("origins b")
        return [re.compile(r"http://b\.formsort\.local:[0-9]+$")]
    logger.warn("origins a")
    return [re.compile(r"http://a\.formsort\.local:[0-9]+$")]


a = Flask(__name__)
CORS(a, origins=o)


@a.before_first_request
def ok():
    current_app.config["OK"] = True


@a.route("/")
def index():
    return """
<html>
  <head>
    <title>a.formsort.local</title>
  </head>
  <body>
    <p>Loaded from A</p>
    <script>
    fetch('http://b.formsort.local:5000/inner')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.text();
        })
        .catch(error => document.getElementById("outcome").innerHTML = error)
        .then(txt => document.getElementById("outcome").innerHTML = txt);
    </script>
    <p>Loading image from B. Outcome: <b id="outcome"></b></p>
  </body>
</html>"""


def chunk(type, data):
    return (
        struct.pack(">I", len(data)) + type + data + struct.pack(">I", zlib.crc32(type + data))
    )


PNG = (
    b"\x89PNG\r\n\x1A\n"
    + chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
    + chunk(b"IDAT", unhexlify(b"789c6300010000050001"))
    + chunk(b"IEND", b"")
)


@a.route("/i.png")
def img():
    return Response(PNG, mimetype="image/png")


@a.route("/inner")
def inner():
    return Response("<b>success</b>", mimetype="text/html")
