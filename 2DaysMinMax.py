#%% 
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import time
import yahoo_finance_helper as yfhelper

#%%
# Fetch historical data for TSLA over the past 30 days
ticker = 'TSLA'
data = yfhelper.GetTicker(ticker)

#%%
# Filter for last 90 days
# Create a cutoff date 120 days in the past
cutoff_date = (pd.Timestamp.now() - pd.Timedelta(days=120)).date()
print(cutoff_date)

# Convert cutoff_date to datetime.date for comparison with data.index
# data.index contains datetime.date objects (no time component) 
# as seen in yahoo_finance_helper.py

# Filter data after cutoff date and verify the filtering worked
data = data[data.index >= cutoff_date]
print(f"First date in filtered data: {data.index.min()}")
print(f"Cutoff date was: {cutoff_date}")
# Print first and last 5 rows
print("\nFirst 5 rows:")
print(data.head())
print("\nLast 5 rows:")
print(data.tail())

#%%
# Convert index from datetime.date to pandas DatetimeIndex
data.index = pd.to_datetime(data.index)

# Now we can use dayofweek attribute
data['DayOfWeek'] = data.index.dayofweek

# Filter for Wednesdays and Fridays
wf_data = data[data['DayOfWeek'].isin([2, 4])].copy()


# Add year and week columns
wf_data['Year'] = wf_data.index.year
wf_data['Week'] = wf_data.index.isocalendar().week

# Group by year and week
grouped = wf_data.groupby(['Year', 'Week'])


#%%
# Calculate percentage changes for each complete Wednesday-Friday pair
percentage_changes = []
friday_dates = []
wednesday_dates = []
wednesday_prices = []
friday_prices = []

for name, group in grouped:
    if len(group) == 2:  # Ensure exactly two days in the group
        group = group.sort_index()  # Sort by date
        if group.iloc[0]['DayOfWeek'] == 2 and group.iloc[1]['DayOfWeek'] == 4:
            wed_close = group.iloc[0]['Close']  # Using 'Close' instead of 'Adj Close'
            fri_close = group.iloc[1]['Close']
            pct_change = ((fri_close - wed_close) / wed_close) * 100
            percentage_changes.append(pct_change)
            friday_dates.append(group.iloc[1].name)  # Store the Friday date
            wednesday_dates.append(group.iloc[0].name)  # Store the Wednesday date
            wednesday_prices.append(wed_close)
            friday_prices.append(fri_close)

# Find min and max percentage changes and display results
if percentage_changes:
    min_pct_change = min(percentage_changes)
    max_pct_change = max(percentage_changes)
    print(f"Minimum percentage change from Wednesday to Friday for {ticker}: {min_pct_change:.2f}%")
    print(f"Maximum percentage change from Wednesday to Friday for {ticker}: {max_pct_change:.2f}%")
    
    # Create an interactive plot with Plotly
    hover_text = [f'Week: {friday.isocalendar().week}, Year: {friday.year}<br>'
                 f'Wed ({wednesday.strftime("%Y-%m-%d")}): ${wed_price:.2f}<br>'
                 f'Fri ({friday.strftime("%Y-%m-%d")}): ${fri_price:.2f}<br>'
                 f'Change: {pct_change:.2f}%' 
                 for friday, wednesday, wed_price, fri_price, pct_change in 
                 zip(friday_dates, wednesday_dates, wednesday_prices, friday_prices, percentage_changes)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[date.strftime('%Y-%m-%d') for date in friday_dates],
        y=percentage_changes,
        mode='lines+markers',
        name='Percentage Change',
        text=hover_text,
        hoverinfo='text',
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title=f'Percentage Change from Wednesday to Friday for {ticker}',
        xaxis_title='Friday Date',
        yaxis_title='Percentage Change (%)',
        hovermode='closest',
        xaxis=dict(tickangle=45)
    )
    
    try:
        fig.show()
    except Exception as e:
        print(f"Could not display figure directly due to: {e}")
        print("Saving figure to HTML file instead...")
        fig.write_html(f"{ticker}_wed_fri_changes.html")
        print(f"Figure saved as {ticker}_wed_fri_changes.html - please open this file in a browser")
else:
    print("No complete Wednesday-Friday pairs found in the last 30 days.")
# %%
