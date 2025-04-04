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

# Sidebar for date selection
st.sidebar.header('Settings')
latest_date = max([load_data('DGS10').index.max()])  # Assumes DGS10 exists
date_options = pd.date_range(end=latest_date, periods=365, freq='D')  # Last year
selected_date = st.sidebar.selectbox(
    'Select Date',
    options=date_options,
    index=0,
    format_func=lambda x: x.strftime('%Y-%m-%d'),
)

# Tab layout
tab1, tab2, tab3 = st.tabs(['Yield Curves', 'Historical Trends', 'Portfolio Stats'])

# Tab 1: Yield Curves
with tab1:
    st.header('Yield Curves')
    col1, col2 = st.columns(2)

    # Treasury Yield Curve
    with col1:
        st.subheader('Treasury Yield Curve')
        treasury_yields = {}
        for series in treasury_series:
            df = load_data(series)
            if selected_date in df.index:
                treasury_yields[series] = df.loc[selected_date, 'yield']
        if treasury_yields:
            fig, ax = plt.subplots()
            maturities = [1 / 12, 3 / 12, 6 / 12, 1, 2, 5, 7, 10, 20, 30]
            yields = [treasury_yields[s] for s in treasury_series]
            ax.plot(maturities, yields, marker='o')
            ax.set_xlabel('Maturity (Years)')
            ax.set_ylabel('Yield (%)')
            ax.set_title(f'Treasury Yield Curve - {selected_date.date()}')
            st.pyplot(fig)

    # ESG Proxy (Corporate vs Treasury)
    with col2:
        st.subheader('Corporate vs Treasury (ESG Proxy)')
        esg_yields = {}
        for series in corporate_series + ['DGS10']:
            df = load_data(series)
            if selected_date in df.index:
                esg_yields[series] = df.loc[selected_date, 'yield']
        if esg_yields:
            fig, ax = plt.subplots()
            labels = ['Aaa (High ESG)', 'Baa (Lower ESG)', '10Y Treasury']
            yields = [esg_yields[s] for s in ['AAA', 'BAA', 'DGS10']]
            ax.bar(labels, yields)
            ax.set_ylabel('Yield (%)')
            ax.set_title(f'ESG Proxy Yields - {selected_date.date()}')
            st.pyplot(fig)

# Tab 2: Historical Trends
with tab2:
    st.header('Historical Trends')
    for series in trend_series:
        df = load_data(series)
        if not df.empty:
            fig, ax = plt.subplots()
            ax.plot(df.index, df['yield'], label=series)
            ax.set_xlabel('Date')
            ax.set_ylabel('Yield (%)')
            ax.set_title(f'{series} Trend')
            ax.legend()
            st.pyplot(fig)

# Tab 3: Portfolio Stats
with tab3:
    st.header('Portfolio Summary')
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

if __name__ == '__main__':
    st.write('Dashboard ready!')
