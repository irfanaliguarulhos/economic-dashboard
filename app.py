import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Initialize session state for theme
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'  # Set dark theme as default

# Load data
@st.cache_data
def load_data():
    try:
        data = pd.read_csv("data/final_economic_data.csv")
        # Ensure default countries exist in the data
        default_countries = ['Canada', 'China', 'Brazil'] if all(item in data['country'].unique() for item in ['Canada', 'China', 'Brazil']) else [data['country'].unique()[0]]
        return data, default_countries
    except FileNotFoundError:
        st.error("Data file not found. Please ensure the file 'final_economic_data.csv' is in the 'data' directory.")
        return pd.DataFrame(), []  # Return empty DataFrame and countries list in case of error

data, default_countries = load_data()

# Load images and icons
@st.cache_data
def load_images():
    try:
        icon = Image.open("data/icon.webp")
        return icon
    except FileNotFoundError:
        st.warning("Icon image not found. Please ensure the file is in the 'data' directory.")
        return None

icon = load_images()

# Header with theme toggle
col1, col2 = st.columns([5, 1])
with col1:
    st.title("🌍 Global Economic Indicators Dashboard")
    st.markdown("**This dashboard provides a comparative analysis of various economic, demographic, and social indicators across multiple countries from 1999 to 2025. 📊 Our dashboard features a user-friendly interface, allowing you to easily select countries and years to visualize data. Enjoy side-by-side comparative analysis of key indicators across countries. Dive into technical analysis with trend lines to visualize economic indicators over time, moving averages to analyze trends in inflation, GDP growth, and unemployment, and correlation analysis to explore relationships between indicators like inflation and unemployment. Lastly, export charts and data for further analysis and reporting. 🚀**")
with col2:
    if st.button(f'{"🌙" if st.session_state.theme == "light" else "☀️"} Theme'):
        st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'

# Apply theme
def apply_theme():
    if st.session_state.theme == 'dark':
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #121212;
                color: #ffffff;
            }
            .stSidebar .css-1d391kg {
                background-color: #121212;
                color: #ffffff;
            }
            .stSidebar .css-1d391kg .css-1d391kg {
                background-color: #121212;
                color: #ffffff;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #ffffff;
                color: #000000;
            }
            .stSidebar .css-1d391kg {
                background-color: #ffffff;
                color: #000000;
            }
            .stSidebar .css-1d391kg .css-1d391kg {
                background-color: #ffffff;
                color: #000000;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

apply_theme()

# Sidebar filters
st.sidebar.header("Controls Panel")
with st.sidebar:
    st.image(icon, use_container_width=True)
    st.markdown("**Dashboard Creator:** [Irfan Ali Khan👤📞](https://www.linkedin.com/in/irfan-ali-khan-93b52b159/)")

selected_countries = st.sidebar.multiselect(
    "Select Countries", data["country"].unique(), default=default_countries
)
selected_year = st.sidebar.slider("Select Year", 2000, 2023, 2023)

# Categorize indicators
economic_indicators = ["GDP Growth", "Inflation", "Unemployment", "Government Debt to GDP", "Current Account Balance", "Foreign Direct Investment", "Consumer Price Index"]
demographic_indicators = ["Population Growth", "Life Expectancy", "Poverty Rate", "Literacy Rate"]
social_indicators = ["Gini Coefficient", "Labor Force Participation"]

# Sidebar for selecting indicators
st.sidebar.header("Select Indicators")
selected_economic_indicators = st.sidebar.multiselect("Economic Indicators", economic_indicators, default=economic_indicators)
selected_demographic_indicators = st.sidebar.multiselect("Demographic Indicators", demographic_indicators, default=demographic_indicators)
selected_social_indicators = st.sidebar.multiselect("Social Indicators", social_indicators, default=social_indicators)

selected_indicators = selected_economic_indicators + selected_demographic_indicators + selected_social_indicators

# Filter data based on selections
filtered_data = data[(data["country"].isin(selected_countries)) & (data["Year"].between(2000, 2023))]

# Display filtered data
if not filtered_data.empty:
    st.write(filtered_data)
else:
    st.warning("No data available for the selected filters.")

# Function to format large numbers
def format_large_numbers(value):
    if abs(value) >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    elif abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    else:
        return f"{value:.2f}"

# Main Content: Visualizations
if not filtered_data.empty:
    st.header("Economic Indicators")
    st.markdown("**Economic indicators such as GDP Growth measure the economic performance and growth rate of a country over time. Inflation helps us understand the rate at which the general level of prices for goods and services is rising, while Unemployment analyzes the percentage of the labor force that is jobless and seeking employment. Government Debt to GDP evaluates the government's debt as a percentage of its Gross Domestic Product. The Current Account Balance observes the balance of exports and imports of goods, services, and transfer payments. Foreign Direct Investment tracks investments made by foreign entities in the domestic economy. Lastly, the Consumer Price Index monitors changes in the price level of a basket of consumer goods and services. 👥**")
    for indicator in selected_economic_indicators:
        st.subheader(f"{indicator} Analysis")
        
        # Line Chart
        fig = px.line(
            filtered_data,
            x="Year",
            y=indicator,
            color="country",
            title=f"{indicator} Trends Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Visual Cards in Row with 3 Columns
        st.subheader(f"{indicator} Performance")
        cols = st.columns(3)
        for i, country in enumerate(selected_countries):
            country_data = filtered_data[filtered_data["country"] == country]
            if not country_data.empty:
                latest_value = country_data[indicator].values[-1]
                previous_value = country_data[indicator].values[-2] if len(country_data[indicator].values) > 1 else latest_value
                delta = latest_value - previous_value
                delta_symbol = "🔺" if delta > 0 else "🔻"
                formatted_value = format_large_numbers(latest_value)
                formatted_delta = format_large_numbers(delta)
                cols[i % 3].metric(label=f"{country} - {indicator}", value=formatted_value, delta=f"{delta_symbol} {formatted_delta}")

    st.header("Demographic Indicators")
    st.markdown("**In terms of demographic indicators, Population Growth tracks the increase in the number of individuals in a population. Life Expectancy measures the average period that a person may expect to live. The Poverty Rate helps us understand the percentage of the population living below the poverty line, and the Literacy Rate gauges the percentage of people who can read and write. 🌱**")
    for indicator in selected_demographic_indicators:
        st.subheader(f"{indicator} Analysis")
        
        # Line Chart
        fig = px.line(
            filtered_data,
            x="Year",
            y=indicator,
            color="country",
            title=f"{indicator} Trends Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Visual Cards in Row with 3 Columns
        st.subheader(f"{indicator} Performance")
        cols = st.columns(3)
        for i, country in enumerate(selected_countries):
            country_data = filtered_data[filtered_data["country"] == country]
            if not country_data.empty:
                latest_value = country_data[indicator].values[-1]
                previous_value = country_data[indicator].values[-2] if len(country_data[indicator].values) > 1 else latest_value
                delta = latest_value - previous_value
                delta_symbol = "🔺" if delta > 0 else "🔻"
                formatted_value = format_large_numbers(latest_value)
                formatted_delta = format_large_numbers(delta)
                cols[i % 3].metric(label=f"{country} - {indicator}", value=formatted_value, delta=f"{delta_symbol} {formatted_delta}")

    st.header("Social Indicators")
    st.markdown("**Social indicators include the Gini Coefficient, which analyzes income inequality within a country, and Labor Force Participation, which monitors the percentage of the working-age population that is part of the labor force.**")
    for indicator in selected_social_indicators:
        st.subheader(f"{indicator} Analysis")
        
        # Line Chart
        fig = px.line(
            filtered_data,
            x="Year",
            y=indicator,
            color="country",
            title=f"{indicator} Trends Over Time"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Visual Cards in Row with 3 Columns
        st.subheader(f"{indicator} Performance")
        cols = st.columns(3)
        for i, country in enumerate(selected_countries):
            country_data = filtered_data[filtered_data["country"] == country]
            if not country_data.empty:
                latest_value = country_data[indicator].values[-1]
                previous_value = country_data[indicator].values[-2] if len(country_data[indicator].values) > 1 else latest_value
                delta = latest_value - previous_value
                delta_symbol = "🔺" if delta > 0 else "🔻"
                formatted_value = format_large_numbers(latest_value)
                formatted_delta = format_large_numbers(delta)
                cols[i % 3].metric(label=f"{country} - {indicator}", value=formatted_value, delta=f"{delta_symbol} {formatted_delta}")

    # Map Chart for GDP Growth
    st.header("Global GDP Growth")
    st.markdown("**This map shows the GDP growth rates across different countries.**")
    map_year = st.slider("Select Year Range for Map", 2000, 2023, (2000, 2023))
    map_data = data[(data["Year"] >= map_year[0]) & (data["Year"] <= map_year[1])]
    fig_map = px.choropleth(
        map_data,
        locations="country",
        locationmode="country names",
        color="GDP Growth",
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="GDP Growth Rate by Country"
    )
    fig_map.update_layout(
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            lakecolor='rgba(0,0,0,0)',
            landcolor='rgba(0,0,0,0)',
            subunitcolor='rgba(255,255,255,0.5)',
            showland=True,
            showlakes=True,
            showcountries=True,
            showocean=True,
            oceancolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_map, use_container_width=True)

else:
    st.warning("No data available for the selected filters.")

# Footer
st.markdown("---")
footer_col1, footer_col2 = st.columns(2)
with footer_col1:
    st.markdown("**Data Sources**: World Bank, IMF")
    st.markdown("**Last Updated**: 2023")
with footer_col2:
    st.markdown("Created by [Irfan Ali Khan](https://www.linkedin.com/in/irfan-ali-khan-93b52b159/)")
    st.markdown("📊 Data updated monthly | Version 1.0 |")