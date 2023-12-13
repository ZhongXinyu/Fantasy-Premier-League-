import src.setting as setting
from src.api import call_api_league_standings,call_api_manager_team,call_api_basic
import pandas as pd 
import numpy as np
import src.miscellaneous as miscellaneous


def top_1000_managers():
    """
    Return top 50 managers from each team league (e.g. Arsenal League, Newcastle United League)
    Output :        id
                0   7626992
                1  51043206
                2  53988576
                3   4132606
                4   5968446
                ...

            a list of top 1000 players id
    """
    df_top1000 = pd.DataFrame(columns = ['manager_id'])
    for league_id in setting.league_id():
        df_top50= call_api_league_standings(league_id)
        df_top1000 = pd.concat([df_top1000, df_top50], ignore_index=True)
    #print (df_top1000.head())
    #np.savetxt(r'top_managers.txt', df_top1000, fmt='%d')
    print ("Top 1000 team manager accquired")
    return (df_top1000["manager_id"])

def top_1000_teams(parameters):
    list_top_1000 = top_1000_managers()
    #list_top_1000 = list_top_1000[0:10] ### Reduce the no of API calls, used for testing.
    df = pd.DataFrame()
    current_week = parameters["current_week"]
    i = 0 
    for manager_id in list_top_1000:
        for event_id in [current_week]: ### Range of weeks
            df_temp = call_api_manager_team(manager_id, event_id)
            df = pd.concat([df, df_temp], ignore_index=True)
            i += 1
            miscellaneous.loading_bar(i,len(list_top_1000), f"Loading Week {event_id}")
    df = df.rename(columns={"element":"id"})
    # df.to_csv(f"Top_players_in_week{current_week}.csv", index=False)
    print ("Top 1000 teams accquired")
    return (df)

def mapping(df,dict_map):
    df["full_name"] = df["id"].apply(lambda x: dict_map[x])
    print ("Mapping Completed")
    return (df)

def counting(df):
    """
    Example input: 
             id  position  multiplier  is_captain  is_vice_captain                  full_name
        0   376         1           1       False            False                  Nick Pope
        1   377         2           1       False            False                Sven Botman
        2    26         3           1       False            False             William Saliba
        3   357         4           1       False            False            Kieran Trippier
        4   301         5           1       False            False            Kevin De Bruyne
        5    13         6           1       False            False                Bukayo Saka
        6   261         7           1       False            False             James Maddison
        7   111         8           1       False            False           Leandro Trossard
        8    28         9           1       False             True  Gabriel Fernando de Jesus
        9   318        10           2        True            False             Erling Haaland
        10  210        11           1       False            False        Aleksandar Mitrović
    
    Example Output:
                             full_name  is_captain  is_vice_captain  count
        0          Aleksandar Mitrović       False            False      4
        1          Alexis Mac Allister       False            False      1
        2        Alisson Ramses Becker       False            False      1
        3   Andreas Hoelgebaum Pereira       False            False      4
        ...
    """
    #print (df)
    df = df.drop(['id','position','multiplier'],axis = 1)
    df = pd.DataFrame({"count":df.groupby(['full_name', 'is_captain', 'is_vice_captain']).size()}).reset_index()
    #df.rename(columns={0:"count"})
    for col in ["is_captain","is_vice_captain"]:
        df[col] = df[col].astype(int)
        df[col] = df[col] * df["count"]
    df = df.groupby(["full_name"]).sum().reset_index()
    df = df.sort_values(by=['count'],ascending=False)
    print (df)
    print (df[df['full_name'] == "Harry Kane"])

    #for index, full_name in enumerate (df["full_name"]):
    #    if full_name in dict_player_count:
    #        dict_player_count[full_name][0] += 1
    #        #dict_player_count[full_name ]
    #    else:
    #        dict_player_count[full_name][0] = 1
    #        #dict_player_count[full_name][1] = df
    print ("Counting completed")
    return (df)


