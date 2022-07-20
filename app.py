import profile
from flask import Flask
from api.profile import profile, profile_view
from api.opt_in import opt_in

from api.match import match_bp

app = Flask(__name__)


@app.route("/", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(profile_view)
app.register_blueprint(profile)
app.register_blueprint(match_bp)
app.register_blueprint(opt_in)

app.run(port=5000)
