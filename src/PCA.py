import pandas as pd
from sklearn import preprocessing, decomposition
import sys
import numpy as np
import src.setting as setting
import src.api as api
## Do we do PCA analysis if 

# Load your data as a NumPy array or a Pandas DataFrame
# Ensure your data is properly scaled (mean-centered and standardized)
# Example:

train_y_total = list()
test_y_total = list()
train_x_total = pd.DataFrame()
test_x_total = pd.DataFrame()

for i in setting.player_id():
    week = 7
    df_history, df_fixtures, df_history_past = api.call_api_player(i)
    if df_history.shape[0] == 0:
        continue
    if sum((df_history.total_points.tolist())) <= week *2: 
        # skip the players that has total 0 points
        continue
    df_transfer = df_history[['round','transfers_balance','transfers_in', 'transfers_out']]
    ### here transfer balance can be the y
    #print (df_history)
    #df_history = df_history.iloc[1:7, :]
    #print (df_history.columns)
    #df_fixtures_info = df_fixtures.columns
    df_list = [
        df_fixtures.iloc[1:(week-1), :]["difficulty"].reset_index(drop = True),
        df_history.iloc[(week-4):(week-2), :][[
            #'opponent_team', 
            'total_points', 
            #'was_home', 
            'minutes',
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
            #'influence', 
            #'creativity',
            #'threat', 
            'ict_index'
            #'value'
            ]].reset_index(drop = True)
        ]
    train_y = list(df_history.iloc[1:week-1, :]["total_points"])
    train_y_total.extend(train_y)
    train_x = pd.concat(df_list,axis = 1)
    train_x_total = pd.concat([train_x_total,train_x], axis = 0)
train_x_total = train_x_total.replace(np.nan, 0)
print (train_x_total,train_y_total)
#print (train_x_total, train_y_total)
# predictions, df = ml_model.TreeRegressor(train_x_total, train_y_total)
data = train_x_total
scaler = preprocessing.StandardScaler()
scaled_data = scaler.fit_transform(data)


# Create a PCA model
n_components = 2  # Choose the number of principal components to retain
pca = decomposition.PCA(n_components=n_components)

# Fit the model to the scaled data
pca.fit(scaled_data)

explained_variance = pca.explained_variance_ratio_
print("Explained Variance Ratios:", explained_variance)

reduced_data = pca.transform(scaled_data)

import matplotlib.pyplot as plt

# Scatter plot of the reduced data
plt.scatter(reduced_data[:, 0], reduced_data[:, 1])
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("PCA Result")
plt.show()
