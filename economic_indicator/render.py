import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots

# Database connection parameters
database = 'postgres'
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = 5432

# Creating an SQLAlchemy engine
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')

# SQL query to fetch data
query = "SELECT * FROM economic_indicators;"

# Connect to the database and fetch data using SQLAlchemy
try:
    data = pd.read_sql_query(query, engine)
except Exception as e:
    print("An error occurred:", e)

# Plotly Visualizations
fig = make_subplots(
    rows=5, cols=1,
    subplot_titles=('GDP Growth Rate Trends (1973-2022)',
                    'Correlation Heatmap of Economic Indicators',
                    'GDP Growth Rate Predictions for IN, VN, and ID (2023-2032)',
                    'GDP Growth Rate Predictions for SG, KR, and MY (2023-2032)',
                    'GDP Growth Rate Predictions (2023-2032)'),
    vertical_spacing=0.08
)

# Selecting features for the model
training_features = [
    'population_growth_rate',
    'gni_per_capita',
    'inflation_rate',
    'government_debt',
    'fdi_net_inflows',
    'ease_of_doing_business',
    'export_percent_gdp',
    'import_percent_gdp'
]

target = 'gdp_growth_rate'


# Function definitions
def calculate_average_values(country_code, data, features):
    country_data = data[data['country_code'] == country_code]
    return country_data[features].mean().tolist()


def predict_for_country(country_code, data, features, target, average_values):
    country_data = data[data['country_code'] == country_code].copy()

    # Use average values for missing data in features
    for i, feature in enumerate(features):
        country_data[feature].fillna(average_values[i], inplace=True)

    # Preparing the data
    y = country_data[target].fillna(country_data[target].mean())
    years = country_data['year'].values.reshape(-1, 1)

    # Train the model
    model = LinearRegression()
    model.fit(years, y)

    # Predict for the next 10 years
    future_years = np.array([[year] for year in range(2023, 2033)])
    predictions = model.predict(future_years)

    return future_years.flatten(), predictions


def append_predictions(data, country_code, years, predictions):
    new_data = pd.DataFrame(
        {'year': years, 'gdp_growth_rate': predictions, 'country_code': country_code})
    return pd.concat([data, new_data], ignore_index=True)


gdp_growth_fig = go.Figure()
correlation_heatmap_fig = go.Figure()
gdp_in = go.Figure()
gdp_sg = go.Figure()
gdp_all = go.Figure()

# Adding traces to the GDP Growth Rate Trends plot
for country_code, country_data in data.groupby('country_code'):
    gdp_growth_fig.add_trace(
        go.Scatter(x=country_data['year'], y=country_data['gdp_growth_rate'],
                   mode='lines', name=country_code))

# Adding traces to the Correlation Heatmap
correlation_matrix = data.drop(['country_code', 'year'], axis=1).corr()
heatmap_trace = go.Heatmap(
    z=correlation_matrix,
    x=correlation_matrix.columns,
    y=correlation_matrix.columns,
    hoverongaps=False, colorscale='Viridis'
)
correlation_heatmap_fig.add_trace(heatmap_trace)

# Processing data
country_codes = ['IN', 'VN', 'ID', 'SG', 'KR', 'MY', 'CN']
for country_code in country_codes:
    average_values = calculate_average_values(country_code, data, training_features)
    years, preds = predict_for_country(country_code, data, training_features, target,
                                       average_values)
    data = append_predictions(data, country_code, years, preds)

# Adding traces for IN, VN, ID predictions
filtered_data = data[data['country_code'].isin(['IN', 'VN', 'ID'])]
for country_code, country_data in filtered_data.groupby('country_code'):
    sorted_data = country_data.sort_values(by='year')
    gdp_in.add_trace(go.Bar(x=sorted_data['year'], y=sorted_data['gdp_growth_rate'],
                            name=country_code))

# Adding the GDP Growth Rate Predictions plot for SG, KR, MY
filtered_data = data[data['country_code'].isin(['SG', 'KR', 'MY'])]
for country_code, country_data in filtered_data.groupby('country_code'):
    sorted_data = country_data.sort_values(by='year')
    gdp_sg.add_trace(
        go.Bar(x=sorted_data['year'], y=sorted_data['gdp_growth_rate'],
               name=country_code))

# Adding the GDP Growth Rate Predictions plot for all countries
filtered_data = data[
    data['country_code'].isin(['SG', 'KR', 'MY', 'ID', 'VN', 'IN', 'CN'])]
for country_code, country_data in filtered_data.groupby('country_code'):
    sorted_data = country_data.sort_values(by='year')
    gdp_all.add_trace(
        go.Bar(x=sorted_data['year'], y=sorted_data['gdp_growth_rate'],
               name=country_code)
    )

# Update layout (can be customized further as needed)
fig.update_layout(height=1200, showlegend=True)

st.title('Economic Indicators Analysis')

# Dropdown for graph selection
graph_selection = st.selectbox(
    'Select Graph:',
    ('All', 'GDP Growth Rate Trends', 'Correlation Heatmap',
     'GDP Growth Rate Predictions for IN, VN, ID',
     'GDP Growth Rate Predictions for SG, KR, MY', 'GDP Growth Rate Predictions')
    # add all graph names here
)
# Adding titles to each figure
gdp_growth_fig.update_layout(title='GDP Growth Rate Trends (1973-2022)')
correlation_heatmap_fig.update_layout(
    title='Correlation Heatmap of Economic Indicators')
gdp_in.update_layout(title='GDP Growth Rate Predictions for IN, VN, and ID (2023-2032)')
gdp_sg.update_layout(title='GDP Growth Rate Predictions for SG, KR, and MY (2023-2032)')
gdp_all.update_layout(title='GDP Growth Rate Predictions (2023-2032)')


def plot_graph(graph_name):
    if graph_name == 'All':
        st.plotly_chart(gdp_growth_fig)
        st.plotly_chart(correlation_heatmap_fig)
        st.plotly_chart(gdp_in)
        st.plotly_chart(gdp_sg)
        st.plotly_chart(gdp_all)
    elif graph_name == 'GDP Growth Rate Trends':
        st.plotly_chart(gdp_growth_fig)
    elif graph_name == 'Correlation Heatmap':
        st.plotly_chart(correlation_heatmap_fig)
    elif graph_name == 'GDP Growth Rate Predictions for IN, VN, ID':
        st.plotly_chart(gdp_in)
    elif graph_name == 'GDP Growth Rate Predictions for SG, KR, MY':
        st.plotly_chart(gdp_sg)
    elif graph_name == 'GDP Growth Rate Predictions':
        st.plotly_chart(gdp_all)


plot_graph(graph_selection)
