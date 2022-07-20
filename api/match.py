from flask import Blueprint, jsonify
import pymongo

match_bp = Blueprint('match', __name__)

# TODO: add assignments to met_with field in DB- don't implement until we fix the matching algo
# TODO: check if ppl are on same team
# TODO: send slack notifs
@match_bp.route('/match', methods=['POST'])
def match():
    client = pymongo.MongoClient(
        'mongodb+srv://admin:admin@matchatcluster.mixvt.mongodb.net/?retryWrites=true&w=majority')
    db = pymongo.database.Database(client, 'matchat')
    profiles = db['profiles']
    internsCursor = profiles.find({"opt_in": True, "is_intern": True}, projection=[
                                  "prefers", "met_with", "timezone", "name"])
    ftesCursor = profiles.find({"opt_in": True, "is_intern": False}, projection=[
                               "prefers", "met_with", "timezone", "name"])
    interns = {}
    ftes = {}
    assignments = {}
    for intern in internsCursor:
        interns[intern['_id']] = {
            'name': intern['name'],
            'prefers': intern['prefers'],
            'met_with': intern['met_with'],
            'timezone': intern['timezone'],
        }

    for fte in ftesCursor:
        ftes[fte['_id']] = {
            'name': fte['name'],
            'prefers': fte['prefers'],
            'met_with': fte['met_with'],
            'timezone': fte['timezone'],
        }

    print('interns: ', interns)
    print('ftes', ftes)
    # naming: matches_x_y -> x wants y
    # list of intern IDs who prefer FTEs
    matches_intern_ftes = [id for id, v in interns.items() if v['prefers']
                           ['ftes'] and not v['prefers']['interns']]

    matches_fte_ftes = [id for id, v in ftes.items() if v['prefers']
                        ['ftes'] and not v['prefers']['interns']]

    matches_intern_interns = [id for id, v in interns.items() if v['prefers']
                              ['interns'] and not v['prefers']['ftes']]

    no_match = []

    # matches_fte_interns = [id for id, v in ftes if v['prefers']
    #                        ['interns'] and not v['prefers']['ftes']]

    ftes_remaining = []
    interns_remaining = []

    for id, fte in ftes.items():
        # match ftes who are only interested in interns to interns
        if matches_intern_ftes and fte['prefers']['interns'] and not fte['prefers']['ftes']:
            # get intern that only wants fte
            assignee = matches_intern_ftes.pop()
            # assign fte that only wants intern -> intern that only wants fte
            assignments[id] = assignee
            assignments[assignee] = id

        # match ftes who are only interested in other ftes to interns
        elif matches_fte_ftes and fte['prefers']['ftes'] and not fte['prefers']['interns']:
            # find an fte that only wants ftes BUT is not the current fte
            for f in matches_fte_ftes:
                if f == id or f in assignments or already_met_recently(ftes[f], fte):
                    continue
                assignee = f
                break
            matches_fte_ftes.remove(f)
            # assign fte that only wants fte -> fte that only wants fte
            assignments[id] = assignee
            assignments[assignee] = id

        else:
            ftes_remaining.append(id)

    for id, intern in interns.items():
        print(id)
        # match interns who are only interested in other interns to interns
        if matches_intern_interns and intern['prefers']['interns'] and not intern['prefers']['ftes']:
            # find an intern that only wants interns BUT is not the current intern
            for i in matches_intern_interns:
                if i == id or i in assignments or already_met_recently(interns[f], intern):
                    continue
                assignee = i
                break
            matches_intern_interns.remove(i)
            # assign intern that only wants interns -> intern that only wants interns
            assignments[id] = assignee
            assignments[assignee] = id
        else:
            interns_remaining.append(id)

    matches_intern_both = [id for id, v in interns.items() if v['prefers']
                           ['ftes'] and v['prefers']['interns']]
    matches_fte_both = [id for id, v in ftes.items() if v['prefers']
                        ['ftes'] and not v['prefers']['interns']]

    for fte in ftes_remaining:
        if ftes[fte]['prefers']['interns'] and not ftes[fte]['prefers']['ftes']:
            assignee = matches_intern_both.pop()
        elif ftes[fte]['prefers']['ftes'] and not ftes[fte]['prefers']['interns']:
            assignee = matches_fte_both.pop()
        else:
            if matches_intern_both:
                assignee = matches_intern_both.pop()
            elif matches_fte_both:
                assignee = matches_fte_both.pop()
            else:
                no_match.append(fte)
                continue

        assignments[fte] = assignee
        assignments[assignee] = fte

    for intern in interns_remaining:
        if matches_intern_both and interns[intern]['prefers']['interns'] and not interns[intern]['prefers']['ftes']:
            assignee = matches_intern_both.pop()
        elif matches_fte_both and interns[intern]['prefers']['ftes'] and not interns[intern]['prefers']['interns']:
            assignee = matches_fte_both.pop()
        else:
            if matches_intern_both:
                assignee = matches_intern_both.pop()
            elif matches_fte_both:
                assignee = matches_fte_both.pop()
            else:
                no_match.append(intern)
                continue

        assignments[intern] = assignee
        assignments[assignee] = intern

    print_assignments(assignments, ftes, interns)

    return jsonify(success=True, status_code=200)


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
    print(ftes)
    for x, y in assignments.items():
        print(ftes[x]['name'], ftes[y]['name'])
