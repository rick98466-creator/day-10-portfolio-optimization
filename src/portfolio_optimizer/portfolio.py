"""Portfolio return and risk calculations."""

import numpy as np
import pandas as pd

from portfolio_optimizer.data_loader import ASSET_COLUMNS


TRADING_DAYS_PER_YEAR = 252


def validate_weights(weights: dict[str, float]) -> pd.Series:
    """Validate asset weights and return them in standard asset order."""
    if set(weights) != set(ASSET_COLUMNS):
        raise ValueError(f"Weights must contain exactly: {ASSET_COLUMNS}")

    series = pd.Series(weights, dtype=float)

    if not np.isfinite(series.to_numpy()).all():
        raise ValueError("Weights must be finite numbers.")

    if (series < 0).any():
        raise ValueError("Weights cannot be negative.")

    if not np.isclose(series.sum(), 1.0, atol=1e-8):
        raise ValueError("Weights must sum to 1.0.")

    return series[ASSET_COLUMNS]


def calculate_portfolio_returns(
    asset_returns: pd.DataFrame,
    weights: dict[str, float],
) -> pd.Series:
    """Calculate daily portfolio returns using fixed allocation weights."""
    required = ASSET_COLUMNS
    missing = [column for column in required if column not in asset_returns.columns]
    if missing:
        raise ValueError(f"Missing asset return columns: {missing}")

    if asset_returns.empty:
        raise ValueError("Asset returns cannot be empty.")

    weight_series = validate_weights(weights)
    values = asset_returns[required].to_numpy(dtype=float)

    if not np.isfinite(values).all():
        raise ValueError("Asset returns must be finite numbers.")

    return pd.Series(
        values @ weight_series.to_numpy(),
        index=asset_returns.index,
        name="Portfolio_Return",
    )


def summarize_portfolio(
    portfolio_returns: pd.Series,
) -> dict[str, float]:
    """Summarize average return and annualized volatility."""
    values = portfolio_returns.to_numpy(dtype=float)

    if len(values) < 2:
        raise ValueError("At least two daily returns are required.")

    if not np.isfinite(values).all():
        raise ValueError("Portfolio returns must be finite numbers.")

    average_daily = float(np.mean(values))
    daily_volatility = float(np.std(values, ddof=1))

    return {
        "average_daily_return": average_daily,
        "annualized_expected_return": average_daily * TRADING_DAYS_PER_YEAR,
        "annualized_volatility": daily_volatility * np.sqrt(TRADING_DAYS_PER_YEAR),
    }
