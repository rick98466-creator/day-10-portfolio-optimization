"""Focused tests for the portfolio price data loader."""

import pandas as pd
import pytest

from portfolio_optimizer.data_loader import load_prices


def test_loads_sample_prices():
    prices = load_prices("data/raw/investment_prices.csv")

    assert len(prices) == 60
    assert list(prices.columns) == [
        "Date", "Asset_A", "Asset_B", "Asset_C"
    ]
    assert pd.api.types.is_datetime64_any_dtype(prices["Date"])
    assert prices["Date"].is_unique
    assert prices["Date"].is_monotonic_increasing


def test_missing_file_raises_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_prices(tmp_path / "missing.csv")


def test_missing_column_is_rejected(tmp_path):
    path = tmp_path / "prices.csv"
    pd.DataFrame({
        "Date": ["2026-01-01"],
        "Asset_A": [100],
    }).to_csv(path, index=False)

    with pytest.raises(ValueError, match="Missing required columns"):
        load_prices(path)


def test_missing_price_is_rejected(tmp_path):
    path = tmp_path / "prices.csv"
    pd.DataFrame({
        "Date": ["2026-01-01"],
        "Asset_A": [100],
        "Asset_B": [None],
        "Asset_C": [100],
    }).to_csv(path, index=False)

    with pytest.raises(ValueError, match="cannot be missing"):
        load_prices(path)


def test_nonpositive_price_is_rejected(tmp_path):
    path = tmp_path / "prices.csv"
    pd.DataFrame({
        "Date": ["2026-01-01"],
        "Asset_A": [100],
        "Asset_B": [0],
        "Asset_C": [100],
    }).to_csv(path, index=False)

    with pytest.raises(ValueError, match="greater than zero"):
        load_prices(path)
