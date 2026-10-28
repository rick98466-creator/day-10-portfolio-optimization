"""Tests for daily investment returns."""

import pandas as pd
import pytest

from portfolio_optimizer.returns import calculate_returns


def test_known_returns_are_calculated_correctly():
    prices = pd.DataFrame({
        "Date": pd.to_datetime(["2026-01-01", "2026-01-02", "2026-01-05"]),
        "Asset_A": [100.0, 102.0, 101.0],
        "Asset_B": [100.0, 100.0, 110.0],
        "Asset_C": [100.0, 90.0, 99.0],
    })

    returns = calculate_returns(prices)

    assert len(returns) == 2
    assert returns.loc[0, "Asset_A"] == pytest.approx(0.02)
    assert returns.loc[0, "Asset_B"] == pytest.approx(0.0)
    assert returns.loc[0, "Asset_C"] == pytest.approx(-0.10)
    assert returns.loc[1, "Asset_B"] == pytest.approx(0.10)
    assert returns.loc[1, "Asset_C"] == pytest.approx(0.10)


def test_returns_exclude_first_price_date():
    prices = pd.DataFrame({
        "Date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "Asset_A": [100.0, 110.0],
        "Asset_B": [100.0, 105.0],
        "Asset_C": [100.0, 95.0],
    })

    returns = calculate_returns(prices)

    assert len(returns) == 1
    assert returns.loc[0, "Date"] == pd.Timestamp("2026-01-02")


def test_invalid_prices_are_rejected():
    prices = pd.DataFrame({
        "Date": pd.to_datetime(["2026-01-01", "2026-01-02"]),
        "Asset_A": [100.0, 0.0],
        "Asset_B": [100.0, 101.0],
        "Asset_C": [100.0, 99.0],
    })

    with pytest.raises(ValueError, match="greater than zero"):
        calculate_returns(prices)
