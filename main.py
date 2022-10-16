from symbol import testlist_star_expr
import api, plot, top_managers
import setting
import miscellaneous
import pandas as pd 
import numpy as np
import ml_model


###### Project 1: Finding the most picked player for top 1000 managers ######

'''
df_full,dict_map = api.call_api_basic()

df = top_managers.top_1000_teams()

df = miscellaneous.mapping(df,dict_map)

dict_count = miscellaneous.counting(df)

plot.bar_player_count(dict_count)
'''

###### project 2: Finding the most sub out/in players and its determing factors #####

train_y_total = list()
test_y_total = list()
train_x_total = pd.DataFrame()
test_x_total = pd.DataFrame()

for i in range(1,500):
    week = 7 
    df_history, df_fixtures, df_history_past = api.call_api_player(i)
    df_transfer = df_history[['round','transfers_balance','transfers_in', 'transfers_out']]
    ### here transfer balance can be the y
    #print (df_history)
    #df_history = df_history.iloc[1:7, :]
    #print (df_history.columns)
    #df_fixtures_info = df_fixtures.columns
    df_list = [
        df_fixtures.iloc[1:(week-1), :]["difficulty"].reset_index(drop = True),
        df_history.iloc[0:(week-2), :][['opponent_team', 'total_points', 'was_home', 'minutes',
       'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
       'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards',
       'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity',
       'threat', 'ict_index', 'value']].reset_index(drop = True)
        ]
    df_list_test = [
        df_fixtures.iloc[week-1:week, :]["difficulty"].reset_index(drop = True),
        df_history.iloc[week-2:week-1, :][['opponent_team', 'total_points', 'was_home', 'minutes',
       'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
       'own_goals', 'penalties_saved', 'penalties_missed', 'yellow_cards',
       'red_cards', 'saves', 'bonus', 'bps', 'influence', 'creativity',
       'threat', 'ict_index', 'value']].reset_index(drop = True)
        ]
    train_y = list(df_history.iloc[1:week-1, :]["transfers_balance"])
    train_y_total.extend(train_y)
    test_y = list((df_history.iloc[week-1:week, :]["transfers_balance"]))
    test_y_total.extend(test_y)
    train_x = pd.concat(df_list,axis = 1)
    train_x_total = pd.concat([train_x_total,train_x], axis = 0)
    test_x = pd.concat(df_list_test,axis = 1)
    test_x_total = pd.concat([test_x_total, test_x], axis = 0)
train_x_total = train_x_total.replace(np.nan, 0)
test_x = test_x.replace(np.nan, 0)
#print (test_x_total, test_y_total)
#print (train_x_total, train_y_total)
predictions, df = ml_model.TreeRegressor(train_x_total, train_y_total, test_x_total, test_y_total)

#print (high_trans_volume)
df_high_volume = df[abs(df["predictions"])> 10000]
print  (miscellaneous.mapping(df_high_volume))

