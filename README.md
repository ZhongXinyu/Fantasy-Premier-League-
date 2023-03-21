#  This is a Football data analysis project 

Data is based on Premier League and Fantasy Premier League game.

## Setting up

1. Install packages in requirement.txt

2. In setting.py, set the week
    ``` python
    def current_week():
        return 26
    ```
3. Run update.py to update till the most recent match day data

## Working functions

### 1.output.py 
Run output.py and open (http://127.0.0.1:8050/) on browser to see interactive data visualisation, where you can compare players based on their performance and also view individual player's performance as time series. (some functions requires further update)

### 2.main.py
Run main.py, the results are generated in output/player_count/{date} folder. These images demonstrate the most commonly picked players *(captain/vice_captain/substitute)* by top 1000 managers. It may take a while to run as it calls API 1000 times for each week's data.(Need to improve performance)

## Other useful output

output/output.xlsx contains the data for all PL players up the week set in setting.py 

ML analysis for performance prediction under deployment (TBD)
Will try Neural network and DT models  
