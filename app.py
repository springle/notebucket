import os

from flask import Flask, request
from waitress import serve

from third_party import is_valid_token, download_blob, upload_blob

ORIGINS = ["https://notebucket.dev"]

app = Flask(__name__)


@app.after_request
def after_request(response):
    if request.headers['Origin'] in ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,reCAPTCHA-Token'
    return response


@app.route("/pull", methods=["GET"])
def pull():
    assert is_valid_token(request.headers.get("reCAPTCHA-Token"))
    return {"note": download_blob(request.args.get("noteid"))}


@app.route("/push", methods=["PUT"])
def push():
    assert is_valid_token(request.headers.get("reCAPTCHA-Token"))
    upload_blob(request.args.get("noteid"), request.data)
    return {}


if __name__ == "__main__":
    server_port = os.environ.get("PORT", "8080")
    serve(app, host="0.0.0.0", port=server_port)
