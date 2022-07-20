import profile
from flask import Flask
from api.profile import profile, profile_view

from api.match import match_bp

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def hello_deez():
    return "<p>Hello, Deez!</p>"
