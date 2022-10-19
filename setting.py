def colour(colour):
    colour_dict = {
        "Very Hard": "#800720",
        "Hard": "#FF1751",
        "Medium": "#E7E7E7",
        "Easy":"#01FC7A",
        "Very Easy":"#375523",
        "FPL_Green":"#E7E7E7"
        }
    return colour_dict[colour]

def league_id():
    league_id_dict = {
        "Premier League": list(range(1,21)),
        "Arsenal": [1],
        "Test": [1],
        "Overall": [314]
    }
    league = "Overall"
    return league_id_dict[league]

def player_id():
    return list(range(1,639))

###

def test():
    return False 

def save_fig():
    if test:
        return False
    else:
        return True

def week():
    return (list(range(1,10)))

def read_from_local():
    return True

def current_week():
    return 9