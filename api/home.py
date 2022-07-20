from flask import request, Blueprint, Response, json
from os import environ
import requests
from models.profile import Profile
from pymongo import MongoClient
import block_kits.home
from utils.constants import ATLAS_CONNECTION_STR
from json import dumps

mongo_client = MongoClient(ATLAS_CONNECTION_STR)

home = Blueprint('home', __name__)

# Send a POST request for profile
@home.post('/home')
def get_profile_handler():
    json_body = request.json
    user_id = json_body["user"]
    print("here")

    # extract from profiles_coll
    profiles_coll = mongo_client.matchat.profiles
    profile_doc = profiles_coll.find_one(user_id)
    print("here")

    if profile_doc is None:
        print("No profile created")
        return Response(
            response=dumps(home.UNCREATED_PROFILE_HOME),
            status_code=200,
            content_type="application/json"
        )
    
    return Response(
        response=dumps(home.created_profile_home(
            Profile(
                name = profile_doc["name"],
                is_intern = profile_doc["is_intern"],
                team_id = profile_doc["team_id"],
                prefers = {
                    "interns": profile_doc["prefers"]["interns"],
                    "ftes": profile_doc["prefers"]["ftes"]
                },
                is_active = profile_doc["is_active"],
                opt_in = profile_doc["opt_in"],
                met_with = profile_doc["met_with"]
            )
        )),
        status_code=200,
        content_type="application/json"
    )

