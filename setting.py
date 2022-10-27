import matplotlib.pyplot as plt
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

def team_colour_dict():
    ###https://teamcolorcodes.com/afc-bournemouth-color-codes/
    colour_dict = {
        1:"#EF0107", #Arsenal
        2:"#95BFE5", #Aston Villa
        3:"#DA291C", #Bournemouth
        4:"#E30613", #Brentford
        5:"#0057B8", #Brighton & Hove Albion
        6:"#034694", #Chelsea
        7:"#1B458F", #Crystal Palace
        8:"#003399", #Everton
        9:"#000000", #Fulham
        10:"#003090", #Leicester City 
        11:"#FFCD00", #Leeds United
        12:"#C8102E", #Liverpool
        13:"#6CABDD", #Manchester City
        14:"#DA291C", #Manchester United
        15:"#241F20", #Newcastle United
        16:"#E53233", #Nottingham Forest
        17:"#D71920", #Southampton
        18:"#132257", #Tottenham Hotspur
        19:"#7A263A", #West Ham United
        20:"#FDB913", #Wolverhampton Wanderers 
    }
    return colour_dict

def team_badge_dict():
    ###https://teamcolorcodes.com/afc-bournemouth-color-codes/
    badge_dict = {
        1: plt.imread('marker/B.png'), #Arsenal
        2:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Aston Villa
        3:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Bournemouth
        4:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Brentford
        5:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Brighton & Hove Albion
        6:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Chelsea
        7:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Crystal Palace
        8:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Everton
        9:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Fulham
        10:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Leicester City 
        11:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Leeds United
        12:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Liverpool
        13:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Manchester City
        14:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Manchester United
        15:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Newcastle United
        16:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Nottingham Forest
        17:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Southampton
        18:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Tottenham Hotspur
        19:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #West Ham United
        20:"https://resources.premierleague.com/premierleague/badges/25/t91.png", #Wolverhampton Wanderers 
    }
    return badge_dict

def league_id():
    league_id_dict = {
        "Premier League": list(range(1,21)),
        "Arsenal": [1],
        "Test": [1],
        "Overall": [314]
    }
    ############################
    league = "Premier League"  #<---- Please Modify this
    ############################
    return league_id_dict[league]

def player_id():
    return list(range(1,639))

###### These are informations that requires changing #######

def test():
    return False 

def save_fig():
    return True

def read_from_local():
    return True

def total_managers():
    return 10766732 ### from api.basic_info
def current_week():
    return 11

def week():
    return (list(range(1,current_week())))