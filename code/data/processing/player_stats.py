#!/opt/anaconda3/bin/python
import csv
import numpy as np
import pandas as pd
from pathlib import Path
from webencodings import UTF8

def filter_receivers(player_table):
    return player_table[player_table["position_group"] == "WR"]

def filter_player(player_table, player_name):
    return player_table[player_table["player_display_name"] == player_name]


def player_prev_weeks(player_table, player_name, curr_week, weeks_prior):
    player_filtered = filter_player(player_table, player_name)
    if curr_week - weeks_prior < 2: #User wants all weeks leading up to curr_week
        return player_filtered[player_filtered["week"] < curr_week]
    else:
        return player_filtered[
            (player_filtered["week"] < curr_week) & 
            (player_filtered["week"] >= curr_week - weeks_prior - 1)
        ]


def extract_data(file_path): 
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        player_data = []
        for row in reader:
            # print(row)
            player_data.append(
                (
                    row["player_display_name"], 
                    row["position_group"], 
                    row["team"],
                    row["season"],
                    row["week"],
                    row["opponent_team"],
                    row["receptions"], 
                    row["receiving_yards"]
                )
            )

    player_dtype = np.dtype(
        [("player_name", "U20"),  
        ("position_group", "U2"), 
        ("team", "U3"),
        ("season", np.int16),
        ("week", np.int16),
        ("opponent_team", "U3"),
        ("receptions", np.int16),  
        ("receiving_yards", np.int16)]
    )

    player_table = np.array(player_data, dtype = player_dtype)

    return player_table

def main(): 
    #columns = "season", "week", "game_id", "game_date", "player_id", "player_name", "team" \
    #    "opponent", "home/away"
    
    #features = "weather", "targets_per_game", "home_away", "game_total", \
    #    "opp_pass_def_rank", "average_targets_last_3_games"
    #pred_output = "fantasy_points"

    #source = "https://www.pro-football-reference.com/players/"
    #games_db_src = "https://www.footballdb.com/scores/index.html?lg=NFL&yr=2021"

    
    BASE_DIR = Path(__file__).resolve().parents[2]
    csv_path = BASE_DIR / "data" / "raw" / "stats_player_week_2021.csv"
    
    data_2021 = filter_receivers(extract_data(csv_path))

    print(f"WR DATABASE SIZE == {data_2021.size}")
    #print(data_2021[data_2021["player_name"] == "Davante Adams"])
    #print(data_2021[:5])
    print(player_prev_weeks(data_2021, "Davante Adams", 5, 3))

if __name__ == "__main__":
    main()