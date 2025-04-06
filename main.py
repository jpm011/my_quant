import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import os

class SimpleInvestmentAnalyzer:
    def __init__(self):
        self.data = None
        self.tickers = []
        self.test_mode = False
        self.test_data_path = "test_data"
        
    def enable_test_mode(self):
        """Enable test mode to use local test data"""
        self.test_mode = True
        if not os.path.exists(self.test_data_path):
            os.makedirs(self.test_data_path)
        
    def fetch_data(self, tickers, period='1y'):
        """
        Fetch historical data for given tickers
        tickers: list of stock symbols
        period: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
        self.tickers = tickers
        self.data = {}
        
        for ticker in tickers:
            try:
                if self.test_mode:
                    # Try to load from test data
                    test_file = os.path.join(self.test_data_path, f"{ticker}_test_data.csv")
                    if os.path.exists(test_file):
                        self.data[ticker] = pd.read_csv(test_file, index_col=0, parse_dates=True)
                        print(f"Loaded test data for {ticker}")
                    else:
                        # Generate test data if not exists
                        self._generate_test_data(ticker)
                else:
                    # Fetch real data
                    stock = yf.Ticker(ticker)
                    self.data[ticker] = stock.history(period=period)
                print(f"Successfully fetched data for {ticker}")
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
        
        return self.data
    
    def _generate_test_data(self, ticker):
        """Generate synthetic test data for a ticker"""
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
        np.random.seed(42)  # For reproducibility
        
        # Generate random walk for prices
        price_changes = np.random.normal(0.001, 0.02, len(dates))
        prices = 100 * (1 + np.cumsum(price_changes))
        
        # Create DataFrame
        df = pd.DataFrame({
            'Open': prices * (1 + np.random.normal(0, 0.001, len(dates))),
            'High': prices * (1 + np.abs(np.random.normal(0, 0.002, len(dates)))),
            'Low': prices * (1 - np.abs(np.random.normal(0, 0.002, len(dates)))),
            'Close': prices,
            'Volume': np.random.randint(1000000, 5000000, len(dates))
        }, index=dates)
        
        # Save test data
        test_file = os.path.join(self.test_data_path, f"{ticker}_test_data.csv")
        df.to_csv(test_file)
        
        self.data[ticker] = df
        print(f"Generated test data for {ticker}")
    
    def calculate_metrics(self, ticker):
        """Calculate basic investment metrics for a given ticker"""
        if ticker not in self.data or self.data[ticker].empty:
            print(f"No data available for {ticker}")
            return None
            
        df = self.data[ticker]
        metrics = {}
        
        # Calculate daily returns
        df['Daily_Return'] = df['Close'].pct_change()
        
        # Basic metrics
        metrics['avg_daily_return'] = df['Daily_Return'].mean()
        metrics['annualized_return'] = metrics['avg_daily_return'] * 252  # Approx trading days in a year
        metrics['volatility'] = df['Daily_Return'].std() * np.sqrt(252)  # Annualized volatility
        metrics['sharpe_ratio'] = metrics['annualized_return'] / metrics['volatility']  # Simple Sharpe ratio (assumes risk-free rate = 0)
        
        # Moving averages
        df['MA50'] = df['Close'].rolling(window=50).mean()
        df['MA200'] = df['Close'].rolling(window=200).mean()
        
        # Current trend
        current_price = df['Close'].iloc[-1]
        metrics['current_price'] = current_price
        metrics['ma50'] = df['MA50'].iloc[-1]
        metrics['ma200'] = df['MA200'].iloc[-1]
        
        # Simple trend analysis
        if metrics['ma50'] > metrics['ma200']:
            metrics['trend'] = 'Bullish'
        else:
            metrics['trend'] = 'Bearish'
            
        return metrics
    
    def visualize_stock(self, ticker):
        """Create a visualization of stock data with key indicators"""
        if ticker not in self.data or self.data[ticker].empty:
            print(f"No data available for {ticker}")
            return
            
        df = self.data[ticker]
        
        # Create plot with close price and moving averages
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['Close'], label='Close Price')
        plt.plot(df.index, df['MA50'], label='50-day MA', alpha=0.7)
        plt.plot(df.index, df['MA200'], label='200-day MA', alpha=0.7)
        
        plt.title(f'{ticker} Stock Price with Moving Averages')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save plot in test mode
        if self.test_mode:
            plot_path = os.path.join(self.test_data_path, f"{ticker}_plot.png")
            plt.savefig(plot_path)
            print(f"Saved plot to {plot_path}")
        
        plt.show()
    
    def generate_report(self, ticker):
        """Generate a simple investment report for a given stock"""
        metrics = self.calculate_metrics(ticker)
        if not metrics:
            return
            
        report = {
            "ticker": ticker,
            "current_price": metrics['current_price'],
            "ma50": metrics['ma50'],
            "ma200": metrics['ma200'],
            "trend": metrics['trend'],
            "annualized_return": metrics['annualized_return'],
            "volatility": metrics['volatility'],
            "sharpe_ratio": metrics['sharpe_ratio']
        }
        
        # Simple recommendation based on trend and Sharpe ratio
        if metrics['trend'] == 'Bullish' and metrics['sharpe_ratio'] > 1:
            recommendation = "Consider Buying: Positive trend with good risk-adjusted returns"
        elif metrics['trend'] == 'Bullish' and metrics['sharpe_ratio'] <= 1:
            recommendation = "Hold/Watch: Positive trend but lower risk-adjusted returns"
        elif metrics['trend'] == 'Bearish' and metrics['sharpe_ratio'] > 0.5:
            recommendation = "Hold with Caution: Negative trend but still some positive risk-adjusted returns"
        else:
            recommendation = "Consider Selling/Avoiding: Negative trend with poor risk-adjusted returns"
            
        report["recommendation"] = recommendation
        
        # Save report in test mode
        if self.test_mode:
            report_path = os.path.join(self.test_data_path, f"{ticker}_report.json")
            with open(report_path, 'w') as f:
                json.dump(report, f, indent=4)
            print(f"Saved report to {report_path}")
        
        # Print report
        print(f"\n==== Investment Analysis for {ticker} ====")
        print(f"Current Price: ${metrics['current_price']:.2f}")
        print(f"50-day Moving Average: ${metrics['ma50']:.2f}")
        print(f"200-day Moving Average: ${metrics['ma200']:.2f}")
        print(f"Current Trend: {metrics['trend']}")
        print(f"Annualized Return: {metrics['annualized_return']*100:.2f}%")
        print(f"Annualized Volatility: {metrics['volatility']*100:.2f}%")
        print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
        print(f"Simple Recommendation: {recommendation}")
        print("\nNote: This is a basic analysis. Real investment decisions should consider")
        print("additional factors and ideally be made with professional financial advice.")
        
        # Visualize the stock
        self.visualize_stock(ticker)
        
        return report


# Example usage
if __name__ == "__main__":
    analyzer = SimpleInvestmentAnalyzer()
    
    # Enable test mode
    analyzer.enable_test_mode()
    
    # Fetch data for a few tech stocks
    tickers = ['AAPL', 'MSFT', 'GOOGL']
    analyzer.fetch_data(tickers)
    
    # Generate reports
    for ticker in tickers:
        analyzer.generate_report(ticker)