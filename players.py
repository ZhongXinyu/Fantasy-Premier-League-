import setting
import miscellaneous 
import plot
import api
#import api.call_api_player
import pandas as pd 
import numpy as np

#api.call_api_player(1)

def player():   
    """
    This function collected numerical information in a dataframe, 
    which can be used in plotting a scatter diagram
    E.g. plot cost["value"] vs performance of the current week["total_points"], or performance of the season["season_points"] 
    """
    df = pd.DataFrame ()
    df_full,dict_map = api.call_api_basic()
    season_points = []
    season_bonus = []
    standard_deviation = []
    mean = []
    for i in setting.player_id():
        week = setting.current_week()
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
        #print (df_history)
        #df_history = df_history.iloc[1:7, :]
        #print (df_history.columns)
        #df_fixtures_info = df_fixtures.columns
        season_points.append(sum(list(df_history["total_points"])))  ### a list that stores the total points of players)
        season_bonus.append(sum(list(df_history["bonus"])))
        standard_deviation.append(np.nanstd(list(df_history["total_points"])))
        mean.append(np.nanmean(list(df_history["total_points"])))
        df = pd.concat([df,df_history[df_history["round"] == week]])
    consistency =[ abs(i/j) for i, j in zip(standard_deviation,mean)]
    df = df.rename(columns = {"element" : "id"})
    df["season_points"] = season_points
    df["season_bonus"] = season_bonus
    df["mean"] = mean
    df["standard_deviation"] = standard_deviation
    df["consistency"] = consistency
    df = miscellaneous.mapping (df, dict_map)
    df = df.fillna(0)
    with pd.ExcelWriter('output.xlsx',mode='w') as writer:  
        df.to_excel(writer, sheet_name='raw_data')

    plot.dot_plot(df,"value","mean","selected")

player()
    #df = miscellaneous.mapping(df,dict_map)

    #print (pd)
        


