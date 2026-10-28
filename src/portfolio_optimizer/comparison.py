"""Compare predefined portfolio allocation strategies."""

import numpy as np
import pandas as pd

from portfolio_optimizer.data_loader import load_prices
from portfolio_optimizer.portfolio import (
    calculate_portfolio_returns,
    summarize_portfolio,
)
from portfolio_optimizer.returns import calculate_returns
from portfolio_optimizer.validation import validate_prices


ALLOCATIONS = {
    "Equal Weight": {
        "Asset_A": 1 / 3,
        "Asset_B": 1 / 3,
        "Asset_C": 1 / 3,
    },
    "Conservative": {
        "Asset_A": 0.25,
        "Asset_B": 0.60,
        "Asset_C": 0.15,
    },
    "Growth Oriented": {
        "Asset_A": 0.20,
        "Asset_B": 0.20,
        "Asset_C": 0.60,
    },
}


def compare_allocations(
    asset_returns: pd.DataFrame,
    risk_free_rate: float = 0.0,
) -> pd.DataFrame:
    """Compare historical return, volatility, and Sharpe ratio."""
    if not np.isfinite(risk_free_rate):
        raise ValueError("Risk-free rate must be finite.")

    rows = []

    for name, weights in ALLOCATIONS.items():
        daily = calculate_portfolio_returns(asset_returns, weights)
        summary = summarize_portfolio(daily)

        volatility = summary["annualized_volatility"]
        excess_return = summary["annualized_expected_return"] - risk_free_rate

        sharpe = excess_return / volatility if volatility > 0 else np.nan

        rows.append({
            "Portfolio": name,
            "Annualized_Expected_Return": summary["annualized_expected_return"],
            "Annualized_Volatility": volatility,
            "Sharpe_Ratio": sharpe,
        })

    return pd.DataFrame(rows)


def main() -> None:
    prices = load_prices("data/raw/investment_prices.csv")
    validate_prices(prices)
    returns = calculate_returns(prices)
    results = compare_allocations(returns)

    print("Historical allocation comparison")
    print("(Synthetic educational data; not investment advice.)\n")
    print(results.to_string(index=False, float_format=lambda value: f"{value:.4f}"))


if __name__ == "__main__":
    main()
