"""Tests for portfolio allocation, returns, and risk."""

import numpy as np
import pandas as pd
import pytest

from portfolio_optimizer.portfolio import (
    calculate_portfolio_returns,
    summarize_portfolio,
    validate_weights,
)


def sample_returns():
    return pd.DataFrame({
        "Asset_A": [0.01, 0.02, -0.01],
        "Asset_B": [0.00, 0.01, 0.02],
        "Asset_C": [-0.02, 0.03, 0.01],
    })


def equal_weights():
    return {"Asset_A": 1/3, "Asset_B": 1/3, "Asset_C": 1/3}


def test_weights_must_sum_to_one():
    with pytest.raises(ValueError, match="sum to 1"):
        validate_weights({"Asset_A": 0.5, "Asset_B": 0.3, "Asset_C": 0.1})


def test_negative_weights_are_rejected():
    with pytest.raises(ValueError, match="negative"):
        validate_weights({"Asset_A": 1.1, "Asset_B": -0.1, "Asset_C": 0.0})


def test_portfolio_returns_are_weighted_asset_returns():
    result = calculate_portfolio_returns(sample_returns(), equal_weights())

    expected_first = (0.01 + 0.00 - 0.02) / 3
    assert result.iloc[0] == pytest.approx(expected_first)
    assert len(result) == 3


def test_summary_calculates_annualized_metrics():
    values = pd.Series([0.01, 0.02, -0.01])
    summary = summarize_portfolio(values)

    assert summary["average_daily_return"] == pytest.approx(np.mean(values))
    assert summary["annualized_expected_return"] == pytest.approx(np.mean(values) * 252)
    assert summary["annualized_volatility"] == pytest.approx(
        np.std(values, ddof=1) * np.sqrt(252)
    )


def test_summary_requires_two_returns():
    with pytest.raises(ValueError, match="At least two"):
        summarize_portfolio(pd.Series([0.01]))
