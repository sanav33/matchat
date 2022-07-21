import profile
from flask import Flask, request, Response
from app.api.profile import profile, profile_view
from app.api.match import match_bp
from app.api.home import home

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/")
def challenge_handler():
    
    return request.json["challenge"]

app.register_blueprint(profile_view)
app.register_blueprint(profile)
app.register_blueprint(match_bp)
app.register_blueprint(home)