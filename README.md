# Financial Portfolio Allocation & Optimization

A Python project for validating financial price data, calculating daily returns, and comparing portfolio allocations.

## Features
- Price data validation
- Daily asset return calculation
- Portfolio return and risk metrics
- Equal-weight, conservative, and growth-oriented allocation comparison
- Excel and CSV report generation
- Automated tests

## Setup
Activate the virtual environment with: .\.venv\Scripts\Activate.ps1
Install dependencies with: python -m pip install numpy pandas openpyxl pytest

## Run Tests
Set PYTHONPATH to src, then run: python -m pytest tests -v

## Generate Excel Report
Run: python -m portfolio_optimizer.reporting

## Methodology
Daily simple returns are calculated from consecutive prices. Annualized metrics use 252 trading days per year.

## Data and Limitations
Sample prices are synthetic and do not represent actual market data. Historical estimates do not guarantee future performance. This project is for educational analysis and is not personalized investment advice.

## Quality Checks
Run the automated tests and inspect report labels, units, and calculations before sharing results.
