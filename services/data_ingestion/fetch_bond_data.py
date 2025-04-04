import os
from datetime import datetime

import pandas as pd
from fredapi import Fred
from loguru import logger

from config.config_variables import data_credentials_config

# Set up FRED API (replace with your API key)
fred = Fred(api_key=data_credentials_config.api_key)

# Define FRED series for yield curves, ESG proxy, historical trends, and portfolio
series_dict = {
    'DGS1MO': '1-Month Treasury',
    'DGS3MO': '3-Month Treasury',
    'DGS6MO': '6-Month Treasury',
    'DGS1': '1-Year Treasury',
    'DGS2': '2-Year Treasury',
    'DGS5': '5-Year Treasury',
    'DGS7': '7-Year Treasury',
    'DGS10': '10-Year Treasury',
    'DGS20': '20-Year Treasury',
    'DGS30': '30-Year Treasury',
    'AAA': 'Moody’s Aaa Corporate',
    'BAA': 'Moody’s Baa Corporate',
    'T10Y2Y': '10Y-2Y Spread',
}

# Create data directory if it doesn’t exist
os.makedirs('data', exist_ok=True)

# Fetch data and save as Parquet
start_date = '2000-01-01'  # Adjust as needed
end_date = datetime.today().strftime('%Y-%m-%d')
logger.info(
    f'Start date for all series is defined as: {start_date}. The end time is {end_date}.'
)

for series_id, name in series_dict.items():
    logger.info(f'Fetching {name} ({series_id})...')
    try:
        # Fetch series
        data = fred.get_series(
            series_id, observation_start=start_date, observation_end=end_date
        )

        # Convert to DataFrame with date index
        df = pd.DataFrame(data, columns=['yield'])
        df.index.name = 'date'

        # Save each series to individual Parquet file
        file_path = f'data/{series_id.lower()}.parquet'
        df.to_parquet(file_path)

        logger.success(f'Saved to {file_path}')

    except Exception as e:
        logger.error(f'Error fetching {series_id}: {e}')

logger.info('Data fetch complete!')
