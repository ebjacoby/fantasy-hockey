

import json
import requests
import csv
import os


request_url = "https://statsapi.web.nhl.com/api/v1/teams"
response = requests.get(request_url)

parsed_response = json.loads(response.text)

current_teams = parsed_response["teams"]

# print(current_teams)

# make list of team IDs

team_id_list = []
for x in current_teams:
    team_id_list.append(int(x["id"]))

# print(team_id_list)

#roster info + player IDs

player_id_list = []
player_name_list = []
player_position_list = []

for x in team_id_list:
    request_url = f"https://statsapi.web.nhl.com/api/v1/teams/{x}/roster"
    response_rosters = requests.get(request_url)
        
    parsed_response_rosters = json.loads(response_rosters.text)

    current_rosters = parsed_response_rosters["roster"]

    for y in current_rosters:
            if y["position"]["abbreviation"] != "G":
                player_id_list.append(y["person"]["id"])
                player_name_list.append(y["person"]["fullName"])
                player_position_list.append(y["position"]["abbreviation"])
            else:
                continue

# print(player_id_list)
# # print(player_name_list)
# print(player_position_list)



b=8474066
request_url = f"https://statsapi.web.nhl.com/api/v1/people/{b}?hydrate=stats(splits=statsSingleSeason)"
response_players = requests.get(request_url)
            
parsed_response_rosters = json.loads(response_players.text)

splits = parsed_response_rosters["people"][0]["stats"][0]["splits"]


if any(splits):
    players_stats = parsed_response_rosters["people"][0]["stats"][0]["splits"][0]["stat"]
    print(players_stats)

breakpoint()

stat_headers = list(players_stats.keys())






csv_file_name = "current_player_stats.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_file_name)

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=stat_headers)
    writer.writeheader() # uses fieldnames set above

    for b in player_id_list:
        request_url = f"https://statsapi.web.nhl.com/api/v1/people/{b}?hydrate=stats(splits=statsSingleSeason)"
        response_players = requests.get(request_url)
                    
        parsed_response_rosters = json.loads(response_players.text)

        players_stats = parsed_response_rosters["people"][0]["stats"][0]["splits"][0]["stat"]

        writer.writerow(players_stats)

# Traceback (most recent call last):
#   File "app/fantasy_hockey.py", line 78, in <module>
#     players_stats = parsed_response_rosters["people"][0]["stats"][0]["splits"][0]["stat"]
# IndexError: list index out of range










# Instructions

#TODO: list of team IDs for the code to loop through when gathering info on specific player IDs ### DONEzxxxxxxx
#TODO: Loop through every team, compiling a list of player ids and names (maybe separately)#### DONExxxxxxxx

#TODO: Once you have list of ids, loop through list to return specific player stats and compile in csv? 
# at least just to view
