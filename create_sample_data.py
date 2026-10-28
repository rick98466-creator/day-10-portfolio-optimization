from pathlib import Path
import numpy as np
import pandas as pd

output = Path("data/raw/investment_prices.csv")
output.parent.mkdir(parents=True, exist_ok=True)

dates = pd.bdate_range(start="2026-01-05", periods=60)

# Synthetic daily returns: reproducible, for learning only.
rng = np.random.default_rng(42)
daily_returns = rng.normal(
    loc=[0.0005, 0.0003, 0.0007],
    scale=[0.010, 0.007, 0.015],
    size=(len(dates) - 1, 3),
)

returns = pd.DataFrame(
    daily_returns,
    columns=["Asset_A", "Asset_B", "Asset_C"],
)

prices = pd.DataFrame(
    index=dates,
    columns=["Asset_A", "Asset_B", "Asset_C"],
    dtype=float,
)
prices.iloc[0] = [100.0, 100.0, 100.0]

for i in range(1, len(dates)):
    prices.iloc[i] = prices.iloc[i - 1] * (1 + returns.iloc[i - 1].to_numpy())

prices.insert(0, "Date", dates.strftime("%Y-%m-%d"))
prices.to_csv(output, index=False, float_format="%.6f")

check = pd.read_csv(output, parse_dates=["Date"])

assert len(check) == 60
assert check["Date"].is_monotonic_increasing
assert check["Date"].is_unique
assert check[["Asset_A", "Asset_B", "Asset_C"]].notna().all().all()
assert (check[["Asset_A", "Asset_B", "Asset_C"]] > 0).all().all()

print(f"Created: {output}")
print(f"Rows: {len(check)}")
print(f"Date range: {check['Date'].min().date()} to {check['Date'].max().date()}")
print("\nFirst five rows:")
print(check.head().to_string(index=False))
print("\nLast recorded prices:")
print(check.iloc[-1].to_string(index=False))
print("\nSynthetic data checks: PASSED")
