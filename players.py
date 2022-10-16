import setting
import api
#import api.call_api_player
import pandas as pd 
import numpy as np

api.call_api_player(1)

df = pd.DataFrame ()
for i in range(1,500):
    week = 7 
    df_history, df_fixtures, df_history_past = api.call_api_player(i)
    df_transfer = df_history[['round','transfers_balance','transfers_in', 'transfers_out']]
    ### here transfer balance can be the y
    #print (df_history)
    #df_history = df_history.iloc[1:7, :]
    #print (df_history.columns)
    #df_fixtures_info = df_fixtures.columns
    df = pd.concat([df,df_transfer.head(1)])

print (pd)
    


