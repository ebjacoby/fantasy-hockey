

import json
import requests


# request_url = "https://statsapi.web.nhl.com/api/v1/teams"
# response = requests.get(request_url)

# parsed_response = json.loads(response.text)

# current_teams = parsed_response["teams"]

# # print(current_teams)

# # make list of team IDs

# team_id_list = []
# for x in current_teams:
#     team_id_list.append(int(x["id"]))

# print(team_id_list)

# #roster info + player IDs

# player_id_list = []
# player_name_list = []
# player_position_list = []

# for x in team_id_list:
#     request_url = f"https://statsapi.web.nhl.com/api/v1/teams/{x}/roster"
#     response_rosters = requests.get(request_url)
        
#     parsed_response_rosters = json.loads(response_rosters.text)

#     current_rosters = parsed_response_rosters["roster"]

#     for y in current_rosters:
#         player_id_list.append(int(y["person"]["id"]))
    
#     for z in current_rosters:
#         player_name_list.append(z["person"]["fullName"])
    
#     for a in current_rosters:
#         player_position_list.append(a["position"]["abbreviation"])

# print(player_id_list)
# print(player_name_list)
# print(player_position_list)

# for b in player_id_list:
#     request_url = f"https://statsapi.web.nhl.com/api/v1/people/{b}?hydrate=stats(splits=statsSingleSeason)"
#     response_players = requests.get(request_url)
        
#     parsed_response_rosters = json.loads(response_players.text)

#     players stats = parsed_response_rosters["roster"]

b=8479393

request_url = f"https://statsapi.web.nhl.com/api/v1/people/{b}?hydrate=stats(splits=statsSingleSeason)"
response_players = requests.get(request_url)
        
parsed_response_rosters = json.loads(response_players.text)

players_stats = parsed_response_rosters["people"][0]["stats"][0]["splits"][0]["stat"]

stat_headers = list(players_stats.keys()) # TODO: assumes first day is on top, but consider sort to ensure latest day is first

print(stat_headers)


# Instructions

#TODO: list of team IDs for the code to loop through when gathering info on specific player IDs ### DONEzxxxxxxx
#TODO: Loop through every team, compiling a list of player ids and names (maybe separately)#### DONExxxxxxxx

#TODO: Once you have list of ids, loop through list to return specific player stats and compile in csv? 
# at least just to view
