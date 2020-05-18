import re
import struct
import zlib
from binascii import unhexlify

from flask import Flask, current_app, Response
from flask_cors import CORS


a = Flask(__name__)
CORS(a, origins=[re.compile(r"http://b\.formsort\.local:[0-9]+$")])


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

function loadDoc() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     document.getElementById("outcome").innerHTML = "success";
    }
  };
  xhttp.open("GET", "http://b.formsort.local:5000/i.png", true);
  xhttp.send();
}

        loadDoc();
    </script>
    <p>Loading image from B. Outcome: <b id="outcome">FAIL</b></p>
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
