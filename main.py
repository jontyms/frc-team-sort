#!/usr/bin/python3

import requests
import json
import os
from typing import List, Optional
import webbrowser
import argparse
import re

parser = argparse.ArgumentParser(
    prog="frc top winning score",
    description="get the top winning score",
    epilog="Text at the bottom of help",
)

parser.add_argument(
    "-o", "--open", help="opens top 5 matches in web browser ", action="store_true"
)
parser.add_argument("--team", type=int, help="team code")

args = parser.parse_args()

with open("token.txt") as token_f:
    token = token_f.read().strip()

headers = {"X-TBA-Auth-Key": token}

try:
    r = requests.head("https://www.thebluealliance.com/api/v3/status", headers=headers)
    print("code:")
    print(r.status_code)
    print("connection sucessful")
except requests.ConnectionError:
    print("failed to connect check token")
# print(requests.get(url, headers=headers))
if not args.team:
    team_key = "frc" + input("Enter a team code: ")
else:
    team_key = "frc" + str(args.team)
# year = int(input("Enter a year: "))
year = 2023


def get_team_winning_events(team_key: str, year: int, match_type: str):
    url = (
        f"https://www.thebluealliance.com/api/v3/team/{team_key}/matches/{year}/simple"
    )
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        events = response.json()
        winning_match_keys = []
        for match in events:
            winning_alliance = match["winning_alliance"]
            if match_type == "q":
                pattren = "\d{4}.*_q.*\d{1,}$"
            if re.match(pattren, match["key"]):
                try:
                    if team_key in match["alliances"][winning_alliance]["team_keys"]:
                        match_dict = [
                            match["key"],
                            match["alliances"][winning_alliance]["score"],
                        ]
                        winning_match_keys.append(match_dict)
                except:
                    print("no winner in " + match["key"])
        return winning_match_keys

    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


match_type = "q"
winning_events = get_team_winning_events(team_key, year, match_type)

sorted_dict = list(sorted(winning_events, key=lambda x: x[1], reverse=True))
print(sorted_dict)
i = 0


while i <= 5:
    score = sorted_dict[i][0]
    print(f"https://www.thebluealliance.com/match/{score}")
    if args.open:
        webbrowser.open(f"https://www.thebluealliance.com/match/{score}")
    i = i + 1
