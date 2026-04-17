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

# Show a preview of the raw data
st.subheader("Raw Data Preview")
st.dataframe(df.head(20))