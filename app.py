from flask import Flask, abort, jsonify, request

from inspector import Inspector

app = Flask(__name__)


@app.route("/search", methods=["GET"])
def search():
    abort(501)


if __name__ == "__main__":
    app.run(host="localhost", debug=True, port=8080)
