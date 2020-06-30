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

def to_twodec(my_num):
    return "{0:,.2f}".format(my_num)


goal_proj = s[third_last_season]["goals"] * .2 + s[second_last_season]["goals"] * .3 + s[last_season]["goals"] * .5
assist_proj = s[third_last_season]["assists"] * .2 + s[second_last_season]["assists"] * .3 + s[last_season]["assists"] * .5
shots_proj = s[third_last_season]["shots"] * .2 + s[second_last_season]["shots"] * .3 + s[last_season]["shots"] * .5
blocked_proj = s[third_last_season]["blocked"] * .2 + s[second_last_season]["blocked"] * .3 + s[last_season]["blocked"] * .5
PPG_proj = s[third_last_season]["powerPlayGoals"] * .2 + s[second_last_season]["powerPlayGoals"] * .3 + s[last_season]["powerPlayGoals"] * .5
PPA_proj = ((s[third_last_season]["powerPlayPoints"]) - (s[third_last_season]["powerPlayGoals"])) * .2 + ((s[second_last_season]["powerPlayPoints"]) - (s[second_last_season]["powerPlayGoals"])) * .3 + ((s[last_season]["powerPlayPoints"]) - (s[last_season]["powerPlayGoals"])) * .5

three_year_season_score = float(goal_proj * 0.75 + assist_proj * 0.625 + shots_proj * 0.075 + blocked_proj * 0.05 + PPG_proj * 0.15 + PPA_proj * 0.1)
print("----------------------")
print("----------------------")
print("According to a three-year weighted average, in  " + player + " will achieve:")
print("----------------------")
print(str(goal_proj) + " goals...")
print(str(assist_proj) + " assists...")
print(str(shots_proj) + " shots on goal...")
print(str(blocked_proj) + " blocked shots...")
print(str(PPG_proj) + " powerplay goals...")
print(str(PPA_proj) + " powerplay assists...")
print("----------------------")
print(player + " also has a current 3-year seasons score of " + str(to_twodec(three_year_season_score)))
print("----------------------")

