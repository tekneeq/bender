import collections


class Player():
    def __init__(self, name, team_id):
        self.name = name
        self.team_id = team_id
        self.data = collections.defaultdict(list)

    def add_week(self, week_no, data_dict):
        self.data[week_no].append(data_dict)

