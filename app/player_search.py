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

#get header data for all players - the ID number and season can stay static
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
    selected_season = input("For which season are you predicting (format = '20182019'): ") #> "9" (string) 
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

#input player    
while True: 
    print("-----------------------")
    player = input("Please input the name of the player for which you would like additional analysis (e.g. Sidney Crosby): ")#str
    player = player.title()
    if str(player) not in player_name_list:
        print("-----------------------")
        print("Oops! Is this player still active?")
        print("-----------------------")
        continue
    else:
        break

def split(x): 
    return [char for char in x]

#identifying years to be used
x = split(selected_season)
finalyear = str(int(x[4] + x[5] + x[6] + x[7]))
secondlastyear = str(int(x[4] + x[5] + x[6] + x[7]) - 1)
thirdlastyear = str(int(x[4] + x[5] + x[6] + x[7]) - 2)
fourthlastyear = str(int(x[4] + x[5] + x[6] + x[7]) - 3)
fifthlastyear = str(int(x[4] + x[5] + x[6] + x[7]) - 4) 


last_season = int(thirdlastyear + secondlastyear)
second_last_season = int(fourthlastyear + thirdlastyear)
third_last_season = int(fifthlastyear + fourthlastyear)
seasons_list = [last_season, second_last_season, third_last_season]


#name and ID dict to vlookup later
name_id_dict = []

for n, i in zip(player_name_list, player_id_list):
    final = { 'player name': n, 'player id': i}
    name_id_dict.append(final)

player_id = [p["player id"] for p in name_id_dict if str(p["player name"]) == player][0]

seasons_dict = {}

for i in seasons_list:
    request_url = f"https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=statsSingleSeason&season={i}"
    response_players = requests.get(request_url)
           
    parsed_response_rosters = json.loads(response_players.text)

    splits = parsed_response_rosters["stats"][0]["splits"]

    if any(splits):
        #for dictionary
        players_stats = parsed_response_rosters["stats"][0]["splits"][0]["stat"]
        seasons_dict[i] = players_stats
    else:
        seasons_dict[i] = no_stats

s = seasons_dict

goal_proj = s[0]["goals"] * .2 + s[1]["goals"] * .3 + s[2]["goals"] * .5
assist_proj = s[0]["assists"] * .2 + s[1]["assists"] * .3 + s[2]["assists"] * .5
shots_proj = s[0]["shots"] * .2 + s[1]["shots"] * .3 + s[2]["shots"] * .5
blocked_proj = s[0]["blocked"] * .2 + s[1]["blocked"] * .3 + s[2]["blocked"] * .5
PPG_proj = s[0]["powerPlayGoals"] * .2 + s[1]["powerPlayGoals"] * .3 + s[2]["powerPlayGoals"] * .5
PPA_proj = ((stats[0]["powerPlayPoints"]) - (stats[0]["powerPlayGoals"])) * .2 + ((stats[1]["powerPlayPoints"]) - (stats[1]["powerPlayGoals"])) * .3 + ((stats[2]["powerPlayPoints"]) - (stats[2]["powerPlayGoals"])) * .5

three_year_season_score = float(goal_proj * 0.75 + assist_proj * 0.625 + shots_proj * 0.075 + stats_proj * 0.05 + PPG_proj * 0.15 + PPA_proj * 0.1









breakpoint()
season_score_list = []

for x in seasons_list:
    stats = seasons_dict[x]
    season_score = float(to_twodec((stats["goals"] * 0.75) + (stats["assists"] * 0.625) + (stats["shots"] * 0.075) + (stats["blocked"] * 0.05) + (stats["powerPlayGoals"] * 0.15) + (((stats["powerPlayPoints"]) - (stats["powerPlayGoals"])) * 0.10)))
    season_score_list.append(season_score)

final_list = []
for n, p, s in zip(player_name_list, player_position_list, season_score_list):
    final = { 'player name': n, 'player position': p, 'season score': s}
    final_list.append(final)

final_list_sorted = sorted(final_list, key=lambda player: player['season score'], reverse=True)

new_stat_headers = ["player name", "player position", "season score"]

csv_file_name = player + ".csv"
csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", csv_file_name)

with open(csv_file_path, "w", newline='') as csv_file: # "w" means "open the file for writing"
    writer = csv.DictWriter(csv_file, fieldnames=new_stat_headers)
    writer.writeheader() # uses fieldnames set above

    for x in final_list_sorted:
        writer.writerow(x)
