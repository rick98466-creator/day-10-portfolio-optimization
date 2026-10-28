"""Additional validation for investment price data."""

import pandas as pd

from portfolio_optimizer.data_loader import ASSET_COLUMNS


def validate_prices(
    prices: pd.DataFrame,
    minimum_observations: int = 2,
) -> None:
    """Raise ValueError if prices are unsuitable for analysis."""
    if minimum_observations < 2:
        raise ValueError("minimum_observations must be at least 2.")

    required = ["Date", *ASSET_COLUMNS]
    missing_columns = [col for col in required if col not in prices.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    if prices.empty or len(prices) < minimum_observations:
        raise ValueError(
            f"At least {minimum_observations} observations are required."
        )

    if prices["Date"].isna().any():
        raise ValueError("Dates cannot be missing.")

    if prices["Date"].duplicated().any():
        raise ValueError("Dates must be unique.")

    if not prices["Date"].is_monotonic_increasing:
        raise ValueError("Dates must be in ascending order.")

    for column in ASSET_COLUMNS:
        numeric = pd.to_numeric(prices[column], errors="coerce")

        if numeric.isna().any():
            raise ValueError(f"{column} contains missing or nonnumeric prices.")

        if not numeric.map(lambda value: float("-inf") < value < float("inf")).all():
            raise ValueError(f"{column} contains non-finite prices.")

        if (numeric <= 0).any():
            raise ValueError(f"{column} prices must be greater than zero.")
