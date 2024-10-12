import streamlit as st
import mysql.connector
import pandas as pd
import datetime
import numpy as np

# MySQL Connection function
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",  
            user="root",
            password="Pnu@2024",
            database="redbus_data"
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Function to load data from MySQL
def load_data():
    conn = create_connection()
    if conn is None:
        return pd.DataFrame()  

    try:
        query = "SELECT * FROM redbus_details"
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows)  
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        df = pd.DataFrame()  
    finally:
        conn.close()

    return df

st.set_page_config(page_title="Redbus Data App", page_icon="🚌", layout="wide")

st.title("🚌 Redbus Data App")

# Load data from MySQL
df = load_data()

if df.empty:
    st.warning("No data available.")
else:
    # Create two columns with medium gaps
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        # Filter based on State
        st.subheader("State")
        states = ['Select State'] + list(df['State'].unique())
        selected_state = st.selectbox("", states, key="state")
        if selected_state != 'Select State':
            df = df[df['State'] == selected_state]

        # From City Filter
        st.subheader("From City")
        from_cities = ['Select City'] + list(df['From_City'].unique())
        selected_from_city = st.selectbox("", from_cities, key="from_city")
        if selected_from_city != 'Select City':
            df = df[df['From_City'] == selected_from_city]

        # Bus Type Filter
        st.subheader("Bus Type")
        bus_types = ['Select Type'] + list(df['Bus_type'].unique())
        selected_bus_type = st.selectbox("", bus_types, key="bus_type")
        if selected_bus_type != 'Select Type':
            df = df[df['Bus_type'] == selected_bus_type]

    with col2:
        # To City Filter
        st.subheader("To City")
        to_cities = ['Select City'] + list(df['To_City'].unique())
        selected_to_city = st.selectbox("", to_cities, key="to_city")
        if selected_to_city != 'Select City':
            df = df[df['To_City'] == selected_to_city]

        # Departing Time Filter
        st.subheader("Departing Time")
        departing_times = ['Select Time'] + list(df['Departure_time'].unique())
        selected_departing_time = st.selectbox("", departing_times, key="departing_time")
        if selected_departing_time != 'Select Time':
            df = df[df['Departure_time'] == selected_departing_time]

        # Star Rating Filter
        st.subheader("Ratings")
        min_star, max_star = 0.0, 5.0
        selected_star_range = st.slider("", min_star, max_star, (min_star, max_star), key="Ratings")
        df = df[(df['Ratings'] >= selected_star_range[0]) & (df['Ratings'] <= selected_star_range[1])]

    # Display the final filtered data with times
    st.subheader("Filtered Bus Data")
    st.write(df[['State', 'Route_name', 'From_City', 'To_City', 'Duration', 'Ratings', 'Fare']])

    # Download filtered data as CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_bus_data_with_times.csv",
        mime="text/csv",
        key="download_button"
    )
