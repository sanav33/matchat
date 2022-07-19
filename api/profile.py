from flask import request, Blueprint, Response

profile = Blueprint('profile', __name__, template_folder='templates')
@profile.post('/profile')
def profile_handler():
    # if connection to db successful
    status_code = profile.flask.Response(status=200)
    return status_code
    
profile_view = Blueprint('profile_view', __name__)
@profile_view.post('/profile_view')
def profile_view_handler():
    json_body = request.json
    trigger_id = json_body["trigger_id"]

    
    return Response(status=200)

@profile_view.after_request
def send_profile_modal():
    return
