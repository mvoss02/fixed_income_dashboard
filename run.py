import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# Set page config
st.set_page_config(page_title='Bond Analytics Dashboard', layout='wide')


# Load data from Parquet files
@st.cache_data
def load_data(series_id):
    file_path = f'data/{series_id.lower()}.parquet'
    if os.path.exists(file_path):
        return pd.read_parquet(file_path)
    else:
        st.error(f'Data file for {series_id} not found!')
        return pd.DataFrame()


# Yield curve data
treasury_series = [
    'DGS1MO',
    'DGS3MO',
    'DGS6MO',
    'DGS1',
    'DGS2',
    'DGS5',
    'DGS7',
    'DGS10',
    'DGS20',
    'DGS30',
]
corporate_series = ['AAA', 'BAA']
trend_series = ['DGS10', 'T10Y2Y']
portfolio_series = ['DGS1', 'DGS5', 'DGS10', 'BAA']

# Tab layout
tab1, tab2, tab3 = st.tabs(['Yield Curves', 'Historical Trends', 'Portfolio Stats'])

# Tab 1: Yield Curves
with tab1:
    st.header('Yield Curves')
    col1, col2 = st.columns(2)

    latest_date = max([load_data('DGS10').index.max()])  # Assumes DGS10 exists
    date_options = pd.date_range(end=latest_date, periods=365, freq='D')  # Last year
    selected_date = st.sidebar.selectbox(
        'Select Date (for Treasury Yield Curve)',
        options=date_options,
        index=0,
        format_func=lambda x: x.strftime('%Y-%m-%d'),
    )

    # Treasury Yield Curve
    with col1:
        st.subheader('Treasury Yield Curve')
        treasury_yields = {}
        for series in treasury_series:
            df = load_data(series)  # Replace with your actual data loading function
            if selected_date in df.index:
                treasury_yields[series] = df.loc[selected_date, 'yield']

        if treasury_yields:
            # Create figure with consistent size (width, height)
            fig, ax = plt.subplots(figsize=(8, 6))  # Set width=8, height=6
            maturities = [1 / 12, 3 / 12, 6 / 12, 1, 2, 5, 7, 10, 20, 30]
            yields = [treasury_yields[s] for s in treasury_series]
            ax.plot(maturities, yields, marker='o')
            ax.set_xlabel('Maturity (Years)')
            ax.set_ylabel('Yield (%)')
            ax.set_title(f'Treasury Yield Curve - {selected_date.date()}')
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
        else:
            st.warning('Sorry... No data has been found for this day. Try another one!')

    # ESG Proxy (Corporate vs Treasury)
    with col2:
        st.subheader('Corporate vs Treasury (ESG Proxy)')

        # Define the series to load
        corporate_series = ['AAA', 'BAA']
        treasury_series = ['DGS10']
        all_series = corporate_series + treasury_series

        # Load data for each series
        esg_yields = {}
        for series in all_series:
            df = load_data(series)  # Replace with your actual data loading function
            esg_yields[series] = df

        # Check if data was loaded
        if esg_yields:
            # Create figure with consistent size (width, height)
            fig, ax = plt.subplots(figsize=(8, 6))  # Match width=8, height=6

            # Define labels and colors
            labels = ['Aaa (High ESG)', 'Baa (Lower ESG)', '10Y Treasury']
            color_map = {'AAA': 'blue', 'BAA': 'red', 'DGS10': 'green'}

            # Plot each series
            for i, series in enumerate(['AAA', 'BAA', 'DGS10']):
                df = esg_yields[series]
                ax.plot(
                    df.index,
                    df['yield'],
                    color=color_map[series],
                    label=labels[i],
                    alpha=0.6,
                )

            # Customize the plot
            ax.set_ylabel('Yield (%)')
            ax.set_title('ESG Proxy Yields (over time)')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)

            # Display the plot in Streamlit
            st.pyplot(fig)

# Tab 2: Historical Trends
with tab2:
    col1, col2, col3 = st.columns([2, 8, 2])

    with col2:
        st.header('Historical Trends')
        trend_data = {}
        for series in trend_series:
            df = load_data(series)
            if not df.empty:
                trend_data[series] = df

        if trend_data:
            # Create figure with consistent size
            fig, ax = plt.subplots(figsize=(8, 6))

            # Plot each series with distinct colors
            color_map = {
                series: plt.cm.tab10(i) for i, series in enumerate(trend_series)
            }  # Auto-generate colors
            for series in trend_series:
                df = trend_data[series]
                ax.plot(
                    df.index,
                    df['yield'],
                    label=series,
                    color=color_map[series],
                    alpha=0.8,
                )

            # Customize the plot
            ax.set_xlabel('Date')
            ax.set_ylabel('Yield (%)')
            ax.set_title('Historical Yield Trends')
            ax.legend()
            ax.grid(True, linestyle='--', alpha=0.7)  # Match grid style

            # Add left and right margins
            fig.subplots_adjust(
                left=0.1, right=0.9
            )  # Adjust left and right margins (0.3 = 30% margin)

            # Display in Streamlit
            st.pyplot(fig)

# Tab 3: Portfolio Stats
with tab3:
    st.header('Portfolio Summary')
    try:
        portfolio = [
            {'series': 'DGS1', 'weight': 0.2, 'face_value': 1000, 'coupon': 2.0},
            {'series': 'DGS5', 'weight': 0.3, 'face_value': 1000, 'coupon': 2.5},
            {'series': 'DGS10', 'weight': 0.3, 'face_value': 1000, 'coupon': 3.0},
            {'series': 'BAA', 'weight': 0.2, 'face_value': 1000, 'coupon': 4.5},
        ]

        portfolio_df = pd.DataFrame(portfolio)
        for i, row in portfolio_df.iterrows():
            df = load_data(row['series'])
            if selected_date in df.index:
                portfolio_df.loc[i, 'yield'] = df.loc[selected_date, 'yield']

        # Calculate summary stats
        portfolio_df['weighted_yield'] = portfolio_df['weight'] * portfolio_df['yield']
        avg_yield = portfolio_df['weighted_yield'].sum()
        total_value = (portfolio_df['face_value'] * portfolio_df['weight']).sum()

        st.table(portfolio_df[['series', 'weight', 'yield', 'face_value']])
        st.write(f'**Average Weighted Yield**: {avg_yield:.2f}%')
        st.write(f'**Total Portfolio Value**: ${total_value:.2f}')
    except Exception:
        st.warning('Sorry... No data has been found for this day. Try another one!')

    # Define the series
    treasury_series = [
        'DGS1MO',
        'DGS3MO',
        'DGS6MO',
        'DGS1',
        'DGS2',
        'DGS5',
        'DGS7',
        'DGS10',
        'DGS20',
        'DGS30',
    ]
    corporate_series = ['AAA', 'BAA']
    trend_series = ['DGS10', 'T10Y2Y']
    portfolio_series = ['DGS1', 'DGS5', 'DGS10', 'BAA']

    # Create a dictionary with explanations
    bond_explanations = {
        'Series': [
            'DGS1MO',
            'DGS3MO',
            'DGS6MO',
            'DGS1',
            'DGS2',
            'DGS5',
            'DGS7',
            'DGS10',
            'DGS20',
            'DGS30',
            'AAA',
            'BAA',
            'T10Y2Y',
        ],
        'Description': [
            '1-Month Treasury Constant Maturity Rate',
            '3-Month Treasury Constant Maturity Rate',
            '6-Month Treasury Constant Maturity Rate',
            '1-Year Treasury Constant Maturity Rate',
            '2-Year Treasury Constant Maturity Rate',
            '5-Year Treasury Constant Maturity Rate',
            '7-Year Treasury Constant Maturity Rate',
            '10-Year Treasury Constant Maturity Rate',
            '20-Year Treasury Constant Maturity Rate',
            '30-Year Treasury Constant Maturity Rate',
            "Moody's Seasoned Aaa Corporate Bond Yield (highest credit quality)",
            "Moody's Seasoned Baa Corporate Bond Yield (lower investment-grade quality)",
            '10-Year Treasury minus 2-Year Treasury Yield Spread (yield curve indicator)',
        ],
        'Category': [
            'Treasury',
            'Treasury',
            'Treasury',
            'Treasury',
            'Treasury',
            'Treasury',
            'Treasury',
            'Treasury',
            'Treasury',
            'Treasury',
            'Corporate',
            'Corporate',
            'Trend',
        ],
    }

    # Create a DataFrame
    df_bonds = pd.DataFrame(bond_explanations)

    # Display the table in Streamlit (e.g., in a tab or section)
    st.header('Bond Series Explanations')
    st.dataframe(
        df_bonds, use_container_width=True
    )  # Use dataframe for better formatting

if __name__ == '__main__':
    st.write('')
