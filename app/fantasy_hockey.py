import json
import requests
import csv
from dotenv import load_dotenv
import os

import pprint

load_dotenv()

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

# player_id_list = player_id_list[:10]
# player_name_list = player_name_list[:10]
# player_list = player_position_list[:10]

ID = os.environ.get("ID", "OOPS, please set env var called 'ID'")

#get header data for all players - the ID number AND SEASON can remain static
request_url = f"https://statsapi.web.nhl.com/api/v1/people/{ID}/stats?stats=statsSingleSeason&season=20182019"

response_players = requests.get(request_url)
            
parsed_response_rosters = json.loads(response_players.text)

players_stats = parsed_response_rosters["stats"][0]["splits"][0]["stat"]

stat_headers = list(players_stats.keys())

# stat_headers.extend(["playername", "playerid", "playerposition"])

empty_list =[] #populating with zeros for data continuity
for x in stat_headers:
    empty_list.append(0)

no_stats = {} 
for key in stat_headers: 
    for value in empty_list: 
        no_stats[key] = value 
        empty_list.remove(value) 
        break  

#main dictionary to use
players = {}

#note years of season
while True: 
    print("------------------------------")
    print("------------------------------")
    print("Please input the hockey season for which you would like to make predictions...")
    selected_season = input("Format season: year1year2 e.g. '20182019' or '20192020': ") #> "9" (string) 
    selected_season_length = len(selected_season)
    if not selected_season.isnumeric():
        print("-----------------------")
        print("Oops! Looks like the formatting wasn't correct.")
        continue
    elif (selected_season_length != 8):
        print("-----------------------")
        print("Oops! Looks like the formatting wasn't correct.")
        continue
    else:
        break

def split(x): 
    return [char for char in x]

x = split(selected_season)
yearzero = str(int(x[0] + x[1] + x[2] + x[3]) - 2)
yearone = str(int(x[0] + x[1] + x[2] + x[3]) - 1)
yeartwo = str(int(x[4] + x[5] + x[6] + x[7]) - 1)

last_season = int(yearone + yeartwo)
second_last_season = int(yearzero + yearone)

#create new dictionary with all players detailed stats
for i,b in enumerate(player_id_list):
    request_url = f"https://statsapi.web.nhl.com/api/v1/people/{b}/stats?stats=statsSingleSeason&season={last_season}"
    response_players = requests.get(request_url)
                
    parsed_response_rosters = json.loads(response_players.text)

    splits = parsed_response_rosters["stats"][0]["splits"]

    if any(splits):
        #for dictionary
        players_stats = parsed_response_rosters["stats"][0]["splits"][0]["stat"]
        player_info = {}
        player_info["playerid"] = b
        player_info["playerposition"] = player_position_list[i]
        player_info["stats"] = players_stats
        players[player_name_list[i]] = player_info
    else:
        player_info = {}
        player_info["playerid"] = b
        player_info["playerposition"] = player_position_list[i]
        player_info["stats"] = no_stats
        players[player_name_list[i]] = player_info


def to_twodec(my_num):
    return "{0:,.2f}".format(my_num)

#draw on the new dictionary to calculate season_score
season_score_list = []

for x in player_name_list:
    stats = players[x]["stats"]
    season_score = float(to_twodec((stats["goals"] * 0.75) + (stats["assists"] * 0.625) + (stats["shots"] * 0.075) + (stats["blocked"] * 0.05) + (stats["powerPlayGoals"] * 0.15) + (((stats["powerPlayPoints"]) - (stats["powerPlayGoals"])) * 0.10)))
    season_score_list.append(season_score)

#create new dictionary to lineup season score with name and position
final_list = []
for n, p, s in zip(player_name_list, player_position_list, season_score_list):
    final = { 'player name': n, 'player position': p, 'season score': s}
    final_list.append(final)

#order the list of player's seasons scores
final_list_sorted = sorted(final_list, key=lambda player: player['season score'], reverse=True)
final_list_sorted_twohundred = final_list_sorted[:200]
new_stat_headers = ["player name", "player position", "season score"]

#write to csv
csv_file_name = "current_player_stats.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_file_name)

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=new_stat_headers)
    writer.writeheader() # uses fieldnames set above

    for x in final_list_sorted_twohundred:
        writer.writerow(x)

print("---------------------")
print("View top 200 players in " + csv_file_name)
print("---------------------")
