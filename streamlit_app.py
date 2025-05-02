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
import plotly.express as px

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

# STEP 3 -------------------------------------------------------------------------------------------------
def fetch_data():
    """Fetch sample data from a PostgreSQL table and handle errors."""
    query = "SELECT * FROM inspections;"
    try:
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

data = fetch_data()

# STEP 4 -------------------------------------------------------------------------------------------------
# Convert inspection_date to datetime
data['inspection_date'] = pd.to_datetime(data['inspection_date'], errors='coerce')

# SIDEBAR FILTERS -------------------------------------------------------------------------------------------------
st.sidebar.header("Filters")

# Risk filter
risk_options = sorted(data['risk'].dropna().unique())
selected_risks = st.sidebar.multiselect("Risk Level", options=risk_options, default=risk_options)

# Date range filter
min_date = data['inspection_date'].min()
max_date = data['inspection_date'].max()

date_range = st.sidebar.date_input(
    "Inspection Date Range", 
    value=(min_date, max_date), 
    min_value=min_date, 
    max_value=max_date
)

# Apply filters
filtered_data = data[
    data['risk'].isin(selected_risks) &
    (data['inspection_date'] >= pd.to_datetime(date_range[0])) &
    (data['inspection_date'] <= pd.to_datetime(date_range[1]))
]

st.write("### Sample of Filtered Data")
st.dataframe(filtered_data.head(10))

# VISUALIZATIONS -------------------------------------------------------------------------------------------------

# Pie Chart: Risk Level Distribution
st.subheader("Risk Level Distribution")
risk_counts = filtered_data['risk'].value_counts().reset_index()
risk_counts.columns = ['risk_level', 'count']

fig = px.pie(risk_counts, 
             names='risk_level', 
             values='count', 
             title="Risk Level Distribution",
             color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig)

# Time Series Plot: Violations Over Time
st.subheader("Violations Over Time")

# Preprocess violations
violations_list = filtered_data['violations'].apply(lambda x: x.strip('{}').split(',') if pd.notna(x) else [])
filtered_data['violation_count'] = filtered_data.groupby('inspection_date')['violations'].transform('count')
violations_per_day = filtered_data.groupby('inspection_date')['violation_count'].sum().reset_index()

fig_time_series = px.line(violations_per_day,
                          x='inspection_date',
                          y='violation_count',
                          title="Violations Over Time",
                          labels={'inspection_date': 'Date', 'violation_count': 'Number of Violations'})
st.plotly_chart(fig_time_series)

# Bar Chart: Results by Risk
st.subheader("Inspection Results by Risk Level")
results_by_risk = filtered_data.groupby(['risk', 'results']).size().reset_index(name='count')
fig_bar = px.bar(results_by_risk, x='risk', y='count', color='results',
                 title="Inspection Results by Risk Level",
                 barmode='group')
st.plotly_chart(fig_bar)

# Box Plot: Violations per Inspection by Risk
st.subheader("Violations per Inspection by Risk")
filtered_data['num_violations'] = filtered_data['violations'].apply(
    lambda x: len(x.strip('{}').split(',')) if pd.notna(x) else 0)

fig_box = px.box(filtered_data, x='risk', y='num_violations',
                 title='Violations per Inspection by Risk Level')
st.plotly_chart(fig_box)

# Bar Chart: Top 10 Facility Types + "Other"
st.subheader("Facility Type Distribution (Top 10 + Other)")

# Count facility types
facility_counts = filtered_data['facility_type'].value_counts()

# Separate top 10
top_10 = facility_counts.head(10)
other = facility_counts[10:].sum()

# Combine top 10 + "Other"
facility_summary = pd.concat([top_10, pd.Series({'Other': other})]).reset_index()
facility_summary.columns = ['facility_type', 'count']

# Plot bar chart
fig_facility_bar = px.bar(
    facility_summary,
    x='facility_type',
    y='count',
    title='Top 10 Facility Types (Others Grouped)',
    text='count',
    color='facility_type',
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_facility_bar.update_traces(textposition='outside')
fig_facility_bar.update_layout(xaxis_title='Facility Type', yaxis_title='Count', showlegend=False)

# Display in Streamlit
st.plotly_chart(fig_facility_bar)


# Bar Chart: Most Common Violation Codes
st.subheader("Top 10 Violation Codes")
violations_list = filtered_data['violations'].apply(lambda x: x.strip('{}').split(',') if pd.notna(x) else [])
flat_violations = [v.strip() for sublist in violations_list for v in sublist]
violation_freq = pd.Series(flat_violations).value_counts().reset_index()
violation_freq.columns = ['violation_code', 'count']

fig_violation_bar = px.bar(violation_freq.head(10), x='violation_code', y='count',
                           title='Top 20 Violation Codes',
                           color='count')
st.plotly_chart(fig_violation_bar)

import json

# Choropleth Map: Normalized Failure Rate by ZIP Code
st.subheader("Failure Rate by ZIP Code")

# --- Step 1: Count total inspections per ZIP ---
inspections_by_zip = filtered_data.groupby('zip').size().reset_index(name='total_inspections')
inspections_by_zip['zip'] = inspections_by_zip['zip'].astype(int).astype(str).str.zfill(5)

# --- Step 2: Count failed inspections per ZIP ---
failures = filtered_data[filtered_data['results'].str.lower() == 'fail']
failures_by_zip = failures.groupby('zip').size().reset_index(name='fail_count')
failures_by_zip['zip'] = failures_by_zip['zip'].astype(int).astype(str).str.zfill(5)

# --- Step 3: Merge and calculate failure rate ---
zip_stats = pd.merge(inspections_by_zip, failures_by_zip, on='zip', how='left').fillna(0)
zip_stats['failure_rate'] = zip_stats['fail_count'] / zip_stats['total_inspections']

# --- Step 4: Load GeoJSON ---
with open('./Zip_Codes.geojson') as f:
    zip_geojson = json.load(f)

# --- Step 5: Create the choropleth ---
fig_choropleth = px.choropleth(
    zip_stats,
    geojson=zip_geojson,
    locations='zip',
    featureidkey='properties.zip',
    color='failure_rate',
    color_continuous_scale='Reds',
    title='Normalized Failure Rate by ZIP Code',
    labels={'failure_rate': 'Failure Rate'},
    hover_data=['fail_count', 'total_inspections'],
    projection='mercator'
)

fig_choropleth.update_geos(fitbounds="locations", visible=False)
fig_choropleth.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})

# --- Step 6: Display in Streamlit ---
st.plotly_chart(fig_choropleth)



