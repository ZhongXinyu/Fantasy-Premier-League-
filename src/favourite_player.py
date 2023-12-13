
"""!

@mainpage
@section intro_sec Introduction
This is the introduction.

@section install_sec Installation
This is the installation.
@see \link README.md \endlink
@see \link api.py \endlink
@see \link setting.py \endlink

@section example_sec Example
This is the example.

@author X.Zhong
@date 08/11/2023

@file main.py
@brief This is the main file for the project
@details Currently, this python script is used to generate the player selections of top 1000 managers for each week.
"""

import src.api as api, src.plot as plot, src.top_managers as top_managers
import src.setting as setting
import src.miscellaneous as miscellaneous
import pandas as pd 
import numpy as np
import time

df_full,dict_map = api.call_api_basic()

###### Project 1: Finding the most picked player for top 1000 managers ######

for week in range (1,setting.current_week()+1):

    df = top_managers.top_1000_teams({"current_week":week})

    df = miscellaneous.mapping(df,dict_map)

    df = miscellaneous.counting(df)

    plot.bar_player_count(df,{"current_week":week})
    
    time.sleep (30)





