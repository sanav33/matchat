import bson
from flask import Blueprint, jsonify
from os import environ
import pymongo
import random

match_bp = Blueprint('match', __name__)

# TODO: add assignments to met_with field in DB- don't implement until we fix the matching algo
# TODO: check if ppl are on same team
# TODO: send slack notifs
@match_bp.route('/match', methods=['POST'])
def match():
    print(create_graph())
    
    return jsonify(success=True, status_code=200)


def create_graph() -> dict:
    ATLAS_CONNECTION_STR = environ.get("TEST_MONGO_URI")

    client = pymongo.MongoClient(ATLAS_CONNECTION_STR)
    db = pymongo.database.Database(client, 'matchat')
    profiles = db['profiles']
    interns = profiles.find({"opt_in": True, "is_intern": True}, projection=[
        "prefers", "met_with", "name"])
    ftes = profiles.find({"opt_in": True, "is_intern": False}, projection=[
        "prefers", "met_with", "name"])
    
    fte_ids = set([f['_id'] for f in ftes])
    intern_ids = set([i['_id'] for i in interns])

    legal_intern_to_fte_matches = {}
    legal_fte_to_intern_matches = {}

    src = bson.ObjectId()
    sink = bson.ObjectId()

    for i in interns:
        legal_intern_to_fte_matches[i['_id']] = fte_ids.copy()
        
    for f in ftes:
        legal_fte_to_intern_matches[f['_id']] = intern_ids.copy().union(set([sink]))

    legal_intern_to_fte_matches[src] = fte_ids.copy()
    legal_fte_to_intern_matches[sink] = intern_ids.copy()
    
    legal_intern_to_fte_matches.update(legal_fte_to_intern_matches)
    return legal_intern_to_fte_matches


def already_met_recently(employee_1, employee_2) -> bool:
    for met_with in employee_1['met_with']:
        if met_with == employee_2['_id']:
            return True

    for met_with in employee_2['met_with']:
        if met_with == employee_1['_id']:
            return True

    return False


"""
Prints out the names of everyone who was paired up. For development purposes only.
"""
def print_assignments(assignments, ftes, interns):
    ftes.update(interns)
    for x, y in assignments.items():
        print(ftes[x]['name'], '->', ftes[y]['name'])


def match_interns_fte_brute_force(interns: list, ftes: list, assignments: dict, no_matches: list) -> bool:
    random.shuffle(interns)
    random.shuffle(ftes)

    for i, (intern, fte) in enumerate(zip(interns, ftes)):
            if already_met_recently(intern, fte):
                return False

            assignments[intern['_id']] = fte
            assignments[fte['_id']] = intern

    i += 1

    # guaranteed that only one or none of these lists will have leftover people
    while i < len(interns):
        no_matches.append(interns[i])
        i += 1
    while i < len(ftes):
        no_matches.append(ftes[i])
        i += 1

    print("ASSIGNMENTS:")
    print(assignments)
    print("\n\n\nNOT MATCHED:")
    print(no_matches)

    return True