from threading import Thread
from flask import request, Blueprint, Response
from os import environ
import requests
from constants import PROFILE_MODAL_DICT

SLACK_API_URL = environ.get("SLACK_API_URL")
ATLAS_CONNECTION_STR = environ.get("ATLAS_CONNECTION_STR")

profile = Blueprint('profile', __name__, template_folder='templates')
@profile.post('/profile')
def post_profile_handler():
    json_body = request.json
    
    slack_id = json_body["user"]["id"]

    # if connection to db successful
    status_code = profile.flask.Response(status=200)
    return status_code

# Handler when user updates profile, TODO: this
def update_profile(slack_id, profile_info):
    return

# Get information from profile. TODO: this
@profile.get('/profile')
def get_profile_handler():
    data = request.get_json()
    


profile_view = Blueprint('profile_view', __name__)
@profile_view.post('/profile_view')
def profile_view_handler():
    json_body = request.json
    trigger_id = json_body["trigger_id"]

    thread_send_profile_form = Thread(
        target=send_profile_form,
        kwargs={
            "trigger_id": trigger_id
        }
    )
    thread_send_profile_form.start()
    
    return Response(status=200)

def send_profile_form(trigger_id):
    request_body = {
        "trigger_id": trigger_id,
        "view": PROFILE_MODAL_DICT,
    }

    print(f"Sending profile edit modal to slack for trigger_id {trigger_id}")
    response = requests.post(
        f"{SLACK_API_URL}/api/views.open",
        json=request_body
    )

    if response.status_code == 200:
        print("Successfully sent modal")
        return
    
    print("Unsuccessfully sent modal")
    return
