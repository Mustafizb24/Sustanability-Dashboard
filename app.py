# Import required libraries
import streamlit as st
import pandas as pd

# Set the page title and layout
st.set_page_config(page_title="Global ESG Sustainability Dashboard", layout="wide")

# Main title and description shown at the top of the dashboard
st.title("Global ESG Sustainability Dashboard")
st.markdown("Exploring country-level sustainability performance using World Bank ESG data.")

# Load and clean the ESG dataset
@st.cache_data
def load_data():
    # Read CSV skipping the first 4 metadata rows
    df = pd.read_csv("ESGCSV.csv", skiprows=4)
    
    # Keep only relevant columns and drop empty ones
    df = df.dropna(axis=1, how='all')

    # Get year columns (everything after the first 4 columns) and name them properly
    year_cols = list(range(1960, 1960 + len(df.columns) - 4))
    df.columns = ["Country Name", "Country Code", "Indicator Name", "Indicator Code"] + [str(y) for y in year_cols]
    
    # Rename first four columns clearly
    df.columns.values[0] = "Country Name"
    df.columns.values[1] = "Country Code"
    df.columns.values[2] = "Indicator Name"
    df.columns.values[3] = "Indicator Code"
    
    return df

# Call the function to load data
df = load_data()

# Sidebar for filters (we will add dropdowns and sliders here later)
st.sidebar.header("Filters")

# Get list of all unique indicators for the dropdown
indicators = df["Indicator Name"].unique().tolist()

# Dropdown to select an indicator (moved to sidebar)
selected_indicator = st.sidebar.selectbox("Select an Indicator", indicators)

# Metric cards showing key summary statistics at the top of the dashboard
st.subheader("Key Metrics (2020)")

# Filter data for the selected indicator in 2020
df_metric = df[df["Indicator Name"] == selected_indicator][["Country Name", "2020"]].dropna()

# Create three columns for the metric cards
col1, col2, col3 = st.columns(3)

col1.metric("Highest Country", 
            df_metric.loc[df_metric["2020"].idxmax(), "Country Name"],
            f'{df_metric["2020"].max():.2f}')

col2.metric("Lowest Country",
            df_metric.loc[df_metric["2020"].idxmin(), "Country Name"],
            f'{df_metric["2020"].min():.2f}')

col3.metric("Global Average",
            "All Countries",
            f'{df_metric["2020"].mean():.2f}')

# Show a preview of the raw data
st.subheader("Raw Data Preview")
st.dataframe(df.head(20))

# Import plotly for charts
import plotly.express as px

# Section: Top 10 countries by a selected indicator
st.subheader("Top 10 Countries by Indicator")

# Filter data for the selected indicator and get the most recent year
df_indicator = df[df["Indicator Name"] == selected_indicator]

# Use the most recent year column with actual data
recent_year = "2020"
df_filtered = df_indicator[["Country Name", recent_year]].dropna()
df_filtered = df_filtered.sort_values(recent_year, ascending=False).head(10)

# Plot the bar chart
fig = px.bar(df_filtered, x="Country Name", y=recent_year,
             title=f"Top 10 Countries: {selected_indicator} (2020)",
             labels={recent_year: "Value", "Country Name": "Country"})
st.plotly_chart(fig, use_container_width=True)

# Section: World map showing indicator by country
st.subheader("World Map View")

# Merge indicator data with country codes for mapping
df_map = df[df["Indicator Name"] == selected_indicator][["Country Name", "Country Code", "2020"]].dropna()

# Plot choropleth world map
fig3 = px.choropleth(df_map,
                     locations="Country Code",
                     color="2020",
                     hover_name="Country Name",
                     color_continuous_scale="Viridis",
                     title=f"{selected_indicator} by Country (2020)")
st.plotly_chart(fig3, use_container_width=True)


# Section: Trend over time for a selected country
st.subheader("Indicator Trend Over Time")

# Dropdown to select a country (moved to sidebar)
countries = df["Country Name"].unique().tolist()
selected_country = st.sidebar.selectbox("Select a Country", countries)

# Filter data for selected country and indicator
df_country = df[(df["Country Name"] == selected_country) & 
                (df["Indicator Name"] == selected_indicator)]

# Get year columns only (from 1960 onwards)
year_columns = [col for col in df.columns if col.isdigit()]

# Reshape data for plotting
df_trend = df_country[year_columns].T
df_trend.columns = ["Value"]
df_trend.index.name = "Year"
df_trend = df_trend.dropna()

# Plot line chart
fig2 = px.line(df_trend, x=df_trend.index, y="Value",
               title=f"{selected_indicator} in {selected_country} over time",
               labels={"x": "Year", "Value": "Value"})
st.plotly_chart(fig2, use_container_width=True)