import profile
from flask import Flask, request, Response
from app.api.profile import profile, profile_view
from app.api.match import match_bp
from app.api.home import get_profile_handler

app = Flask(__name__)


@app.get("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.post("/")
def post_handler():
    challenge = request.json["challenge"]
    if challenge:
        return challenge
    
    return router(request)

def router(request) -> Response:
    if request.json["type"] == "app_home_opened":
        return get_profile_handler(request)
    elif request.json["type"] == "block_actions":
        return {
        }[request.json["actions"]]
    elif request.json["type"] == "view_submission":
        return
