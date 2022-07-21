from flask import request, Blueprint, Response, json
from os import environ
import requests
from app.models.profile import Profile
from pymongo import MongoClient
from app.block_kits.home import *
from app.utils.constants import ATLAS_CONNECTION_STR
from json import dumps

mongo_client = MongoClient(ATLAS_CONNECTION_STR)

def get_profile_handler(request):
    json_body = request.json
    slack_id = json_body["user"]

    # extract from profiles_coll
    profiles_coll = mongo_client.matchat.profiles
    profile_doc = profiles_coll.find_one({"slack_id": slack_id})

    if profile_doc is None:
        print("No profile created")
        return Response(
            response=dumps(UNCREATED_PROFILE_HOME),
            status=200,
            content_type="application/json"
        )
    
    return Response(
        response=dumps(created_profile_home(
            Profile(
                slack_id=slack_id,
                name = profile_doc["name"],
                is_intern = profile_doc["is_intern"],
                team_id = profile_doc["team_id"],
                prefers_interns = profile_doc["prefers"]["interns"],
                prefers_ftes = profile_doc["prefers"]["ftes"],
                is_active = profile_doc["is_active"],
                opt_in = profile_doc["opt_in"],
                met_with = profile_doc["met_with"]
            )
        )),
        status=200,
        content_type="application/json"
    )

