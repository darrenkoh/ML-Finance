# ML-Finance

A Python-based project that applies machine learning techniques to financial market analysis, focusing on stock price patterns and trading strategies.

## Project Overview

ML-Finance uses data science and machine learning to analyze stock market data, identify patterns, and develop potential trading strategies. The project includes tools for:

- Fetching and processing historical stock data from Yahoo Finance
- Analyzing price movements between specific days (e.g., Wednesday to Friday patterns)
- Implementing time series clustering and pattern recognition
- Visualizing financial data and analysis results

## Features

- **Historical Data Analysis**: Retrieve and analyze historical stock price data
- **Day-of-Week Analysis**: Examine stock price behavior between specific days (e.g., Wednesday to Friday)
- **Time Series Analysis**: Apply clustering and pattern detection to identify recurring price movements
- **Interactive Visualizations**: View price trends and analytical results through interactive charts

## Project Structure

- `main.ipynb`: Main analysis notebook implementing ML techniques for stock data analysis
- `Simple_2_days_Min_Max.ipynb`: Analysis of min/max price changes over 2-day periods
- `2DaysMinMax.py`: Python script version of the 2-day analysis
- `yahoo_finance_helper.py`: Helper functions for fetching and processing Yahoo Finance data
- `PGE_TESLA.ipynb`: Specific analysis for PG&E and Tesla stocks
- `TSLA/`, `NVDA/`: Directories containing cached stock data for Tesla and NVIDIA

## Getting Started

### Prerequisites

- Python 3.10+
- Required packages (available in requirements.txt):
  - numpy
  - pandas
  - matplotlib
  - plotly
  - yfinance
  - tslearn
  - kneed
  - ipywidgets
  - nbformat

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ML-Finance.git
   cd ML-Finance
   ```

2. Set up a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

1. Start with the Jupyter notebooks to explore the analyses:
   ```bash
   jupyter notebook
   ```

2. Open one of the notebook files (`.ipynb`) to explore specific analyses:
   - `main.ipynb` - For the main machine learning analysis
   - `Simple_2_days_Min_Max.ipynb` - For the 2-day price movement analysis

3. To use the Python script version of the analysis:
   ```bash
   python 2DaysMinMax.py
   ```

## How It Works

### Data Collection

The project uses `yahoo_finance_helper.py` to fetch stock data from Yahoo Finance. Data is cached locally in ticker-specific directories to minimize API calls.

### Analysis Methods

1. **Day-of-Week Analysis**: Examines price changes between specific days (e.g., Wednesday to Friday) to identify potential trading patterns.

2. **Time Series Clustering**: Uses TimeSeriesKMeans from tslearn to identify recurring patterns in stock price movements.

3. **Pattern Visualization**: Employs matplotlib and plotly to create interactive visualizations of the analysis results.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Yahoo Finance for providing the financial data
- The open-source community for developing the tools and libraries used in this project