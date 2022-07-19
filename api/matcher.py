import app
import pymongo


@app.route('/match', methods=['POST'])
def match():
    client = pymongo.MongoClient('mongodb://testjkerwdkjrds')
    db = pymongo.database.Database(client, 'db')
    profiles = db['profiles']
    internsCursor = profiles.find({"opt_in": True, "is_intern": True}, projection=[
                                  "prefers", "met_with", "timezone"])
    ftesCursor = profiles.find({"opt_in": True, "is_intern": False}, projection=[
                               "prefers", "met_with", "timezone"])
    interns = {}
    ftes = {}
    assignments = {}
    for intern in internsCursor:
        interns[intern['_id']] = {
            'prefers': intern['prefers'],
            'met_with': intern['met_with'],
            'timezone': intern['timezone'],
        }

    for fte in ftesCursor:
        ftes[fte['_id']] = {
            'prefers': fte['prefers'],
            'met_with': fte['met_with'],
            'timezone': fte['timezone'],
        }

    # naming: matches_x_y -> x wants y
    # list of intern IDs who prefer FTEs
    matches_intern_ftes = [id for id, v in interns if v['prefers']
                           ['ftes'] and not v['prefers']['interns']]

    matches_fte_ftes = [id for id, v in ftes if v['prefers']
                        ['ftes'] and not v['prefers']['interns']]

    matches_intern_interns = [id for id, v in interns if v['prefers']
                              ['interns'] and not v['prefers']['ftes']]

    no_match = []

    # matches_fte_interns = [id for id, v in ftes if v['prefers']
    #                        ['interns'] and not v['prefers']['ftes']]

    ftes_remaining = []
    interns_remaining = []

    for fte in ftes:
        # match ftes who are only interested in interns to interns
        if matches_intern_ftes and fte['prefers']['interns'] and not fte['prefers']['ftes']:
            # get intern that only wants fte
            assignee = matches_intern_ftes.pop()
            # assign fte that only wants intern -> intern that only wants fte
            assignments[fte['_id']] = assignee
            assignments[assignee] = fte['_id']

        # match ftes who are only interested in other ftes to interns
        elif matches_fte_ftes and fte['prefers']['ftes'] and not fte['prefers']['interns']:
            # find an fte that only wants ftes BUT is not the current fte
            for f in matches_fte_ftes:
                if f == fte['_id'] or f in assignment or already_met_recently(ftes[f], fte):
                    continue
                assignee = f
                break
            matches_fte_ftes.remove(f)
            # assign fte that only wants fte -> fte that only wants fte
            assignments[fte['_id']] = assignee
            assignments[assignee] = fte['_id']

        else:
            ftes_remaining.append(fte)

    for intern in interns:
        # match interns who are only interested in other interns to interns
        if matches_intern_interns and interns['prefers']['interns'] and not interns['prefers']['ftes']:
            # find an intern that only wants interns BUT is not the current intern
            for i in matches_intern_interns:
                if i == i['_id'] or i in assignments or already_met_recently(interns[f], intern):
                    continue
                assignee = i
                break
            matches_intern_interns.remove(i)
            # assign intern that only wants interns -> intern that only wants interns
            assignments[intern['_id']] = assignee
            assignments[assignee] = intern['_id']
        else:
            interns_remaining.append(intern)

    matches_intern_both = [id for id, v in interns if v['prefers']
                           ['ftes'] and v['prefers']['interns']]
    matches_fte_both = + [id for id, v in ftes if v['prefers']
                          ['ftes'] and not v['prefers']['interns']]

    for fte in ftes_remaining:
        if fte['prefers']['interns'] and not fte['prefers']['ftes']:
            assignee = matches_intern_both.pop()
        elif fte['prefers']['ftes'] and not fte['prefers']['interns']:
            assignee = matches_fte_both.pop()
        else:
            if matches_intern_both:
                assignee = matches_intern_both.pop()
            elif matches_fte_both:
                assignee = matches_fte_both.pop()
            else:
                no_match.append(fte)
                continue

        assignments[fte['_id']] = assignee
        assignments[assignee] = fte['_id']

    for intern in interns_remaining:
        if intern['prefers']['interns'] and not intern['prefers']['ftes']:
            assignee = matches_intern_both.pop()
        elif intern['prefers']['ftes'] and not intern['prefers']['interns']:
            assignee = matches_fte_both.pop()
        else:
            if matches_intern_both:
                assignee = matches_intern_both.pop()
            elif matches_fte_both:
                assignee = matches_fte_both.pop()
            else:
                no_match.append(intern)
                continue

        assignments[intern['_id']] = assignee
        assignments[assignee] = intern['_id']

# add assignments to met_with field in DB
# send slack notifs
    for assignment in assignments:
        if


def already_met_recently(employee_1, employee_2) -> bool:
    for met_with in employee_1['met_with']:
        if met_with == employee_2['_id']:
            return True

    for met_with in employee_2['met_with']:
        if met_with == employee_1['_id']:
            return True

    return False
