import os
from os.path import exists
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import re

def GetTicker(symbol):
    if not os.path.exists(symbol):
        os.makedirs(symbol)
    
    today = datetime.today()
    filename = f"{symbol}/{today.strftime('%Y-%m-%d')}_{symbol}.csv"
    
    # Calculate days since latest data file if files exist
    period_days = '730d'  # Default fallback period
    if os.path.exists(symbol) and len(os.listdir(symbol)) > 0:
        # Extract dates from filenames
        date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2})_')
        dates = []
        for file in os.listdir(symbol):
            match = date_pattern.search(file)
            if match:
                try:
                    file_date = datetime.strptime(match.group(1), '%Y-%m-%d')
                    dates.append(file_date)
                except ValueError:
                    continue
        
        if dates:
            # Get the latest date from the files
            latest_date = max(dates)
            # Calculate days difference
            days_diff = (today - latest_date).days
            # Add a small buffer (e.g., 10 days) to ensure overlap
            period_days = f'{max(days_diff + 10, 30)}d'  # At least 30 days
    
    if not exists(filename):
        quote = yf.Ticker(symbol)
        history = quote.history(period=period_days, auto_adjust=False)
        
        # Convert datetime index to date only (strip time portion)
        history.index = history.index.date
        
        history.to_csv(filename, index=True)
        time.sleep(1)
    
    dfs = []
    for filename in os.listdir(symbol):
        file_path = os.path.join(symbol, filename)
        
        # First, check the file format by looking at the first few rows
        with open(file_path, 'r') as f:
            header = f.readline().strip()
        
        # Determine if the first column is likely a date index
        if header.startswith('Date,') or header.startswith('"Date",'):
            # Date is a column name
            df = pd.read_csv(file_path)
            # Convert Date column to date objects
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            df.set_index('Date', inplace=True)
        else:
            # Date might be the index already
            df = pd.read_csv(file_path, index_col=0)
            # Convert index to datetime and then to date objects
            df.index = pd.to_datetime(df.index).date
        
        dfs.append(df)
    
    # Concatenate all dataframes
    if dfs:
        df = pd.concat(dfs)
        
        # Remove duplicates that might occur due to overlapping date ranges
        df = df[~df.index.duplicated(keep='last')]
        
        # Sort by date
        df = df.sort_index()
        
        return df
    
    return pd.DataFrame()  # Return empty dataframe if no files were found