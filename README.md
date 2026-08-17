# Fantasy Manager

A data engineering and modeling pipeline for NFL fantasy football analysis, currently focused on predicting weekly wide receiver fantasy performance from historical play, game, and scoring data.

## Overview

Fantasy Manager ingests raw weekly player statistics, game schedules, and fantasy scoring data, reconciles them into a single clean dataset, and engineers features intended for a downstream predictive model. The project is under active development: the data pipeline is functional end-to-end, while the modeling layer is in early scaffolding.

## Project Structure

```
code/
├── data/
│   ├── raw/                    # Source CSVs (player stats, schedules, fantasy scoring)
│   └── processing/
│       ├── player_stats.py     # Extracts and filters weekly player stat lines
│       ├── schedule.py         # Extracts game schedules and reshapes them team-wise
│       ├── fantasy.py          # Pulls weekly PPR fantasy point totals
│       ├── betting_lines.py    # Betting line ingestion (planned)
│       ├── weather.py          # Game weather ingestion (planned)
│       ├── merged_stats.py     # Joins all sources into one dataset and builds rolling features
│       └── Makefile             # Convenience targets for running each pipeline stage
└── model/
    └── features.py          # Model feature engineering (in progress)
```

## Data Pipeline

The pipeline is orchestrated in `merged_stats.py` and combines three sources per player-week:

1. **Player stats** (`player_stats.py`) — weekly receiving stats (targets, receptions, receiving yards), currently filtered to wide receivers.
2. **Game schedule** (`schedule.py`) — expands each game into a per-team row (home/away) for joining against player-team-week.
3. **Fantasy scoring** (`fantasy.py`) — weekly PPR fantasy point totals, fetched per season/week.

Player names are normalized across sources (punctuation, suffixes, and known aliasing edge cases) to maximize match rate on the join. Missing fantasy point values after the join are treated as zero (bye weeks, unrostered performances, etc.), and postseason weeks are excluded.

On top of the merged dataset, `add_rolling_features` computes trailing-performance features per player, using only prior weeks to avoid leakage:

- A short rolling average (default: trailing 3 weeks) capturing recent form
- A full-season expanding average capturing an established baseline

Betting lines and weather data are planned additions to enrich the feature set with game-context signals.

## Getting Started

**Requirements:** Python 3 and [pandas](https://pandas.pydata.org/).

```bash
cd code/data/processing

# Run an individual pipeline stage
./player_stats.py
./schedule.py
./fantasy.py

# Run the full merge pipeline
./merged_stats.py

# Or use the Makefile
make merged
```

`merged_stats.py` builds the combined, feature-enriched dataset in memory for downstream use (e.g., model training).

## Roadmap

- [ ] Incorporate betting lines and weather as model features
- [ ] Extend beyond wide receivers to other skill positions
- [ ] Build out the modeling pipeline (`code/model/`): encoding, train/test split, model training and evaluation
- [ ] Persist the merged dataset rather than regenerating it per run

## Status

This project is a personal, in-progress build. The data pipeline (extraction, cleaning, joining, and feature generation) is functional; the predictive model is not yet implemented.
