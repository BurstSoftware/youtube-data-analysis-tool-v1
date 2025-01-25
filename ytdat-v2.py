import streamlit as st
import pandas as pd

# Function to load data
def load_data(file_path):
    data = pd.read_csv(file_path)
    return data

# Streamlit app
st.title("YouTube Video Analytics Tool")

st.sidebar.header("Filters")

# File uploader
data_file = st.file_uploader("Upload your CSV file", type=["csv"])
if data_file:
    data = load_data(data_file)
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Numeric filters
    st.sidebar.subheader("Numeric Filters")

    views_min, views_max = st.sidebar.slider(
        "Views Range",
        min_value=float(data["Views"].min(skipna=True)),
        max_value=float(data["Views"].max(skipna=True)),
        value=(float(data["Views"].min(skipna=True)), float(data["Views"].max(skipna=True)))
    )

    duration_min, duration_max = st.sidebar.slider(
        "Duration Range (seconds)",
        min_value=float(data["Duration"].min(skipna=True)),
        max_value=float(data["Duration"].max(skipna=True)),
        value=(float(data["Duration"].min(skipna=True)), float(data["Duration"].max(skipna=True)))
    )

    # Filtering data based on user input
    filtered_data = data[
        (data["Views"] >= views_min) &
        (data["Views"] <= views_max) &
        (data["Duration"] >= duration_min) &
        (data["Duration"] <= duration_max)
    ]

    # String filters
    st.sidebar.subheader("Text Filters")
    selected_titles = st.sidebar.multiselect(
        "Select Video Titles",
        options=data["Video title"].dropna().unique(),
        default=data["Video title"].dropna().unique()
    )

    filtered_data = filtered_data[filtered_data["Video title"].isin(selected_titles)]

    # Date filter
    st.sidebar.subheader("Date Filter")
    if "Video publish time" in data.columns:
        data["Video publish time"] = pd.to_datetime(data["Video publish time"], errors='coerce')
        min_date = data["Video publish time"].min()
        max_date = data["Video publish time"].max()

        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_data = filtered_data[
                (data["Video publish time"] >= pd.Timestamp(start_date)) &
                (data["Video publish time"] <= pd.Timestamp(end_date))
            ]

    # Display filtered data
    st.write("### Filtered Results")
    st.dataframe(filtered_data)

    # Download button
    st.download_button(
        label="Download Filtered Data",
        data=filtered_data.to_csv(index=False),
        file_name="filtered_data.csv",
        mime="text/csv"
    )
else:
    st.write("Please upload a CSV file to get started.")
