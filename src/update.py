import requests as re
import json
import src.setting as setting
import pandas as pd
import src.api as api, src.miscellaneous as miscellaneous
import numpy as np
import sys
import time
import src.miscellaneous as miscellaneous

"""@package docstring
Documentation for this module.

More details.
"""


def update_basic_info():
    """
    Updates the information for events
    """
    df_full,dict_map = api.call_api_basic()
    df_map = pd.DataFrame.from_dict(dict_map, orient='index', columns = ["full_name","team","position"])
    df_map["element"] = df_map.index
    df_full.to_pickle("data_base/full_info.pkl")
    df_map.to_pickle("data_base/mapping.pkl")
    print ("Basic Info Updated")

def update_player_info():
    """
    Updates the player information, including full name, team, position   
    """
    

def update_player():
    df_history = pd.DataFrame()
    df_fixtures = pd.DataFrame()
    df_history_past = pd.DataFrame()
    for id in setting.player_id():
        url = f"https://fantasy.premierleague.com/api/element-summary/{id}/"
        r = re.get(url)
        json_dict=r.json()
        with open(f'data_base/player/{id}.json', "w") as outfile:
            json.dump(json_dict, outfile)
        if "history" in json_dict.keys():
            df_history = pd.concat([df_history, pd.DataFrame(json_dict["history"])])
        if "fixtures" in json_dict.keys():
            df_fixtures = pd.concat([df_fixtures, pd.DataFrame(json_dict["fixtures"])])     
        if "history_past" in json_dict.keys():
            df_history_past = pd.concat([df_history_past, pd.DataFrame(json_dict["history_past"])])

        miscellaneous.loading_bar(id, len(setting.player_id()), loading_message = "Updating Player Info: ")
        # percentage = id/max(setting.player_id())
        # bar_length = 30
        # progress = int(bar_length * percentage)

        # sys.stdout.write("\r[{:<{}}] {:.0%}".format("=" * progress, bar_length, percentage))
        # sys.stdout.flush()
        # time.sleep(0.1)
  # Adjust the sleep duration for the desired speed
    df_fixtures.to_pickle("data_base/player/fixtures.pkl")
    df_history.to_pickle("data_base/player/history.pkl")
    df_history_past.to_pickle("data_base/player/history_past.pkl")
    print ("Player Info Updated")


def update_database():
    """
        This function collected numerical information in a dataframe, 
        which can be used in plotting a scatter diagram
        E.g. plot cost["value"] vs performance of the current week["total_points"], or performance of the season["season_points"] 
    """
    df = pd.DataFrame ()
    df = pd.DataFrame(columns=[
                    'element',
                    'round',
                    'total_points',
                    'selected',
                    'transfers_balance',
                    'transfers_in',
                    'transfers_out',
                    'value',
                    'bonus'
                ]) 
    df_full,dict_map = api.call_api_basic()
    last_3_points = []
    last_5_points = []
    season_points = []
    season_bonus = []
    standard_deviation = []
    mean = []
    points_time_series = []
    selected_time_series = []
    week = setting.current_week()
    id = setting.player_id()
    for i in id:
        df_history, df_fixtures, df_history_past = api.call_api_player(i)
        if df_history.shape[0] == 0:
            continue
        df_history = df_history[
                [
                    'element',
                    'round',
                    'total_points',
                    'selected',
                    'transfers_balance',
                    'transfers_in',
                    'transfers_out',
                    'value',
                    'bonus'
                ]
            ]
        season_points.append(sum(list(df_history["total_points"])))  ### a list that stores the total points of players)
        last_5_points.append(sum(list(df_history["total_points"])[-5:]))
        last_3_points.append(sum(list(df_history["total_points"])[-3:]))
        season_bonus.append(sum(list(df_history["bonus"])))
        standard_deviation.append(np.nanstd(list(df_history["total_points"])))
        mean.append(np.nanmean(list(df_history["total_points"])))
        df = pd.concat([df,df_history[df_history["round"] == week].head(1)]) #Take the first one in case of double week
    
        ''' element  round  total_points  selected  transfers_balance  transfers_in  transfers_out  value  bonus
            26       61     28             0      2666                 -9             0              9     52      0
            27       61     29             0      2652                -14             0             14     52      0
            28       61     29             0      2652                -14             0             14     52      0
        '''
        points_time_series.append(list(df_history["total_points"]))
        selected_time_series.append(list(df_history["selected"]))
    consistency = [abs(i / j) if j != 0 else None for i, j in zip(standard_deviation, mean)]
    df = df.rename(columns = {"element" : "id"})
    df["last_5_points"] = last_5_points
    df["last_3_points"] = last_3_points
    df["season_points"] = season_points
    df["season_bonus"] = season_bonus
    df["points_time_series"] = points_time_series
    df["selected_time_series"] = selected_time_series
    df["mean"] = mean
    df["standard_deviation"] = standard_deviation
    df["consistency"] = consistency
    df = miscellaneous.mapping(df, dict_map)
    df = df.fillna(0)
    df = setting.filter(df)
    with pd.ExcelWriter('output/output.xlsx',mode='w') as writer:  
        df.to_excel(writer, sheet_name='raw_data')
    df.to_pickle("data_base/player/database.pkl")


    df_concise = df[["full_name","value","season_points","season_bonus","last_3_points","last_5_points","points_time_series","selected_time_series"]]
    df_concise = df_concise.melt(id_vars="full_name", 
            var_name="Indicator Name", 
            value_name="Value")
    with pd.ExcelWriter('output/concise_output.xlsx',mode='w') as writer:  
        df_concise.to_excel(writer, sheet_name='raw_data')
    df_concise.to_json('output/concise_output.json')
    print ("Database Updated")


if __name__ == '__main__':
    update_basic_info()
    update_player_info()
    update_player()
    update_database()