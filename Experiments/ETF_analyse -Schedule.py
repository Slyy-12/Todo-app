import yfinance as yf
import pandas as pd
from datetime import datetime
import concurrent.futures
import numpy as np
import schedule
import time
# Load ASX tickers from CSV
def load_tickers(file_path):
   try:
       tickers_df = pd.read_csv(file_path, encoding="utf-8-sig")
       return tickers_df['Ticker'].tolist()
   except UnicodeDecodeError as e:
       print(f"Encoding error: {e}. Trying with 'latin1'...")
       try:
           tickers_df = pd.read_csv(file_path, encoding="latin1")
           return tickers_df['Ticker'].tolist()
       except Exception as e:
           print(f"Error loading tickers: {e}")
           return []
   except Exception as e:
       print(f"Error loading tickers: {e}")
       return []
# Calculate RSI (Relative Strength Index)
def calculate_rsi(data, period=14):
   delta = data['Close'].diff()
   gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
   loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
   rs = gain / loss
   rsi = 100 - (100 / (1 + rs))
   return rsi
# Analyze a single stock for buy signal with enhanced strategy
def analyze_stock(ticker):
   try:
       etf = yf.Ticker(ticker)
       data = etf.history(period="1y")
       # Check if there's enough data
       if len(data) < 200 or data.empty:
           return None
       # Calculate moving averages
       data['SMA50'] = data['Close'].rolling(window=50).mean()
       data['SMA200'] = data['Close'].rolling(window=200).mean()
       # Calculate RSI
       data['RSI'] = calculate_rsi(data)
       # Calculate MACD and Signal Line
       data['MACD'] = data['Close'].ewm(span=12, adjust=False).mean() - data['Close'].ewm(span=26, adjust=False).mean()
       data['Signal Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
       # Check for buy signal:
       # 1. 50-day SMA crosses above 200-day SMA
       # 2. RSI is below 70 (not overbought)
       # 3. Volume is 20% higher than 50-day average volume
       # 4. MACD crosses above the Signal Line (bullish crossover)
       # Conditions for buy signal
       crossover = (data['SMA50'].iloc[-1] > data['SMA200'].iloc[-1]) and (data['SMA50'].iloc[-2] <= data['SMA200'].iloc[-2])
       rsi_condition = data['RSI'].iloc[-1] < 70  # RSI below 70
       volume_condition = data['Volume'].iloc[-1] > 1.2 * data['Volume'].rolling(window=50).mean().iloc[-1]  # 20% higher volume
       macd_condition = data['MACD'].iloc[-1] > data['Signal Line'].iloc[-1] and data['MACD'].iloc[-2] <= data['Signal Line'].iloc[-2]
       # Final buy signal condition
       if crossover and rsi_condition and volume_condition and macd_condition:
           return ticker
   except Exception as e:
       print(f"Error analyzing {ticker}: {e}")
   return None
# Scan all ASX tickers using parallel processing
def scan_asx_market(tickers):
   print(f"Scanning ASX market at {datetime.now()}")
   buy_signals = []
   with concurrent.futures.ThreadPoolExecutor() as executor:
       results = executor.map(analyze_stock, tickers)
       for result in results:
           if result:
               buy_signals.append(result)
   return buy_signals
# Save buy signals to a file
def save_results(buy_signals, file_name="buy_signals.csv"):
   try:
       timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
       df = pd.DataFrame({"Ticker": buy_signals, "Timestamp": timestamp})
       df.to_csv(file_name, index=False)
       print(f"Buy signals saved to {file_name}")
   except Exception as e:
       print(f"Error saving results: {e}")
# Main function to execute the analysis
def daily_analysis():
   # Load ASX tickers from file
   asx_tickers = load_tickers("asx_tickers.csv")
   if not asx_tickers:
       print("No tickers to analyze. Exiting.")
       return
   # Scan the ASX market for buy signals
   buy_signals = scan_asx_market(asx_tickers)
   # Print and save results
   if buy_signals:
       print("Buy signals detected for the following stocks:")
       for signal in buy_signals:
           print(signal)
       save_results(buy_signals)
   else:
       print("No buy signals detected.")
# Schedule the script to run at 6 PM every day
schedule.every().day.at("18:00").do(daily_analysis)
# Run the scheduled tasks
while True:
   schedule.run_pending()
   time.sleep(60)  # Wait for 1 minute before checking the schedule again