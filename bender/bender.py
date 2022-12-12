import json
import os

import requests
from requests import HTTPError
import espn_api
from common.player import Player

'''

1. Create and datafill Teams/Players from data files
2. Analyze

'''


TEAM_API = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{}"
# TEAM_API = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
SCORE_API = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
NEWS_API = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/news"

TB = TEAM_API.format('tb')
"""
try:

    response = requests.get(SCORE_API)

    parsed = json.loads(response.content)
    # events = parsed['events']
    # for val_dict in events:
    #    print(f"{val_dict['id']} {val_dict['shortName']}")

    print(json.dumps(parsed, indent=4))

    # If the response was successful, no Exception will be raised
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')  # Python 3.6
except Exception as err:
    print(f'Other error occurred: {err}')  # Python 3.6
else:
    print('Success!')
"""
TEAM_ID = {
    'Bears': 'CHI',
    'Bengals': 'CIN',
    'Bills': 'BUF',
    'Broncos': 'DEN',
    'Browns': 'CLE',
    'Buccaneers': 'TB',
    'Cardinals': 'AZ',
    'Chargers': 'LAC',
    'Chiefs': 'KC',
    'Colts': 'IND',
    'Commanders': 'WA',
    'Cowboys': 'DAL',
    'Dolphins': 'MIA',
    'Eagles': 'PHI',
    'Falcons': 'ATL',
    'Giants': 'NYG',
    'Jaguars': 'JAX',
    'Jets': 'NYJ',
    'Lions': 'DET',
    'Packers': 'GB',
    'Panthers': 'CAR',
    'Patriots': 'NE',
    'Raiders': 'LV',
    'Rams': 'LAR',
    'Ravens': 'BAL',
    'Saints': 'NO',
    'Seahawks': 'SEA',
    'Steelers': 'PIT',
    'Texans': 'HOU',
    'Titans': 'TEN',
    'Vikings': 'MIN',
    '49ers': 'SF',

}
EAST = {
    'AFC': ['Miami Dolphins', 'Buffalo Bills', 'New York Jets', 'New England Patriots'],
    'NFC': ['Philadelphia Eagles', 'Dallas Cowboys', 'New York Giants', 'Washington Commanders']
}
NORTH = {
    'AFC': ['Cleveland Browns', 'Baltimore Ravens', 'Cincinnati Bengals', 'Pittsburgh Steelers'],
    'NFC': ['Minnesota Vikings', 'Green Bay Packers', 'Chicago Bears', 'Detroit Lions']
}
SOUTH = {
    'AFC': ['Jacksonville Jaguars', 'Indianapolis Colts', 'Tennessee Titans', 'Houston Texans'],
    'NFC': ['Tampa Bay Buccaneers', 'New Orleans Saints', 'Carolina Panthers', 'Atlanta Falcons']
}
WEST = {
    'AFC': ['Kansas City Chiefs', 'Denver Broncos', 'Los Angeles Chargers', 'Las Vegas Raiders'],
    'NFC': ['Los Angeles Rams', 'San Fransisco 49ers', 'Seattle Seahawks', 'Arizona Cardinals']
}

# upload <file>
# create/delete teams
from os import listdir
from os.path import isfile, join
from common.team import Team
import yaml


def init():
    data_dir = os.path.join(os.getcwd(), 'data')
    game_files = [os.path.join(data_dir, f) for f in listdir(data_dir) if isfile(join(data_dir, f))]

    # Create Teams
    for conf, team_list in EAST.items():
        for team in team_list:
            Team(team, conf, 'East', TEAM_ID[team.split()[-1]])

    for conf, team_list in NORTH.items():
        for team in team_list:
            Team(team, conf, 'East', TEAM_ID[team.split()[-1]])

    for conf, team_list in SOUTH.items():
        for team in team_list:
            Team(team, conf, 'East', TEAM_ID[team.split()[-1]])

    for conf, team_list in WEST.items():
        for team in team_list:
            Team(team, conf, 'East', TEAM_ID[team.split()[-1]])

    def populate(week_no, data_dict):
        for player_name, player_stats in data_dict.items():
            player_obj = Player(player_name, player_stats['Team'])
            player_obj.add_week(week_no, player_stats)
            Team.teams[player_obj.team_id].add_player(player_obj)

    # init games
    for gfile in game_files:
        away_team, home_team, week_no = gfile.split('_')
        with open(gfile, "r") as stream:
            try:
                data_dict = yaml.safe_load(stream)
                pass_dict = data_dict['Passing']
                populate(week_no, pass_dict)
                rush_dict = data_dict['Rushing']
                populate(week_no, rush_dict)
                rec_dict = data_dict['Receiving']
                populate(week_no, rec_dict)



            except yaml.YAMLError as exc:
                print("-----------")
                print(exc)

    print(game_files)
    for t in sorted(Team.teams.values(), key=lambda t: t.id):
        print(t.id)
        print([p.name for p in t.players])


init()
