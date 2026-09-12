import numpy as np
import pandas as pd
import pytest

from src.forecasting import (
    FEATURE_COLUMNS,
    build_next_month_features,
)


def test_build_next_month_features():
    dates = pd.date_range(
        "2025-08-01",
        periods=12,
        freq="MS",
    )

    target = pd.Series(
        np.arange(100.0, 112.0),
        index=dates,
        name="overall_index",
    )

    features = build_next_month_features(target)

    assert features.columns.tolist() == FEATURE_COLUMNS
    assert features.index[0] == pd.Timestamp("2026-08-01")

    row = features.iloc[0]

    assert row["lag_1"] == 111.0
    assert row["lag_2"] == 110.0
    assert row["lag_3"] == 109.0
    assert row["lag_12"] == 100.0
    assert row["rolling_mean_12"] == pytest.approx(105.5)
    assert row["month_sin"] == pytest.approx(-0.5)
    assert row["month_cos"] == pytest.approx(
        -np.sqrt(3) / 2
    )


def test_rejects_missing_value():
    dates = pd.date_range("2025-08-01", periods=12, freq="MS")
    target = pd.Series(
        np.arange(100.0, 112.0),
        index=dates,
        name="overall_index",
    )
    target.iloc[-1] = np.nan

    with pytest.raises(ValueError, match="missing values"):
        build_next_month_features(target)


def test_rejects_missing_month():
    dates = pd.date_range("2025-07-01", periods=13, freq="MS")
    target = pd.Series(
        np.arange(100.0, 113.0),
        index=dates,
        name="overall_index",
    )

    target = target.drop(pd.Timestamp("2026-01-01"))

    with pytest.raises(ValueError, match="consecutive monthly"):
        build_next_month_features(target)
