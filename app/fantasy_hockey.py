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

player_id_list = player_id_list[:2]
player_name_list = player_name_list[:2]
player__list = player_position_list[:2]

ID = os.environ.get("ID", "OOPS, please set env var called 'ID'")

request_url = f"https://statsapi.web.nhl.com/api/v1/people/{ID}/stats?stats=statsSingleSeason&season=20182019"

response_players = requests.get(request_url)
            
parsed_response_rosters = json.loads(response_players.text)

players_stats = parsed_response_rosters["stats"][0]["splits"][0]["stat"]

stat_headers = list(players_stats.keys())

stat_headers.extend(["playername", "playerid", "playerposition"])

empty_list =[] #populating with zeros for data continuity
for x in stat_headers:
    empty_list.append("0")

no_stats = {} 
for key in stat_headers: 
    for value in empty_list: 
        no_stats[key] = value 
        empty_list.remove(value) 
        break  

#main dictionary to use
players = {}

#write to csv and organize players{} dictionary
csv_file_name = "current_player_stats.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_file_name)

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=stat_headers)
    writer.writeheader() # uses fieldnames set above

    for i,b in enumerate(player_id_list):
        request_url = f"https://statsapi.web.nhl.com/api/v1/people/{b}/stats?stats=statsSingleSeason&season=20182019"
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

            #for csv
            players_stats["playername"] = player_name_list[i]
            players_stats["playerid"] = b
            players_stats["playerposition"] = player_position_list[i]
            writer.writerow(players_stats)
        else:
            writer.writerow(no_stats)

while True: 
    selected_season = input("Please input a season (format: year1year2 e.g. '20182019' or '20172018'): ") #> "9" (string) 
    selected_season_length = len(selected_season)
    if not selected_season.isnumeric():
        print("-----------------------")
        print("Oops! Looks like the formatting wasn't correct.")
        print("-----------------------")
        continue
    elif (selected_season_length != 8):
        print("-----------------------")
        print("Oops! Looks like the formatting wasn't correct.")
        print("-----------------------")
        continue
    else:
        break

#calculate game score per season for two seasons? for all players. 
#Order by game score for who to pick in the next season

print(selected_season)


# try:
#     symbol = input("Please input a stock identifier: ")
#     symbol_length = len(symbol)
#     if (symbol_length < 3 or symbol_length > 5) or not symbol.isalpha():
#         print("The system is expecting a properly-formed stock symbol like 'MSFT' or 'IBM' - please try again!")
#         exit()