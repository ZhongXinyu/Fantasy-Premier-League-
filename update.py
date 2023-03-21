import requests as re
import json
import setting
import pandas as pd
import api, miscellaneous
import numpy as np

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
        df = pd.concat([df,df_history[df_history["round"] == week]])
        points_time_series.append(list(df_history["total_points"]))
        selected_time_series.append(list(df_history["selected"]))
    consistency =[ abs(i/j) for i, j in zip(standard_deviation,mean)]
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


    df_concise = df[["full_name","value","season_points","season_bonus","last_3_points","last_5_points","points_time_series","selected_time_series"]]
    df_concise = df_concise.melt(id_vars="full_name", 
            var_name="Indicator Name", 
            value_name="Value")
    with pd.ExcelWriter('output/concise_output.xlsx',mode='w') as writer:  
        df_concise.to_excel(writer, sheet_name='raw_data')
    df_concise.to_json('output/concise_output.json')
    print ("Database Updated")

# update_basic_info()
# update_player()
update_database()