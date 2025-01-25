import streamlit as st
import pandas as pd

# Function to load data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    return data

# Streamlit app
st.title("Date and Views Filtering Tool")

st.sidebar.header("Filters")

# File uploader
data_file = st.file_uploader("Upload your CSV file", type=["csv"])
if data_file:
    data = load_data(data_file)
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Date filter
    st.sidebar.subheader("Date Range Filter")
    min_date = data["Date"].min()
    max_date = data["Date"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_data = data[
            (data["Date"] >= pd.Timestamp(start_date)) &
            (data["Date"] <= pd.Timestamp(end_date))
        ]
    else:
        filtered_data = data

    # Numeric filter for Views
    st.sidebar.subheader("Views Range Filter")

    views_min, views_max = st.sidebar.slider(
        "Views Range",
        min_value=int(data["Views"].min()),
        max_value=int(data["Views"].max()),
        value=(int(data["Views"].min()), int(data["Views"].max()))
    )

    filtered_data = filtered_data[
        (filtered_data["Views"] >= views_min) &
        (filtered_data["Views"] <= views_max)
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
