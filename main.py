import requests
import json
import os
from typing import List, Optional


with open("token.txt") as token_f:
    token = token_f.read().strip()

headers = {'X-TBA-Auth-Key': token }

try:
    r = requests.head("https://www.thebluealliance.com/api/v3/status", headers=headers)
    print("code:")
    print(r.status_code)
    print("connection sucessful")
except requests.ConnectionError:
    print("failed to connect check token")
#print(requests.get(url, headers=headers))

team_key = "frc" + input("Enter a team code: ")
#year = int(input("Enter a year: "))
year = 2023

def get_team_winning_events(team_key: str, year: int):
    url = f'https://www.thebluealliance.com/api/v3/team/{team_key}/matches/{year}/simple'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json()
        winning_match_keys = []
        for match in events:
         winning_alliance = match["winning_alliance"]
         try:
           if team_key in match["alliances"][winning_alliance]["team_keys"]:
            match_dict =  [match["key"],  match["alliances"][winning_alliance]["score"]]
            winning_match_keys.append(match_dict)
         except:
           print("no winner in " + match["key"])
        return winning_match_keys 


    else:
        print(f"Error {response.status_code}: {response.text}")
        return None

winning_events = get_team_winning_events(team_key, year)

sorted_dict = dict(sorted(winning_events, key=lambda x: x[1], reverse=True))
print(sorted_dict)

