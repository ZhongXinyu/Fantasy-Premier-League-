import pandas as pd
import setting
def mapping(df,dict_map):
    
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
    #for index, full_name in enumerate (df["full_name"]):
    #    if full_name in dict_player_count:
    #        dict_player_count[full_name][0] += 1
    #        #dict_player_count[full_name ]
    #    else:
    #        dict_player_count[full_name][0] = 1
    #        #dict_player_count[full_name][1] = df
    print ("Counting completed")
    return (df)