"""!
This script will collect the information of players to predict the transfer balance
We will use the following predictors:
- total_points
- accumulative_points
- next_team_difficulty


the y-value is the transfer balance

"""
# append the path of src

import src.api as api
import src.setting as setting
import pandas as pd 
import numpy as np

###### project 2: Finding the most sub out/in players and its determing factors #####

df_fixtures = pd.read_pickle("data_base/player/fixtures.pkl")
df_history = pd.read_pickle("data_base/player/history.pkl")
df_history_past = pd.read_pickle("data_base/player/history_past.pkl")
df_database = pd.read_pickle("data_base/player/database.pkl")
df_team = pd.read_pickle("data_base/team.pkl")

### We would like to investigate player with mean points > 2
player_id = df_database[df_database["mean"]>2]["id"].unique().tolist()

X = pd.DataFrame()
y = pd.DataFrame()

### targer week is the current week
for target_week in range(7, 12):

    start_week = target_week - 6
    end_week = target_week - 1

    df_history["week"] = df_history.index + 1

    df_predictors = df_history[df_history["element"].isin(player_id)][
        [
            'element',
            # 'opponent_team', 
            'total_points', 
            #'was_home', 
            #'minutes',
            'goals_scored', 
            'assists', 
            'clean_sheets', 
            'goals_conceded',
            #'own_goals', 
            #'penalties_saved', 
            #'penalties_missed', 
            #'yellow_cards',
            #'red_cards', 
            #'saves', 
            'bonus', 
            #'bps', 
            'influence', 
            'creativity',
            'threat', 
            'ict_index',
            #'value',
            'week'
        ]
    ]

    # filter out the week
    df_predictors = df_predictors[(df_predictors["week"] >= start_week) & (df_predictors["week"] <= end_week)]
    
    # rename the week to -5, -4, -3, -2, -1
    df_predictors["week"] = df_predictors["week"] - target_week
    
    # # add culumative points
    # df_predictors["culumative_points"] =  df_predictors.groupby('element')['total_points'].sum() - df_predictors.groupby('element')['total_points'].cumsum()
    # make it a pivot table
    df_predictors = df_predictors.pivot_table(index='element', columns = 'week', values=df_predictors.columns).reset_index()
    # rename the columns
    df_predictors.columns = [f'{col[0]}{col[1]}' for col in df_predictors.columns]

    # add the team of the player
    df_predictors = pd.merge(df_predictors, df_team, on = "element", how = "left")

    # add opponent team to the player
    df_opponent = df_history[(df_history["element"].isin(player_id)) & (df_history["week"] == target_week)][
        ["element",
        "opponent_team"]
    ]
    df_predictors = pd.merge(df_predictors, df_opponent, on = "element", how = "left")

    # map the team difficulty
    df_label = df_history[df_history["element"].isin(player_id) & (df_history["week"]==target_week)][
        [
            'element',
            'transfers_balance'
        ]
    ]

    X = pd.concat([X, df_predictors], axis = 0)
    y = pd.concat([y, df_label], axis = 0)

# save the data to pickle
X.to_pickle("data_base/model/predictors.pkl")
y.to_pickle("data_base/model/label.pkl")
