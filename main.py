

from Request_Thread import *
from Team import *
import json
import requests
import threading
from Analysis import *

TEAMS_LIST = ['Alabama', 'Georgia', 'Ohio State', 'Texas', 'Clemson', 'Oregon', 'Texas A&M', 'Oklahoma', 'LSU', 'Notre Dame', 'Penn State', 'Florida', 'Florida State',
               'Miami', 'USC', 'Michigan', 'Tennessee', 'Auburn', 'Missouri', 'Ole Miss', 'South Carolina', 'North Carolina', 'Nebraska', 'Kentucky', 'SMU', 'Arkansas',
                 'Wisconsin', 'TCU', 'UCLA', 'Arizona State', 'Colorado', 'UCF', 'Utah', 'Mississippi State', 'Washington', 'Louisville', 'Purdue', 'Texas Tech', 'Iowa',
                   'NC State', 'Michigan State', 'Stanford', 'Pittsburgh', 'Baylor', 'Minnesota', 'Georgia Tech', 'California', 'Syracuse', 'Kansas', 'Vanderbilt',
                     'Maryland', 'Virginia Tech', 'Oklahoma State', 'West Virginia', 'Northwestern', 'Arizona', 'Indiana', 'Boston College', 'Rutgers', 'Cincinnati', 
                     'Virginia', 'Tulane', 'Illinois', 'Kansas State', 'Charlotte', 'Houston', 'UTSA', 'Iowa State', 'South Florida', 'Duke', 'Wake Forest', 'Memphis',
                       'Oregon State', 'East Carolina', 'Washington State', 'San Diego State', 'Boise State', 'BYU', 'North Texas', 'Florida Atlantic', 'Marshall', 
                       'Massachusetts', 'UAB', 'App State', 'UNLV', 'Arkansas State', 'Toledo', 'Liberty', 'Fresno State', 'Southern Miss', 'Georgia State',
                         'Coastal Carolina', 'Tulsa', 'South Alabama', 'Louisiana', 'Western Michigan', 'Colorado State', 'Utah State', 'Texas State', 'Rice', 'UConn', 
                         'Akron', 'Louisiana Tech', 'Temple', 'Georgia Southern', 'Nevada', 'Western Kentucky', 'Hawai\'i', 'Eastern Michigan', 'Miami (OH)', 
                         'Florida International', 'Middle Tennessee', 'Troy', 'Sam Houston', 'Bowling Green', 'San José State', 'Central Michigan', 'New Mexico', 
                         'Ball State', 'James Madison', 'UTEP', 'Wyoming', 'Ohio', 'Northern Illinois', 'Kent State', 'Buffalo', 'Jacksonville State', 'Old Dominion', 
                         'New Mexico State', 'UL Monroe', 'Kennesaw State', 'Army', 'Air Force', 'Navy']
TOP_LEVEL_URL = "http://127.0.0.1:5000/api/"
ENDPOINTS = ["talent", "team_stats", "team_records", "adv_stats", "games"]

def get_data(data, teams):
  for team in teams:
      if 'talent' in data.keys():
          if team.name == data['school']:
            team.talent = float(data['talent'])
      elif 'total' in data.keys():
        if team.name == data['team']:
            team.wins = int(data['total']['wins'])
            team.losses = int(data['total']['losses'])
            team.home_wins = int(data['homeGames']['wins'])
            team.home_losses = int(data['homeGames']['losses'])
            team.road_wins = int(data['awayGames']['wins'])
            team.road_losses = int(data['awayGames']['losses'])
            
      elif 'statName' in data.keys():
        if team.name == data['team']:
          match data['statName']:
          #offensive data
            case 'totalYards':
              team.total_yards = int(data['statValue'])
            case 'netPassingYards':
              team.passing_yards = int(data['statValue'])
            case 'rushingYards':
              team.rushing_yards = int(data['statValue'])
            case 'turnovers':
              team.turnovers = int(data['statValue'])
            case 'possessionTime':
              team.possession_time = int(data['statValue'])
            case 'rushingTDs':
              team.rushing_tds = int(data['statValue'])
            case 'passingTDs':
              team.passing_tds = int(data['statValue'])
          #defensive data
            case 'interceptions':
              team.interceptions = int(data['statValue'])
            case 'fumblesRecovered':
              team.fumbles_recovered = int(data['statValue'])
            case 'tacklesForLoss':
              team.tackles_for_loss = int(data['statValue'])
            # case _:
            #     print("Error: data not found in team_stats.json")
      elif 'defense' in data.keys():
        if team.name == data['team']:
            #more defensive data
            team.overall_ppa = float(data['defense']['ppa'])
            team.passing_ppa = float(data['defense']['passingPlays']['ppa'])
            team.rushing_ppa = float(data['defense']['rushingPlays']['ppa'])
            team.success_rate = float(data['defense']['successRate'])
      elif 'venue' in data.keys():
        if team.name == data['home_team']:
          try:
            if data['home_points'] > data['away_points']:
                team.teams_beaten_home.append(data['away_team'])
            elif data['home_points'] < data['away_points']:
                team.teams_lost_home.append(data['away_team'])
            else:
                print("Game Error 1")
          except TypeError:
            pass
        elif team.name == data['away_team']:
          try:
            if data['home_points'] > data['away_points']:
                team.teams_lost_road.append(data['home_team'])
            elif data['home_points'] < data['away_points']:
                team.teams_beaten_road.append(data['home_team'])
            else:
                print("Game Error 2")
          except TypeError:
            pass
      else:
         print("Data not Found")

def get_data_threaded(teams):
    req_threads = []
    threads = []
    for url in ENDPOINTS:
        req_threads.append(Request_Thread(f"{TOP_LEVEL_URL}{url}"))
    for req in req_threads:
       req.start()
    for req in req_threads:
       req.join()

    for req in req_threads:
       if req.response:
          for item in req.response:
            threads.append(threading.Thread(target=get_data, args=(item, teams)))

    for thread in threads:
      thread.start()

    for thread in threads:
      thread.join()
def create_teams():
    team_data = []

    for new_team in TEAMS_LIST:
        team = Team(new_team)
        team_data.append(team)
    return team_data

def main():
  analysis = Analysis()
  team_objects = create_teams()
  get_data_threaded(team_objects)
  average = analysis.find_average(team_objects)
  analysis.rank_teams(team_objects, average)
        


if __name__ == "__main__":
    main()