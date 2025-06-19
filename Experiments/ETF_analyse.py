import yfinance as yf
import pandas as pd
from datetime import datetime
# Load ASX tickers from CSV
def load_tickers(file_path):
   try:
       tickers_df = pd.read_csv(file_path)
       return tickers_df['Ticker'].tolist()
   except Exception as e:
       print(f"Error loading tickers: {e}")
       return []
# Analyze a single stock for buy signal
def analyze_stock(ticker):
   try:
       etf = yf.Ticker(ticker)
       data = etf.history(period="3mo")
       #print (data)
       # Check if there's enough data
       if len(data) < 200 or data.empty:
           print(f"Not enough data for {ticker}. Skipping.")
           return None
       # Calculate moving averages
       data['SMA50'] = data['Close'].rolling(window=50).mean()
       data['SMA200'] = data['Close'].rolling(window=200).mean()
       # Check for buy signal (50-day SMA crosses above 200-day SMA)
       buy_signal = (data['SMA50'].iloc[-1] > data['SMA200'].iloc[-1]) and \
                    (data['SMA50'].iloc[-2] <= data['SMA200'].iloc[-2])
       if buy_signal:
           return ticker
   except Exception as e:
       print(f"Error analyzing {ticker}: {e}")
   return None
# Scan all ASX tickers
def scan_asx_market(tickers):
   print(f"Scanning ASX market at {datetime.now()}")
   buy_signals = []
   for ticker in tickers:
       print(f"Analyzing {ticker}...")
       result = analyze_stock(ticker)
       if result:
           buy_signals.append(result)
   return buy_signals
# Main function
if __name__ == "__main__":
   # Load ASX tickers from file
   asx_tickers = load_tickers("asx_tickers.csv")
   if not asx_tickers:
       print("No tickers to analyze. Exiting.")
       exit()
   # Scan the ASX market
   buy_signals = scan_asx_market(asx_tickers)
   # Print results
   if buy_signals:
       print("Buy signals detected for the following stocks:")
       for signal in buy_signals:
           print(signal)
   else:
       print("No buy signals detected.")