#!/opt/anaconda3/bin/python
import csv
import numpy as np
from pathlib import Path


def extract_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            games = []
            for row in reader:
                # print(row)
                total_line = row["total_line"].strip()
                if total_line:
                    total_line_value = float(total_line)
                else:
                    total_line_value = np.nan
                games.append(
                    (
                        row["home_team"],
                        row["away_team"], 
                        row["season"],
                        row["week"],
                        row["gameday"],
                        row["location"], 
                        total_line_value,
                        #row["wind"],
                        #row["temp"]
                    )
                )
    
    games_dtype = np.dtype(
            [("home_team", "U3"),  
            ("away_team", "U3"), 
            ("season", np.int16),
            ("week", np.int16), 
            ("gameday", "U20"),  
            ("location", "U5"),
            ("total_line", np.float64)]
            #("wind", np.int16),
            #("temp", np.int16)]
            
    )
    
    games_table = np.array(games, dtype = games_dtype)
    
    return games_table

def get_year(array, year: int):
    return array[array["season"] == year]
     

def main():
    BASE_DIR = Path(__file__).resolve().parents[2]
    csv_path = BASE_DIR / "data" / "raw" / "game_schedule.csv"

    #schedule_path = "stats_player_week_2021.csv"
    games_raw = extract_data(csv_path)
    games_2021 = get_year(games_raw, 2021)

    print(games_2021[:5])



if __name__ == "__main__":
    main()