import setting
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, date
import numpy as np
import seaborn as sns
import mplcursors
import os
# load sample data


def dot_plot(df,x_value,y_value,size):
    """
    Reference:https://seaborn.pydata.org/generated/seaborn.scatterplot.html
    """
    ### Setting Filters ###
    #df = df[df["position"] == 1] 
    df = df[df["mean"] > 2]
    df = df[df["selected"] > setting.total_managers()*0.01]
    # df = df[df["position"] == 4]
    colour_dict = setting.team_colour_dict()
    #######################
    
    #badge_dict = setting.team_badge_dict()
    #x_median = np.median(df[x_value])
    #y_median = np.median(df[y_value])
    #df["size"] = df["season_points"].apply (lambda x: x)
    ax = sns.scatterplot(
        data = df, 
        x = x_value, 
        y = y_value, 
        hue = "team",
        #style = "team",
        size = size,
        sizes = (20, 400),
        #markers = badge_dict,
        alpha = 0.6,
        palette = colour_dict #https://cmdlinetips.com/2019/04/how-to-specify-colors-to-scatter-plots-in-python/
        #style = "position"
        #hue_norm=(0, 1)
        )
    #cursor(hover=True)
    #ax2 = sns.regplot(data = df, x = x_value, #y = y_value)
    #ax.axhline(np.median(df[y_value]))
    #ax.axvline(np.median(df[x_value]))
    plt.legend([],[], frameon=False) ###Remove legend
    crs = mplcursors.cursor(ax, hover = True)
    labels = list(
        df["full_name"]
        + ", PPG=" 
        + df["mean"].astype(str)
        #+ df["consistency"].astype(str)
        )
    #print (labels)
    crs.connect("add", lambda sel: sel.annotation.set_text(labels[sel.index]))
    plt.show()
    if setting.save_fig:
        plt.savefig(f'output/Scattered_Plot_of{y_value}against{x_value}_{datetime.now()}.jpeg')
        print ("Figure saved")

def bar_player_count(df,parameters):
    """
    Example Input:

                               full_name  is_captain  is_vice_captain  is_substitute  count  normal
    34                    Erling Haaland          29               13              0     50       8
    64                   Kieran Trippier           0                0              8     48      40
    60                      João Cancelo           0                0              1     43      42
    38          Gabriel Martinelli Silva           0                1              0     38      37
    43                        Harry Kane          19               11              0     37       7
    ..                               ...         ...              ...            ...    ...     ...

    """
    current_week = parameters["current_week"]
    #print (df)
    df = df.head(20)
    df = df.set_index("full_name")
    df = df.sort_values(by=['count'])
    df = df[["is_substitute","normal","is_vice_captain","is_captain"]]
    #player_name = np.array(df["full_name"])
    ax = df.plot(
        kind="barh",
        stacked = True,
        color = [setting.colour("Medium"),setting.colour("Easy"),setting.colour("Hard"),setting.colour("Very Hard")]
        )
    sum_container = np.array([0] * 20)        
    #for container in ax.containers:
    #    container.datavalues = np.subtract(container.datavalues,sum_container)
    #    sum_container = np.add(sum_container,container.datavalues)
    #    container.datavalues[container.datavalues==0]=['nan']
    #    ax.bar_label(container)    
    '''
    count = np.array(df["count"])
    fig, ax = plt.subplots()
    y = np.array(list(df["count"]))
    y4 = np.array 
    y3 = np.array(list(df["is_captain"]))
    y2 = np.array(list(df["is_vice_captain"]))
    y1 = np.array(list(df["count"]-df["is_vice_captain"]-df["is_captain"]))
    df.plot(x='full_name', kind='barh', stacked=True,title='Stacked Bar Graph by dataframe')
    ax.barh(player_name, y1, tick_label=player_name, label= "Player",color = setting.colour("Easy"))
    ax.barh(player_name, y2, left=y1, tick_label=player_name, label= "Vice captain",color = setting.colour("Hard"))
    ax.barh(player_name, y3, left=y1+y2, tick_label=player_name, label= "Captain",color = setting.colour("Very Hard"))
    ax.tick_params(axis='both', which='both', labelsize=8)
    
    for index, value in enumerate(y1):
        if value:
            plt.text(0, index+0.3, str(value), weight = "bold", color = "white")
    for index, value in enumerate(y2):
        if value:
            plt.text(y1[index], index+0.3, str(value), weight = "bold", color = "white")
    for index, value in enumerate(y3):
        if value:
            plt.text(y2[index] + y1[index], index+0.3, str(value), weight = "bold", color = "white")
    for index, value in enumerate(y):
        if value:
            plt.text(y3[index] + y2[index] + y1[index], index+0.3, str(value), weight = "bold", color = "black")

    ax.legend()
    plt.gca().invert_yaxis() #reverse y-axis, so that the highest count is shown at top
    '''
    ax.set_title(f"Top 20 most frequently picked players in week{current_week}")
    if setting.save_fig:
        today = date.today()
        folder_name = "output/"+"player_count/"+today.strftime("%b-%d-%Y")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        plt.savefig(f'{folder_name}/player_count_week_{current_week}.jpeg',bbox_inches = "tight" ,pad_inches = 1)
        print (f"Week{current_week} Figure saved")
    else:
        plt.show()

#dict_player_count = {'Alisson Ramses Becker': 7, 'Kieran Trippier': 41, 'Ivan Perišić': 8, 'João Cancelo': 37, 'Gabriel Martinelli Silva': 27, 'Luis Díaz': 20, 'Bernardo Veiga de Carvalho e Silva': 5, 'Andreas Hoelgebaum Pereira': 13, 'Ivan Toney': 8, 'Harry Kane': 15, 'Erling Haaland': 50, 'David Raya Martin': 4, 'Leon Bailey': 5, 'Diogo Dalot Teixeira': 5, 'Neco Williams': 15, 'Nick Pope': 14, 'Trent Alexander-Arnold': 10, 'Jadon Sancho': 1, 'Bukayo Saka': 12, 'Kevin De Bruyne': 17, 'Jack Harrison': 2, 'Gabriel Fernando de Jesus': 48, 'Sam Greenwood': 3, 'Fraser Forster': 4, 'Japhet Tanganga': 3, 'Marc Cucurella Saseta': 3, 'Crysencio Summerville': 1, 'Hugo Lloris': 4, 'Tyrell Malacia': 4, 'Luis Sinisterra Lucumí': 1, 'Riyad Mahrez': 1, 'Mateusz Lis': 1, 'Hugo Bueno López': 1, 'Jacob Murphy': 2, 'Lewis Brunt': 1, 'William Saliba': 27, 'Reece James': 16, 'Wesley Fofana': 2, 'Mohamed Salah': 9, 'Aleksandar Mitrović': 15, 'José Malheiro de Sá': 7, 'Pablo Fornals Malla': 1, 'Anthony Gordon': 4, 'Dan Burn': 2, 'Ederson Santana de Moraes': 5, 'Marcus Rashford': 10, 'Danny Ward': 12, 'Eric Dier': 3, 'Billy Gilmour': 1, 'Robert Sánchez': 8, 'Leandro Trossard': 13, 'Martin Ødegaard': 6, 'Miguel Almirón Rejala': 9, 'Emerson Leite de Souza Junior': 3, 'Alexander Isak': 5, 'Harrison Reed': 1, 'Aaron Ramsdale': 2, 'Pascal Groß': 7, 'Pedro Lomba Neto': 4, 'Gabriel dos Santos Magalhães': 7, 'Fabian Schär': 5, 'Phil Foden': 14, 'Vicente Guaita': 2, 'Jack Colback': 1, 'Wilfried Zaha': 6, 'James Ward-Prowse': 2, 'Bernd Leno': 1, 'Son Heung-min': 7, 'Nathan Patterson': 5, 'Kristoffer Klaesson': 1, 'Joachim Andersen': 3, 'Kurt Zouma': 1, 'Pierre-Emile Højbjerg': 4, 'Jordan Pickford': 3, 'Cheick Doucouré': 1, 'Lisandro Martínez': 1, 'Timothy Castagne': 1, 'Asmir Begović': 2, 'Alexis Mac Allister': 4, 'Oleksandr Zinchenko': 2, 'Dean Henderson': 4, 'Virgil van Dijk': 3, 'Dejan Kulusevski': 3, 'Julián Álvarez': 1, 'James Maddison': 2, 'Sven Botman': 2, 'Josh Dasilva': 1, 'Thiago Emiliano da Silva': 1, 'Ilkay Gündogan': 1, 'Jefferson Lerma Solís': 1, 'Conor Coady': 4, 'Jacob Ramsey': 2, 'Mathias Jorgensen': 1, 'Emerson Palmieri dos Santos': 2, 'Daniel Iversen': 1, 'Jannik Vestergaard': 2, 'Sean Longstaff': 2, 'Illan Meslier': 1, 'Kieffer Moore': 1, 'Lukasz Fabianski': 1, 'Mohammed Salisu': 1, 'Joël Veltman': 1, 'Harvey Elliott': 2, 'Karl Darlow': 1, 'Ryan Sessegnon': 1, 'David De Gea Quintana': 2, 'Benjamin White': 2, 'Aaron Cresswell': 1, 'Matt Targett': 1, 'Raheem Sterling': 2, 'Kai Havertz': 1, 'Robin Olsen': 2, 'Max Kilman': 2, 'Emiliano Martínez Romero': 3, 'Bruno Guimarães Rodriguez Moura': 1, 'Lewis Dunk': 4, 'Raphaël Varane': 1, 'Anthony Elanga': 1, 'Kepa Arrizabalaga': 1, 'Andrew Robertson': 1, 'Rúben Gato Alves Dias': 1, 'Philippe Coutinho Correia': 1, 'Kieran Tierney': 1, 'Kalidou Koulibaly': 2, 'Jarrod Bowen': 4, 'Lucas Tolentino Coelho de Lima': 1, 'Cameron Archer': 1, 'Odsonne Edouard': 1, 'Edouard Mendy': 2, 'Rodrigo Hernandez': 1, 'Tyrone Mings': 2, 'Philip Billing': 1, 'Will Dennis': 1, 'Eberechi Eze': 2, 'Alphonse Areola': 1, 'Rodrigo Moreno': 1, 'Lucas Digne': 2, 'Saïd Benrahma': 1, 'Roméo Lavia': 1, 'Tomas Soucek': 1, 'Matija Šarkić': 1, 'Declan Rice': 1, 'João Filipe Iria Santos Moutinho': 1, 'Yves Bissouma': 1, 'Tyrick Mitchell': 1, 'Adrián San Miguel del Castillo': 1, 'Demarai Gray': 1, 'Ben Mee': 1, 'Bryan Mbeumo': 1, 'Marc Guéhi': 1, 'Allan Saint-Maximin': 2, 'Rico Henry': 1, 'Lloyd Kelly': 1, 'Ben Chilwell': 1, 'Paulo Gazzaniga Farias': 1, 'Adam Lallana': 1}
#bar_player_count(dict_player_count)

def line_ml_comparison(test, prediction):
    plt.plot(test, label = "test")
    plt.plot(prediction, label = "prediction")
    plt.legend()
    plt.show()