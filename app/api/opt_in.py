from threading import Thread
from flask import request, Blueprint, Response
from api.profile import update_profile
from os import environ
import requests
from block_kits.profile import PROFILE_MODAL_DICT
from models.profile import Profile
from pymongo import MongoClient

ATLAS_CONNECTION_STR = environ.get("ATLAS_CONNECTION_STR")

mongo_client = MongoClient(ATLAS_CONNECTION_STR)

opt_in = Blueprint('opt_in', __name__)
@opt_in.post('/opt_in')
def opt_in_handler():
    json_body = request.json
    print(json_body)
    values = json_body["view"]["state"]["values"]

    profile = Profile(
        json_body["user"]["id"],
        json_body["user"]["name"],
        values["emp_type"]["static_select-action"]["value"] == "Intern",
        json_body["user"]["team_id"],
        "Interns" in values["preference"]["preference-multi_static_select-action"]["value"],
        "Full-time Employees" in values["preference"]["preference-multi_static_select-action"]["value"],
    )

    profile.opt_in = values["opt_in"]["static_select-action"]["value"]

    thread_update_profile = Thread(
        target=update_profile,
        kwargs={"profile": profile}
    )
    thread_update_profile.start()

    return Response(status=200)
