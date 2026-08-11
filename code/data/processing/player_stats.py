#!/opt/anaconda3/bin/python
import pandas as pd
from pathlib import Path

def filter_receivers(player_table):
    return player_table[player_table["position_group"] == "WR"]

def filter_player(player_table, player_name):
    return player_table[player_table["player_name"] == player_name]


def player_prev_weeks(player_table, player_name, curr_week, weeks_prior):
    player_filtered = filter_player(player_table, player_name)
    if curr_week - weeks_prior < 2: #User wants all weeks leading up to curr_week
        return player_filtered[player_filtered["week"] < curr_week]
    else: # User wants a limited set of weeks
        return player_filtered[
            (player_filtered["week"] < curr_week) &
            (player_filtered["week"] >= curr_week - weeks_prior)
        ]


def extract_data(file_path):
    columns = {
        "player_display_name": "player_name",
        "position_group": "position_group",
        "team": "team",
        "season": "season",
        "week": "week",
        "opponent_team": "opponent_team",
        "receptions": "receptions",
        "receiving_yards": "receiving_yards",
    }

    player_table = pd.read_csv(
        file_path,
        usecols=list(columns.keys()),
        dtype={
            "player_display_name": "string",
            "position_group": "string",
            "team": "string",
            "season": "int16",
            "week": "int16",
            "opponent_team": "string",
            "receptions": "int16",
            "receiving_yards": "int16",
        },
    ).rename(columns=columns)

    return player_table

def main():
    #features = "weather", "targets_per_game", "home_away", "game_total", \
    #    "opp_pass_def_rank", "average_targets_last_3_games"

    BASE_DIR = Path(__file__).resolve().parents[2]
    csv_path = BASE_DIR / "data" / "raw" / "stats_player_week_2021.csv"

    data_2021 = filter_receivers(extract_data(csv_path))

    #print(f"WR DATABASE SIZE == {len(data_2021)}")
    #print(data_2021[data_2021["player_name"] == "Davante Adams"])
    #print(data_2021[:5])

    #print(player_prev_weeks(data_2021, "Cooper Kupp", 5, 4))

    return data_2021

if __name__ == "__main__":
    main()
