"""!
@file miscellaneous.py
"""
import pandas as pd
import setting as setting
import sys 
import time

def mapping(df,dict_map):
    """!
    @brief Mapping player id to player full name, team, position and team colour
    @param df: (DataFrame) dataframe with player id
    @param dict_map: (dict) mapping dictionary with id as key mapped to players full name
    @return df: (DataFrame) dataframe with player full name, team, position and team colour
    """
    df["full_name"] = df["id"].apply(lambda x: dict_map[x][0])
    df["team"] = df["id"].apply(lambda x:dict_map[x][1])
    df["position"] = df["id"].apply(lambda x:dict_map[x][2])

    colour_dict = setting.team_colour_dict()
    df["team_colour"] = df["team"].apply(lambda x: colour_dict[x])
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
    df = df.drop(['id','position','multiplier'],axis = 1)
    df = pd.DataFrame({"count":df.groupby(['full_name', 'is_captain', 'is_vice_captain','is_substitute']).size()}).reset_index()
    for col in ["is_captain","is_vice_captain","is_substitute"]:
        df[col] = df[col].astype(int)
        df[col] = df[col] * df["count"]
    df ["normal"] = df["count"] - df["is_captain"] - df["is_vice_captain"] - df ["is_substitute"]
    df = df.groupby(["full_name"]).sum().reset_index()
    df = df.sort_values(by=['count'],ascending=False)
    print ("Counting completed")
    return (df)


def loading_bar(i: int, total_iterations: int, loading_message:str = "", message:str = "") -> None:
    """!
    @brief Print a loading bar in the terminal
    @param i: (int) current iteration
    @param total_iterations: (int) total iterations
    @param loading_message: (str) loading message before the loading bar
    @param message: (str) message to be printed after the loading bar
    """
    percentage = i / total_iterations
    bar_length = 30
    progress = int(bar_length * percentage)
    sys.stdout.write("\r")
    sys.stdout.write(f"{loading_message}")
    sys.stdout.write("[{:<{}}] {:.0%}".format("█" * progress, bar_length, percentage) + f"{message}")
    sys.stdout.flush()
    
