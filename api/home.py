from flask import request, Blueprint, Response, json
from os import environ
import requests
from constants import PROFILE_MODAL_DICT
from models.profile import Profile
from pymongo import MongoClient

SLACK_API_URL = environ.get("SLACK_API_URL")
ATLAS_CONNECTION_STR = environ.get("ATLAS_CONNECTION_STR")

mongo_client = MongoClient(ATLAS_CONNECTION_STR)

home = Blueprint('home', __name__)

# Get information from profile. TODO: this
@profile.post('/home')
def get_profile_handler():
    json_body = request.json
    user_id = Profile(json_body["user"]["id"])

    # extract from profiles_coll
    profile_doc = profiles_coll.find_one(profile.slack_id)

    # extract user information

    # edge case: user does not exist in collection, return empty

