import profile
from flask import Flask, request, Response
from api.profile import profile, profile_view
from api.opt_in import opt_in

from api.match import match_bp

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
        # return get_profile_handler(request)
        pass
    elif request.json["type"] == "block_actions":
        return 
        # return {
        # }[request.json["actions"]]
    elif request.json["type"] == "view_submission":
        return


app.register_blueprint(profile_view)
app.register_blueprint(profile)
app.register_blueprint(match_bp)
app.register_blueprint(opt_in)

app.run(port=5000)
