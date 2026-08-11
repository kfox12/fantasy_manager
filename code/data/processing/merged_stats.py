#!/opt/anaconda3/bin/python

import re
import pandas as pd
from pathlib import Path
import player_stats
import schedule
import fantasy


# Players whose name in the fantasy source doesn't match player_stats
# (legal name changes, nicknames) and can't be reconciled by normalize_name alone.
NAME_ALIASES = {
    "Robby Anderson": "Robbie Chosen",
    "Gabriel Davis": "Gabe Davis",
    "Deonte Harris": "Deonte Harty",
}


def normalize_name(name: str) -> str:
    name = str(name)
    name = NAME_ALIASES.get(name, name)
    name = re.sub(r"[.']", "", name)
    name = re.sub(r"\s+(Jr|Sr|II|III|IV)$", "", name, flags=re.IGNORECASE)
    return name.strip()


def compile_sources():
    BASE_DIR = Path(__file__).resolve().parents[2]
    raw_dir = BASE_DIR / "data" / "raw"
    players = player_stats.filter_receivers(
        player_stats.extract_data(raw_dir / "stats_player_week_2021.csv")
    )
    players = players[players["week"] <= 18]  # exclude postseason

    games = schedule.get_year(
        schedule.extract_data(raw_dir / "game_schedule.csv"), 2021
    )
    games_by_team = schedule.by_team(games).drop(columns="opponent_team")


    fantasy_points = fantasy.extract_season(2021)
    fantasy_points["_merge_name"] = fantasy_points["player_name"].map(normalize_name)
    fantasy_points = fantasy_points.drop(columns="player_name")

    merged = players.merge(games_by_team, on=["season", "week", "team"], how="left")
    merged["_merge_name"] = merged["player_name"].map(normalize_name)
    merged = merged.merge(fantasy_points, on=["_merge_name", "season", "week"], how="left")
    merged = merged.drop(columns="_merge_name")

    return merged

def main():
    merged_2021 = compile_sources()
    print(merged_2021[:10])
    return merged_2021


    

if __name__ == "__main__":
    main()
