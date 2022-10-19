import this
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
    standard_deviation = []
    mean = []
    for i in setting.player_id():
        week = setting.current_week()
        df_history, df_fixtures, df_history_past = api.call_api_player(i)
        df_history = df_history[['element','round','total_points','selected','transfers_balance','transfers_in', 'transfers_out','value']]
        #print (df_history)
        #df_history = df_history.iloc[1:7, :]
        #print (df_history.columns)
        #df_fixtures_info = df_fixtures.columns
        season_points.append(sum(list(df_history["total_points"])))  ### a list that stores the total points of players)
        standard_deviation.append(np.nanstd(list(df_history["total_points"])))
        mean.append(np.nanmean(list(df_history["total_points"])))
        df = pd.concat([df,df_history[df_history["round"] == week]])
    consistency =[ abs(i/j) for i, j in zip(standard_deviation,mean)]
    print (len(mean),len(standard_deviation),len(season_points))
    df = df.rename(columns = {"element" : "id"})
    df["season_points"] = season_points
    df["mean"] = mean
    df["standard_deviation"] = standard_deviation
    df["consistency"] = consistency
    df = miscellaneous.mapping (df, dict_map)
    df = df.fillna(0)
    print (df.consistency)

    plot.dot_plot(df)

    #df = miscellaneous.mapping(df,dict_map)

    #print (pd)
        


