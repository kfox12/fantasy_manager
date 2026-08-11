#!/opt/anaconda3/bin/python
import pandas as pd

BASE_URL = "https://raw.githubusercontent.com/fantasydatapros/data/master/weekly/{season}/week{week}.csv"


def extract_data(season, week):
    columns = {
        "Player": "player_name",
        "PPRFantasyPoints": "fantasy_points",
    }

    week_table = pd.read_csv(
        BASE_URL.format(season=season, week=week),
        usecols=list(columns.keys()),
        dtype={
            "Player": "string",
            "PPRFantasyPoints": "float64",
        },
    ).rename(columns=columns)

    week_table["season"] = season
    week_table["week"] = week

    return week_table


def extract_season(season, weeks=range(1, 19)):
    return pd.concat(
        (extract_data(season, week) for week in weeks),
        ignore_index=True,
    )


def main():
    fantasy_2021 = extract_season(2021)

    print(f"FANTASY DATABASE SIZE == {len(fantasy_2021)}")
    print(fantasy_2021[:5])


if __name__ == "__main__":
    main()
