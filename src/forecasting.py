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
    if not isinstance(target.index, pd.DatetimeIndex):
        raise TypeError("target must use a DatetimeIndex")

    if target.index.has_duplicates:
        raise ValueError("target contains duplicate months")

    if not target.index.is_monotonic_increasing:
        raise ValueError("target dates must be in chronological order")

    if target.isna().any():
        raise ValueError("target contains missing values")

    expected_dates = pd.date_range(
        start=target.index.min(),
        end=target.index.max(),
        freq="MS",
    )

    if not target.index.equals(expected_dates):
        raise ValueError(
            "target must contain consecutive monthly observations")

    if len(target) < 12:
        raise ValueError(
            "target must contain at least 12 monthly observations")

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


def check_required_files(data_path, model_path):
    missing_files = [
        path for path in (data_path, model_path)
        if not path.exists()
    ]

    if missing_files:
        missing_list = "\n".join(
            f"- {path}" for path in missing_files
        )

        raise FileNotFoundError(
            "Forecast prerequisites are missing:\n"
            f"{missing_list}\n\n"
            "Place the MBIE source files in data/raw/ and run "
            "notebooks/05_monthly_data_inspection.ipynb followed by "
            "notebooks/06_monthly_forecasting.ipynb."
        )


def main():
    try:
        check_required_files(DATA_PATH, MODEL_PATH)
    except FileNotFoundError as error:
        raise SystemExit(str(error)) from None

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
