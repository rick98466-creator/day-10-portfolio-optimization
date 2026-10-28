"""Calculate simple daily returns from investment prices."""

import pandas as pd

from portfolio_optimizer.data_loader import ASSET_COLUMNS
from portfolio_optimizer.validation import validate_prices


def calculate_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Return a DataFrame of daily returns, excluding the first date."""
    validate_prices(prices)

    returns = prices[ASSET_COLUMNS].pct_change(fill_method=None).iloc[1:].copy()
    returns.insert(0, "Date", prices["Date"].iloc[1:].to_numpy())

    if returns[ASSET_COLUMNS].isna().any().any():
        raise ValueError("Calculated returns contain missing values.")

    return returns.reset_index(drop=True)
