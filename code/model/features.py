import pandas as pd
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from data.processing import merged_stats

# Need to drop the columns that won't be used for training
# Need to transform some of the features with one-hot
# Drop NaN's in week 1
# Split train vs test


YEAR = 2021
TRAINING_TEST_SPLIT = 14
TRAINING_FEATURE_KEEP = [
    "week", "total_line", "is_home", 
    "fantasy_points", "fantasy_points_prev3avg",
    "receiving_yards_prev3avg", "targets_prev3avg",
    "fantasy_points_seasonavg", "receiving_yards_seasonavg",
    "targets_seasonavg"
    ]


def drop_no_history(df) -> pd.DataFrame:
    history_cols = [c for c in TRAINING_FEATURE_KEEP 
                    if c.endswith(("prev3avg", "seasonavg"))]
    
    df = df.dropna(subset= history_cols)
    return df

def drop_training_cols(df) -> pd.DataFrame:
    df = df[TRAINING_FEATURE_KEEP]
    return df

def separate_train_test(df):
    train = df[df["week"] <= TRAINING_TEST_SPLIT]
    test = df[df["week"] > TRAINING_TEST_SPLIT]

    return train, test 

def clean_data_for_training(df: pd.DataFrame):
    df = drop_training_cols(df)
    df = drop_no_history(df)
    train, test = separate_train_test(df)

    return train, test

def prepare_model(train, test):
    Y_train = train["fantasy_points"]
    X_train = train.drop(columns=["fantasy_points", "week"])


    Y_test = test["fantasy_points"]
    X_test = test.drop(columns=["fantasy_points", "week"])

    return X_train, Y_train, X_test, Y_test

def compute_baseline(X_test, Y_test, col):
    return mean_absolute_error(Y_test, X_test[col])


def main():
    df = merged_stats.compile_sources(YEAR)

    train, test = clean_data_for_training(df)

    X_train, Y_train, X_test, Y_test = prepare_model(train, test)
    baseline = min(compute_baseline(X_test, Y_test, "fantasy_points_prev3avg"), 
                   compute_baseline(X_test, Y_test, "fantasy_points_seasonavg"))
    print(f"Baseline is {baseline}")
    model = LinearRegression()
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)

    print(f"Mean Absolute Error (MAE): {mean_absolute_error(Y_test, Y_pred):.4f}")
    print(f"mean-only floor: {mean_absolute_error(Y_test, [Y_train.mean()] * len(Y_test))}")
    print("----------")
    print(f"Mean Squared Error (MSE): {mean_squared_error(Y_test, Y_pred):.4f}")
    print(f"R-squared Score: {r2_score(Y_test, Y_pred):.4f}")



if __name__ == "__main__":
    main()