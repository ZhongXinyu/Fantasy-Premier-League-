import requests as re
import json
import setting


def update_basic_info():
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = re.get(url)
    json_dict=r.json()
    with open(f'data_base/basic_info.json', "w") as outfile:
        json.dump(json_dict, outfile)
    print ("Basic Info Updated")

def update_player():
    for id in setting.player_id():
        url = f"https://fantasy.premierleague.com/api/element-summary/{id}/"
        r = re.get(url)
        json_dict=r.json()
        with open(f'data_base/player/{id}.json', "w") as outfile:
            json.dump(json_dict, outfile)
    print ("Player Info Updated")

update_basic_info()