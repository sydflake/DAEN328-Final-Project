# STEP 1 -------------------------------------------------------------------------------------------------
import streamlit as st
st.title("Chicago Food Inspections Data Visualization with Streamlit") 
st.write("Welcome!")

from dotenv import load_dotenv
import os

load_dotenv()  # loads variables from .env into environment

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}


# STEP 2 -------------------------------------------------------------------------------------------------
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns


# Function to Connect to PostgreSQL
@st.cache_resource
def get_db_connection():
    """Establish a connection to the PostgreSQL database."""
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{DB_PARAMS['user']}:{DB_PARAMS['password']}@"
            f"{DB_PARAMS['host']}:{DB_PARAMS['port']}/{DB_PARAMS['dbname']}"
        )
        conn = engine.connect()
        return conn
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return None

conn = get_db_connection()

if conn:
    st.success("Successfully connected to PostgreSQL database!")
else:
    st.error("Failed to connect. Check your credentials.")

# STEP 3-------------------------------------------------------------------------------------------------
def fetch_data():
    """Fetch sample data from a PostgreSQL table and handle errors."""
    query = "SELECT * FROM inspections LIMIT 10;"  # Replace 'your_table' with actual table name
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

data = fetch_data()
if not data.empty:
    st.write("### Sample Data from PostgreSQL")
    st.dataframe(data)
else:
    st.warning("⚠ No data retrieved. Check your query or database connection.")

# STEP 4 -------------------------------------------------------------------------------------------------
# VISUALIZATIONS
# Pie Plots-------------------------------------------
