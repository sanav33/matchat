class Profile:

    def __init__(
        self,
        slack_id: str, 
        name: str, 
        is_intern: bool, 
        team_id: str, 
        prefers_interns: bool,
        prefers_ftes: bool
        ) -> None:
            self.slack_id = slack_id
            self.name = name
            self.is_intern = is_intern
            self.team_id = team_id
            self.prefers = {
                "interns": prefers_interns,
                "ftes": prefers_ftes
            }

            self.is_active = True
            self.opt_in = False
            self.met_with = list()

    def getObjDict(self):
        return {
            "slack_id": self.slack_id,
            "name": self.name,
            "is_intern": self.is_intern,
            "team_id": self.team_id,
            "prefers": self.prefers.copy(),
            "is_active": self.is_active,
            "opt_in": self.opt_in,
            "met_with": self.met_with,
        }

    def getProfileInfoDict(self):
        return {
            "name": self.name,
            "is_intern": self.is_intern,
            "team_id": self.team_id,
            "prefers": self.prefers.copy(),
        }