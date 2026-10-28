"""Load investment price data from a CSV file."""

from pathlib import Path

import pandas as pd


ASSET_COLUMNS = ["Asset_A", "Asset_B", "Asset_C"]


def load_prices(path: str | Path) -> pd.DataFrame:
    """Load dated asset prices and return a validated DataFrame."""
    csv_path = Path(path)

    if not csv_path.is_file():
        raise FileNotFoundError(f"Price data file not found: {csv_path}")

    prices = pd.read_csv(csv_path)

    required_columns = ["Date", *ASSET_COLUMNS]
    missing_columns = [
        column for column in required_columns
        if column not in prices.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    prices = prices[required_columns].copy()
    prices["Date"] = pd.to_datetime(prices["Date"], errors="raise")

    for column in ASSET_COLUMNS:
        prices[column] = pd.to_numeric(prices[column], errors="raise")

    if prices.empty:
        raise ValueError("Price data is empty.")

    if prices["Date"].isna().any():
        raise ValueError("Dates cannot be missing.")

    if prices["Date"].duplicated().any():
        raise ValueError("Dates must be unique.")

    if not prices["Date"].is_monotonic_increasing:
        raise ValueError("Dates must be in ascending order.")

    if prices[ASSET_COLUMNS].isna().any().any():
        raise ValueError("Asset prices cannot be missing.")

    if not (prices[ASSET_COLUMNS] > 0).all().all():
        raise ValueError("Asset prices must be greater than zero.")

    return prices
