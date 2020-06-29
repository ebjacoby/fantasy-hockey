

import json
import requests


request_url = "https://statsapi.web.nhl.com/api/v1/teams"
response = requests.get(request_url)


parsed_response = json.loads(response.text)

current_teams = parsed_response["teams"]

# print(current_teams)


id_list = []
for x in current_teams:
    id_list.append(int(x["id"]))

print(id_list)

# Instructions

#Loop through every team, compiling a list of player ids and names (maybe separately)

# Once you have list of ids, loop through list to return specific player stats and compile in csv? 
# at least just to view
