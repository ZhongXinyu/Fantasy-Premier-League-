import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import setting

### THIS is a test file designed by ChatGPT ###

# Define the API endpoint
endpoint = "https://fantasy.premierleague.com/api/bootstrap-static/"

# Make a GET request to the API
response = requests.get(endpoint)

# Check that the request was successful
if response.status_code == 200:
    # Load the data into a pandas DataFrame
    data = pd.DataFrame(response.json()["elements"])

    # Filter the data to show only the columns we need and only players with total points greater than or equal to 40
    data = data[['second_name', 'now_cost', 'total_points', 'team']]
    data = data[data.total_points >= 40]
    

    # Use the custom color map to set the marker color
    data['color'] = data['team'].map(lambda x: setting.team_colour_dict()[x])
    data['team_name'] = data['team'].map(lambda x: setting.team_name_map()[x])
    data['team'] = data['team'].astype(str)

    # Create the dropdown box
    teams = data['team_name'].unique()
    # dropdown = go.layout.Updatemenu(buttons=list([dict(label=t, method="update",
    #                                                   args=[{"visible":data['team_name']==t},
    #                                                         {"title": f"Market Value vs Total Points for {t} Players with Total Points >= 40",
    #                                                          "annotations": []}]) for t in teams]),
    #                                  direction="down", showactive=True)

    # Plot the data as a scatter plot
    fig = px.scatter(data, x='now_cost', y='total_points', color='team_name',
                     title="Market Value vs Total Points for Premier League Players with Total Points >= 40",
                     hover_name='second_name', labels={'now_cost': 'Market Value (in millions)',
                                                       'total_points': 'Total Points'},
                     template="plotly_dark",
                     height=700, width=900)
    # fig.update_layout(updatemenus=[dropdown], height=700, width=900)
    # print (dropdown)
    fig.show()
else:
    # Print an error message
    print("Failed to retrieve data from API")
