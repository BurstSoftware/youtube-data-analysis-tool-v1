import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def load_data():
    """Load the CSV data into a pandas DataFrame."""
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    return None

def main():
    st.title("YouTube Video Data Analysis")
    
    # Load data
    df = load_data()
    
    if df is not None:
        # Sidebar for filtering
        st.sidebar.header("Filters")
        
        # Date range filter
        date_range = st.sidebar.date_input(
            "Select Date Range", 
            value=(df['Date'].min().date(), df['Date'].max().date())
        )
        
        # Content filter
        unique_contents = df['Content'].unique()
        selected_contents = st.sidebar.multiselect(
            "Select Video Contents", 
            unique_contents, 
            default=unique_contents
        )
        
        # Filtering the dataframe
        filtered_df = df[
            (df['Date'].dt.date >= date_range[0]) & 
            (df['Date'].dt.date <= date_range[1]) & 
            (df['Content'].isin(selected_contents))
        ]
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Videos", len(filtered_df))
        with col2:
            st.metric("Total Views", filtered_df['Views'].sum())
        with col3:
            st.metric("Avg Views per Video", filtered_df['Views'].mean().round(2))
        
        # Visualizations
        st.subheader("Views Over Time")
        views_by_date = filtered_df.groupby('Date')['Views'].sum().reset_index()
        fig = px.line(views_by_date, x='Date', y='Views', 
                      title='Cumulative Views by Date')
        st.plotly_chart(fig)
        
        # Detailed View
        st.subheader("Video Details")
        st.dataframe(filtered_df[['Date', 'Content', 'Video title', 'Duration', 'Views']])
        
        # Download filtered data
        st.download_button(
            label="Download Filtered Data",
            data=filtered_df.to_csv(index=False),
            file_name="filtered_youtube_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
