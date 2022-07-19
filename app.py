import profile
from flask import Flask
from api.profile import profile_view

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(profile_view)
app.register_blueprint(profile)

app.run(port=3000)