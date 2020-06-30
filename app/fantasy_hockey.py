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

player_id_list = player_id_list[:8]
player_name_list = player_name_list[:8]
player__list = player_position_list[:8]

ID = os.environ.get("ID", "OOPS, please set env var called 'ID'")

#get header data for all players - the ID number and season can stay static
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

#note years of season
while True: 
    print("Please input the hockey season for which you would like to make predictions...")
    print("Also, note that this model is designed to predict scores after seasons already played...")
    selected_season = input("(format season: year1year2 e.g. '20182019' or '20192020'): ") #> "9" (string) 
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

def split(x): 
    return [char for char in x]

x = split(selected_season)
yearzero = str(int(x[0] + x[1] + x[2] + x[3]) - 2)
yearone = str(int(x[0] + x[1] + x[2] + x[3]) - 1)
yeartwo = str(int(x[4] + x[5] + x[6] + x[7]) - 1)

last_season = int(yearone + yeartwo)
second_last_season = int(yearzero + yearone)

#write to csv and organize players{} dictionary
csv_file_name = "current_player_stats.csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_file_name)

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=stat_headers)
    writer.writeheader() # uses fieldnames set above

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

            #for csv
            players_stats["playername"] = player_name_list[i]
            players_stats["playerid"] = b
            players_stats["playerposition"] = player_position_list[i]
            writer.writerow(players_stats)
        else:
            player_info = {}
            player_info["playerid"] = b
            player_info["playerposition"] = player_position_list[i]
            player_info["stats"] = no_stats
            writer.writerow(no_stats)

pprint.pprint(players)
breakpoint()

#TODO: calculate game score per season for two seasons? for all players. 
#TODO: Order by game score for who to pick in the next season

def to_twodec(my_num):
    return "{0:,.2f}".format(my_num)

season_score_list = []

for x in player_name_list:
    stats = players[x]["stats"]
    season_score = to_twodec(float((stats["goals"] * 0.75) + (stats["assists"] * 0.625) + (stats["shots"] * 0.075) + (stats["blocked"] * 0.05) + (stats["powerPlayGoals"] * 0.15) + (((stats["powerPlayPoints"]) - (stats["powerPlayGoals"])) * 0.10)))
    season_score_list.append(season_score)


final_list = []
for n, i, s in zip(player_name_list, player_id_list, season_score_list):
    final = { 'player name': n, 'player id': i, 'season_score': s}
    final_list.append(final)

final_list_sorted = sorted(final_list, key=lambda k: k['season_score'])

print(final_list_sorted)


#Player Game Score = (0.75 * G) + (0.7 * A1) + (0.55 * A2) + (0.075 * SOG) + 
# (0.05 * BLK) + (0.15 * PD) – (0.15 * PT) + (0.01 * FOW) – (0.01 * FOL) + 
# (0.05 * CF) – (0.05 * CA) + (0.15 * GF) – (0.15* GA)

# try:
#     symbol = input("Please input a stock identifier: ")
#     symbol_length = len(symbol)
#     if (symbol_length < 3 or symbol_length > 5) or not symbol.isalpha():
#         print("The system is expecting a properly-formed stock symbol like 'MSFT' or 'IBM' - please try again!")
#         exit()