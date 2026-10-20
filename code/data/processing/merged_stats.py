#!/opt/anaconda3/bin/python

import re
import pandas as pd
from pathlib import Path
from data.processing import player_stats, schedule, fantasy


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


def add_rolling_features(df, weeks_prior=3, stat_cols=("fantasy_points", "receiving_yards", "targets")):
    df = df.sort_values(["player_name", "season", "week"]).reset_index(drop=True)
    stat_cols = list(stat_cols)
    group_keys = ["player_name", "season"]

    # Shift each player-season's own stats down by 1 row so a row only ever
    # sees data from strictly earlier weeks, then average over that.
    shifted = df.groupby(group_keys)[stat_cols].shift(1)
    shifted_groups = shifted.groupby([df[key] for key in group_keys])

    # Short window: recent form.
    rolling_avg = (
        shifted_groups.rolling(window=weeks_prior, min_periods=1)
        .mean()
        .reset_index(level=group_keys, drop=True)
    )
    rolling_avg.columns = [f"{c}_prev{weeks_prior}avg" for c in stat_cols]

    # Full history to date: established baseline, unbounded by the short window.
    expanding_avg = shifted_groups.expanding().mean().reset_index(level=group_keys, drop=True)
    expanding_avg.columns = [f"{c}_seasonavg" for c in stat_cols]

    return pd.concat([df, rolling_avg, expanding_avg], axis=1)


def compile_sources(year):
    BASE_DIR = Path(__file__).resolve().parents[2]
    raw_dir = BASE_DIR / "data" / "raw"
    players = player_stats.filter_receivers(
        player_stats.extract_data(raw_dir / f"stats_player_week_{year}.csv")
    )
    #players = players[players["week"] <= 18]  # exclude postseason

    games = schedule.get_year(
        schedule.extract_data(raw_dir / "game_schedule.csv"), year
    )
    games_by_team = schedule.by_team(games).drop(columns="opponent_team")


    fantasy_points = fantasy.extract_season(year)
    fantasy_points["_merge_name"] = fantasy_points["player_name"].map(normalize_name)
    fantasy_points = fantasy_points.drop(columns="player_name")

    merged = players.merge(games_by_team, on=["season", "week", "team"], how="left")
    merged["_merge_name"] = merged["player_name"].map(normalize_name)
    merged = merged.merge(fantasy_points, on=["_merge_name", "season", "week"], how="left")
    merged = merged.drop(columns="_merge_name")
    merged["fantasy_points"] = merged["fantasy_points"].fillna(0)

    merged = add_rolling_features(merged)

    return merged

def main():
    merged_2021 = compile_sources(2021)
    print(merged_2021.columns.tolist())

    return merged_2021


if __name__ == "__main__":
    main()
