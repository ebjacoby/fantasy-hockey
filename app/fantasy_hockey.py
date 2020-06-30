

import json
import requests
import csv
import os

import pandas as pd 

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

player_id_list = player_id_list[:10]
player_name_list = player_name_list[:10]
player__list = player_position_list[:10]



b=8473544
request_url = f"https://statsapi.web.nhl.com/api/v1/people/{b}/stats?stats=statsSingleSeason&season=20182019"

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

print(players)


    # rows = zip(player_id_list, player_name_list, player_position_list)

    # with open(csv_file_path, "w", newline='') as csv_file:
    # writer = csv.writer(csv_file)
    # for row in rows:
    #     writer.writerow(row)










# f = open(csv_file_path, 'r')
# reader = csv.DictReader(f)

# dict_list= {}

# for row in reader:
#     dict_list[row[0]] = {'timeOnIce':row[1],'assists':row[2],'goals':row[3],'pim':row[4],'shots':row[5],'games':row[6],'hits':row[7],'powerPlayGoals':row[8],'powerPlayPoints':row[9],'powerPlayTimeOnIce':row[10],'evenTimeOnIce':row[11],'penaltyMinutes':row[12],'faceOffPct':row[13],'shotPct':row[14],'gameWinningGoals':row[15],'overTimeGoals':row[16],'shortHandedGoals':row[17],'shortHandedPoints':row[18],'shortHandedTimeOnIce':row[19],'blocked':row[20],'plusMinus':row[21],'points':row[22],'shifts':row[23],'timeOnIcePerGame':row[24],'evenTimeOnIcePerGame':row[25],'shortHandedTimeOnIcePerGame':row[26],'powerPlayTimeOnIcePerGame':row[27]}

# print(dict_list)







# Traceback (most recent call last):
#   File "app/fantasy_hockey.py", line 78, in <module>
#     players_stats = parsed_response_rosters["people"][0]["stats"][0]["splits"][0]["stat"]
# IndexError: list index out of range










# Instructions

#TODO: list of team IDs for the code to loop through when gathering info on specific player IDs ### DONEzxxxxxxx
#TODO: Loop through every team, compiling a list of player ids and names (maybe separately)#### DONExxxxxxxx

#TODO: Once you have list of ids, loop through list to return specific player stats and compile in csv? 
# at least just to view
