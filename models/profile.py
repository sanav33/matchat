class Profile:

    def __init__(self, slack_id, name, is_intern, team, prefers_interns, prefers_ftes) -> None:
        self.slack_id = slack_id
        self.name = name
        self.is_intern = is_intern
        self.team = team
        self.prefers = {
            "interns": prefers_interns,
            "ftes": prefers_ftes
        }

        self.is_active = True
        self.opted_in = False
        self.met_with = list()

    def getObjDict(self):
        return {
            "slack_id": self.slack_id,
            "name": self.name,
            "is_intern": self.is_intern,
            "team": self.team,
            "prefers": self.prefers.copy(),
            "is_active": self.is_active,
            "opted_in": self.opted_in,
            "met_with": self.met_with,
        }

    def getProfileInfoDict(self):
        return {
            "name": self.name,
            "is_intern": self.is_intern,
            "team": self.team,
            "prefers": self.prefers.copy(),
        }