from curses import termname
import requests as re
import pandas as pd
import setting
import json

"""
Documentation for reference: https://medium.com/@frenzelts/fantasy-premier-league-api-endpoints-a-detailed-guide-acbd5598eb19
"""

def call_api_basic():
    """
    url: "https://fantasy.premierleague.com/api/bootstrap-static/"
    json.keys():['events', 'game_settings', 'phases', 'teams', 'total_players', 'elements', 'element_stats', 'element_types']
    Under element:
        -id : player_id
        -first_name
        -second_name
        -element_type (1:GoalKeeper,2:Defender,3:Midfielder,4:Striker)
    Output:
    df_element: a database of player information
    dcit_map: a mapping dictionary with id as key mapped to players full name 
    """
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = re.get(url)
    json=r.json()
    #print (json.keys())
    #print (json["element_types"])
    df_element = pd.DataFrame(json["elements"])
    df_map = df_element[["id","first_name","second_name","team","element_type"]].copy()
    df_map["full_name"] = df_map.first_name + " " + df_map.second_name
    df_map = df_map[["id","full_name","team","element_type"]]
    dict_map = df_map.set_index('id').T.to_dict('list') #Reference: https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary
    #print (dict_map)
    #dict_map = dict((id,full_name,team)for (id,full_name,team) in zip(df_map["id"],df_map["full_name"],df_map["team"]))
    #print (df_element, dict_map)
    #print (len(df_element_extracted))
    #print (df_map[df_map.full_name == "Bernd Leno"])
    return (df_element,dict_map)

def call_api_player(id):
    """
    Player Detailed Data
    url: https://fantasy.premierleague.com/api/element-summary/{id}/"
    json.keys():['fixtures', 'history', 'history_past']
    Example of player id:
    3 Granit Xhaka
    318 Erling Haaland
    428 Son Heung-min

    Output: df_history
           element  fixture  opponent_team  ...  selected  transfers_in transfers_out
        0      318       10             19  ...   3398599             0             0
        1      318       17              3  ...   5226268       1143813         29876
        2      318       28             15  ...   5676608        368864        141547
        3      318       37              7  ...   5967805        231905        132280
        4      318       49             16  ...   6793855        675165         50249
        5      318       51              2  ...   7781487        802502         20223
        6      318       80             20  ...   8407273        142869          7827
        7      318       88             14  ...   8548463        126753         32563

        df_history.columns
        Index(['element', 'fixture', 'opponent_team', 'total_points', 'was_home',
            'kickoff_time', 'team_h_score', 'team_a_score', 'round', 'minutes',
            'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
            'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards',
            'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity',
            'threat', 'ict_index', 'value', 'transfers_balance', 'selected',
            'transfers_in', 'transfers_out'],
            dtype='object')
    """
    if setting.read_from_local:
        f = open (f'data_base/player/{id}.json', "r")
        j = json.loads(f.read())
    else:
        url = f"https://fantasy.premierleague.com/api/element-summary/{id}/"
        r = re.get(url)
        j = r.json()
    #print (json)
    df_history = pd.DataFrame(j["history"])
    df_fixtures = pd.DataFrame(j["fixtures"])
    df_history_past = pd.DataFrame(j["history_past"])
    #print (df_history, df_fixtures, df_history_past,sep="\n")
    return (df_history, df_fixtures, df_history_past)

def call_api_manager_information(manager_id):
    url =  f'https://fantasy.premierleague.com/api/entry/{manager_id}/'
    r = re.get(url)
    json=r.json()
    print (json.keys())
    df_current = pd.DataFrame(json)
    print (df_current)

def call_api_manager_history(manager_id):
    url =  f'https://fantasy.premierleague.com/api/entry/{manager_id}/history/'
    r = re.get(url)
    json=r.json()
    print (json.keys())
    df_current = pd.DataFrame(json["chips"])
    print (df_current)

def call_api_league_standings(league_id):
    """
    url : "https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings"
    json.keys:['new_entries', 'last_updated_data', 'league', 'standings']
    Output:               id  event_total            player_name  rank  last_rank  rank_sort  total    entry            entry_name
                0    7626992           79             Ross Lewis     1          2          1    623  1434027                Roscoe
                1   51043206           79           Ricky Chahal     2          3          2    622  7071466     Game of Throw-Ins
                2   53988576           69            Kike Markic     3          1          3    621  7415973       Cb Dalton Split
                3    4132606           85              Ray Hurst     4          8          4    616   795537     Hursty s Allstars
                4    5968446           77             Tony Cusse     5          4          5    616  1130525            Anita Dump
    """
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings"
    r = re.get(url)
    json=r.json()
    df_top50 = pd.DataFrame(json["standings"]["results"])
    #print (json.keys())
    league_name = json["league"]
    #print (df_top50)
    #print (league_name)
    df_top50_id = df_top50[["entry"]].copy()
    df_top50_id = df_top50_id.rename(columns={"entry":"manager_id"})
    return (df_top50_id)

def call_api_my_team(manager_id):
    """
    NEED to repair
    Expected: Login and see my team
    """
    url = 'https://users.premierleague.com/accounts/login/'
    payload = {
        'password': 'NFLSzxy0716!',
        'login': 'zhong.xinyu@dhs.sg',
        'redirect_uri': 'https://fantasy.premierleague.com/a/login',
        'app': 'plfpl-web'
    }
    session = re.session()
    session.post(url, data=payload)
    r = session.get(f'https://fantasy.premierleague.com/drf/my-team/{manager_id}')
    #print (r)
    json=r.json()
    #print (json)

def call_api_manager_team(manager_id, event_id):
    """
    Returns the pick of manager{manager_id} at week{event_id}
    json.keys():['active_chip', 'automatic_subs', 'entry_history', 'picks']
    Output:

        element  position  multiplier  is_captain  is_vice_captain
    0       147         1           1       False            False
    1       457         2           1       False            False
    2       146         3           1       False            False
    3       312         4           1       False            False
    4       357         5           1       False            False
    ...

    """
    url =  f'https://fantasy.premierleague.com/api/entry/{manager_id}/event/{event_id}/picks/'
    r = re.get(url)
    json=r.json()
    #print (json.keys())
    #print (json['detail'])
    df_picks = pd.DataFrame(json["picks"])
    #print (df_picks)
    #print(manager_id, event_id)
    return (df_picks)

call_api_basic()
#print (call_api_player(318))
#call_api_league_standings(1)
#call_api_manager_information(7626992)
#call_api_manager_history(7626992)
#call_api_my_team(7134674)
#call_api_manager_team(51043206,1)
#print(pd)