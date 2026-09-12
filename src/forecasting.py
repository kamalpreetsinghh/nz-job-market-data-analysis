from pathlib import Path

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_jobs_online.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "ridge_monthly_index_forecaster.joblib"
)

FEATURE_COLUMNS = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_12",
    "rolling_mean_12",
    "month_sin",
    "month_cos",
]


def build_next_month_features(target):
    next_month = (
        target.index.max()
        + pd.offsets.MonthBegin(1)
    )

    same_month_last_year = (
        next_month - pd.DateOffset(years=1)
    )

    month_number = next_month.month

    features = pd.DataFrame(
        {
            "lag_1": [target.iloc[-1]],
            "lag_2": [target.iloc[-2]],
            "lag_3": [target.iloc[-3]],
            "lag_12": [target.loc[same_month_last_year]],
            "rolling_mean_12": [target.iloc[-12:].mean()],
            "month_sin": [
                np.sin(
                    2 * np.pi * (month_number - 1) / 12
                )
            ],
            "month_cos": [
                np.cos(
                    2 * np.pi * (month_number - 1) / 12
                )
            ],
        },
        index=pd.DatetimeIndex(
            [next_month],
            name="Date",
        ),
    )

    return features[FEATURE_COLUMNS]


def main():
    monthly = pd.read_csv(
        DATA_PATH,
        parse_dates=["Date"],
        index_col="Date",
    )

    target = monthly["overall_index"].asfreq("MS")

    if target.isna().any():
        raise ValueError(
            "The monthly target contains missing periods or values."
        )

    model = joblib.load(MODEL_PATH)

    future_features = build_next_month_features(target)

    prediction = model.predict(future_features)[0]
    forecast_month = future_features.index[0].to_period("M")

    print(f"Forecast month: {forecast_month}")
    print(f"Predicted overall index: {prediction:.2f}")


if __name__ == "__main__":
    main()
