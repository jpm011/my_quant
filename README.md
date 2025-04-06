# MyQuant - Simple Investment Analysis Tool

A Python-based tool for basic investment analysis and stock market data visualization. This project provides a simple way to analyze stocks, calculate key metrics, and generate investment reports.

## Features

- Fetch historical stock data using Yahoo Finance API
- Calculate key investment metrics:
  - Daily and annualized returns
  - Volatility
  - Sharpe ratio
  - Moving averages (50-day and 200-day)
  - Trend analysis
- Generate comprehensive investment reports
- Visualize stock data with moving averages
- Support for multiple stocks analysis

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jpm011/my_quant.git
cd my_quant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/MacOS
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

```python
from main import SimpleInvestmentAnalyzer

# Initialize the analyzer
analyzer = SimpleInvestmentAnalyzer()

# Fetch data for stocks
tickers = ['AAPL', 'MSFT', 'GOOGL']
analyzer.fetch_data(tickers)

# Generate analysis report for a stock
analyzer.generate_report('AAPL')
```

## Example Output

The tool generates reports including:
- Current price and moving averages
- Trend analysis (Bullish/Bearish)
- Annualized return and volatility
- Sharpe ratio
- Simple investment recommendation
- Visual chart with price and moving averages

## Dependencies

- pandas
- numpy
- yfinance
- matplotlib

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. It should not be used as the sole basis for making investment decisions. Always do your own research and consult with a qualified financial advisor before making investment decisions. 