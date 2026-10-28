"""Tests for portfolio allocation comparisons."""

import pandas as pd
import pytest

from portfolio_optimizer.comparison import compare_allocations


def test_comparison_returns_all_three_strategies():
    returns = pd.DataFrame({
        "Asset_A": [0.01, 0.02, -0.01, 0.015],
        "Asset_B": [0.005, 0.006, 0.004, 0.007],
        "Asset_C": [-0.02, 0.03, 0.01, 0.025],
    })

    result = compare_allocations(returns)

    assert len(result) == 3
    assert result["Portfolio"].tolist() == [
        "Equal Weight", "Conservative", "Growth Oriented"
    ]
    assert result["Annualized_Volatility"].ge(0).all()


def test_nonfinite_risk_free_rate_is_rejected():
    returns = pd.DataFrame({
        "Asset_A": [0.01, 0.02],
        "Asset_B": [0.005, 0.006],
        "Asset_C": [-0.02, 0.03],
    })

    with pytest.raises(ValueError, match="finite"):
        compare_allocations(returns, risk_free_rate=float("nan"))


def test_missing_asset_is_rejected():
    returns = pd.DataFrame({
        "Asset_A": [0.01, 0.02],
        "Asset_B": [0.005, 0.006],
    })

    with pytest.raises(ValueError, match="Missing asset return columns"):
        compare_allocations(returns)
