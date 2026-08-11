#!/opt/anaconda3/bin/python
import pandas as pd
from pathlib import Path


def extract_data(file_path):
    columns = ["home_team", "away_team", "season", "week", "gameday", "location", "total_line"]

    games_table = pd.read_csv(
        file_path,
        usecols=columns,
        dtype={
            "home_team": "string",
            "away_team": "string",
            "season": "int16",
            "week": "int16",
            "gameday": "string",
            "location": "string",
            "total_line": "float64",
        },
    )

    return games_table

def get_year(table, year: int):
    return table[table["season"] == year]

def by_team(games_table):
    home = games_table.rename(columns={"home_team": "team", "away_team": "opponent_team"})
    home["is_home"] = True
    away = games_table.rename(columns={"away_team": "team", "home_team": "opponent_team"})
    away["is_home"] = False

    return pd.concat([home, away], ignore_index=True)

def main():
    BASE_DIR = Path(__file__).resolve().parents[2]
    csv_path = BASE_DIR / "data" / "raw" / "game_schedule.csv"

    #schedule_path = "stats_player_week_2021.csv"
    games_raw = extract_data(csv_path)
    games_2021 = get_year(games_raw, 2021)

    print(games_2021[:5])



if __name__ == "__main__":
    main()
