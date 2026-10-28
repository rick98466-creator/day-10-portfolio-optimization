"""Tests for additional investment data validation."""

import pandas as pd
import pytest

from portfolio_optimizer.data_loader import load_prices
from portfolio_optimizer.validation import validate_prices


def valid_prices():
    return pd.DataFrame({
        "Date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "Asset_A": [100.0, 101.0],
        "Asset_B": [100.0, 99.0],
        "Asset_C": [100.0, 102.0],
    })


def test_sample_data_passes_validation():
    prices = load_prices("data/raw/investment_prices.csv")
    validate_prices(prices)


def test_duplicate_dates_are_rejected():
    prices = valid_prices()
    prices.loc[1, "Date"] = prices.loc[0, "Date"]

    with pytest.raises(ValueError, match="unique"):
        validate_prices(prices)


def test_unsorted_dates_are_rejected():
    prices = valid_prices().iloc[::-1].reset_index(drop=True)

    with pytest.raises(ValueError, match="ascending"):
        validate_prices(prices)


def test_nan_price_is_rejected():
    prices = valid_prices()
    prices.loc[0, "Asset_A"] = float("nan")

    with pytest.raises(ValueError, match="missing or nonnumeric"):
        validate_prices(prices)


def test_zero_price_is_rejected():
    prices = valid_prices()
    prices.loc[0, "Asset_B"] = 0

    with pytest.raises(ValueError, match="greater than zero"):
        validate_prices(prices)


def test_too_few_observations_are_rejected():
    prices = valid_prices().iloc[:1]

    with pytest.raises(ValueError, match="At least 2 observations"):
        validate_prices(prices)


def test_invalid_minimum_observations_is_rejected():
    with pytest.raises(ValueError, match="at least 2"):
        validate_prices(valid_prices(), minimum_observations=1)
