import struct
import zlib
from binascii import unhexlify

from flask import Blueprint, Response


index = Blueprint("index", __name__, url_prefix="/")


@index.route("/")
def index_page():
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


@index.route("/i.png")
def img():
    return Response(PNG, mimetype="image/png")


@index.route("/inner")
def inner():
    return Response("<b>success</b>", mimetype="text/html")
