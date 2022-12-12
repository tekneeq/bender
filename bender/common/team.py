
class Team():
    teams = {}

    def __init__(self, name, conf, div, id):
        self.games = []
        self.players = []

        self.name = name
        self.city = self.name.split()[:-1]
        self.mascot = self.name.split()[-1]
        self.id = id

        self.conference = conf
        self.division = div

        Team.teams[self.id] = self

    def get_stats(self):
        return [game.get_stats() for game in self.games]

    def add_player(self, player_obj):
        self.players.append(player_obj)
