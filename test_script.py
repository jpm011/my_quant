from main import SimpleInvestmentAnalyzer
import os

def run_tests():
    # Initialize analyzer
    analyzer = SimpleInvestmentAnalyzer()
    
    # Enable test mode
    analyzer.enable_test_mode()
    
    # Test with different stocks
    test_stocks = ['TEST1', 'TEST2', 'TEST3']
    
    print("=== Starting Test Run ===")
    print(f"Test data will be saved in: {analyzer.test_data_path}")
    
    # Fetch and analyze data
    analyzer.fetch_data(test_stocks)
    
    # Generate reports
    for stock in test_stocks:
        print(f"\nAnalyzing {stock}...")
        report = analyzer.generate_report(stock)
        
        # Verify files were created
        test_files = [
            f"{stock}_test_data.csv",
            f"{stock}_plot.png",
            f"{stock}_report.json"
        ]
        
        print("\nVerifying test files:")
        for file in test_files:
            file_path = os.path.join(analyzer.test_data_path, file)
            if os.path.exists(file_path):
                print(f"✓ {file} created successfully")
            else:
                print(f"✗ {file} not found")
    
    print("\n=== Test Run Completed ===")
    print("Check the test_data directory for generated files")

if __name__ == "__main__":
    run_tests() 