# Import required libraries
import streamlit as st
import pandas as pd

# Set the page title and layout
st.set_page_config(page_title="Global ESG Sustainability Dashboard", layout="wide")

# Main title and description shown at the top of the dashboard
st.title("Global ESG Sustainability Dashboard")
st.markdown("Exploring country-level sustainability performance using World Bank ESG data.")

# Sidebar for filters (we will add dropdowns and sliders here later)
st.sidebar.header("Filters")

# Placeholder message while we build the dashboard
st.write("Dashboard loading...")