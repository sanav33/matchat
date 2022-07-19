from flask import Flask

from api.match import match_bp

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


app.register_blueprint(match_bp)
