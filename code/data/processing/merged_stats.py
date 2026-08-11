#!/opt/anaconda3/bin/python

import pandas as pd
from pathlib import Path
import player_stats
import schedule
import fantasy


def compile_sources():
    BASE_DIR = Path(__file__).resolve().parents[2]
    raw_dir = BASE_DIR / "data" / "raw"
    players = player_stats.filter_receivers(
        player_stats.extract_data(raw_dir / "stats_player_wwek_2021.csv")
    )

    games = schedule.get_year(
        schedule.extract_data(raw_dir / "game_schedule.csv"), 2021
    )
    games_by_team = schedule.by_team(games).drop(columns="opponent_team")


    fantasy_points = fantasy.extract_season(2021)

    merged = players.merge(games_by_team, on=["season", "week", "team"], how="left")
    merged = merged.merge(fantasy_points, on=["player_name", "season", "week"], how="left")

    return merged

def main():
    merged_2021 = compile_sources()
    print(merged_2021)
    return merged_2021


    

if __name__ == "__main__":
    main()
