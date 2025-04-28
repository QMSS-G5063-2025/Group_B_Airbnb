import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
import os

st.set_page_config(page_title="Price Insights", page_icon="💲", layout="wide")

st.title("💲 Manhattan Airbnb Listing Price")
st.markdown("---")

# --- Build safe file path ---
CURRENT_DIR = os.path.dirname(__file__)  # this points to /pages/
DATA_PATH = os.path.join(CURRENT_DIR, "..", "data", "airbnb_cleaned.csv")

# --- Load data ---
df = pd.read_csv(DATA_PATH)
df2 = df.copy()
df2['price'] = df2['price'].replace('[\$,]', '', regex=True).astype(float)

# =========================
# Chart 1: Top Neighborhoods
# =========================

st.markdown("## Average Airbnb Price")

# --- Preprocessing: calculate average price ---
avg_price = df2.groupby(['neighbourhood', 'room_type'])['price'].mean().reset_index()

# --- Airbnb pink/red shades ---
airbnb_colors = ['#FFCDD2', '#E57373', '#F44336', '#D32F2F']

# --- Unique options ---
neighborhoods = sorted(avg_price['neighbourhood'].unique())
room_types = sorted(avg_price['room_type'].unique())

# Insert 'All' at the top
neighborhood_options = ['All'] + neighborhoods
room_type_options = ['All'] + room_types

# --- Sidebar selections ---

# Default selections
default_neighborhoods = ['Chelsea', 'Harlem', 'Hell\'s Kitchen', 'Lower East Side', 'Midtown']

selected_neighborhoods = st.multiselect(
    "Select Neighborhood(s):",
    neighborhood_options,
    default=[n for n in default_neighborhoods if n in neighborhoods]
)

selected_room_types = st.multiselect(
    "Select Room Type(s):",
    room_type_options,
    default=['All']
)

# --- Logic to handle 'All' selection ---

# If 'All' is selected for neighborhoods, ignore other selections and select all
if 'All' in selected_neighborhoods:
    filtered_neighborhoods = neighborhoods
else:
    filtered_neighborhoods = selected_neighborhoods

# If 'All' is selected for room types, ignore other selections and select all
if 'All' in selected_room_types:
    filtered_room_types = room_types
else:
    filtered_room_types = selected_room_types

# --- Filtered Data ---
filtered_data = avg_price[
    (avg_price['neighbourhood'].isin(filtered_neighborhoods)) &
    (avg_price['room_type'].isin(filtered_room_types))
]

# --- Warning if nothing selected ---
if not filtered_neighborhoods or not filtered_room_types:
    st.warning("⚠️ Please select at least one neighborhood and one room type to display the chart.")
elif filtered_data.empty:
    st.warning("⚠️ No matching data found with your selections.")
else:
    # --- Create figure ---
    fig = px.bar(
        filtered_data,
        x='neighbourhood',
        y='price',
        color='room_type',
        barmode='group',
        color_discrete_sequence=airbnb_colors,
        labels={'price': 'Average Price (USD)', 'neighbourhood': 'Neighborhood'}
    )

    fig.update_layout(
        template='plotly_white',
        width=1000,
        height=600,
        font=dict(color='black', family='Arial'),
        legend_title_text="Room Type",
        legend_title_font=dict(color='black', size=16),
        legend_font=dict(color='black', size=14),
        xaxis_tickangle=-30,
        margin=dict(b=150),
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================
# Chart 2: Price Distribution
# =========================

st.markdown("## Airbnb Price Distribution")

# Neighborhood filter
neighborhoods = sorted(df2['neighbourhood'].unique())
neighborhood_options = ['All'] + neighborhoods

selected_neighborhoods = st.multiselect(
    "Select Neighborhood(s):",
    neighborhood_options,
    default=['All'],
    key="neighborhood_multiselect"
)

# Room type filter
room_types = sorted(df2['room_type'].unique())
room_type_options = ['All'] + room_types

selected_room_types = st.multiselect(
    "Select Room Type(s):",
    room_type_options,
    default=['All'],
    key="room_type_multiselect"
)

# --- Apply filters ---

# Filter Neighborhood
if 'All' in selected_neighborhoods:
    filtered_df = df2.copy()
else:
    filtered_df = df2[df2['neighbourhood'].isin(selected_neighborhoods)]

# Filter Room Type
if 'All' not in selected_room_types:
    filtered_df = filtered_df[filtered_df['room_type'].isin(selected_room_types)]

# --- Price Range Slider ---
max_price = int(df2['price'].max())

price_range = st.slider(
    "Select Price Range:",
    min_value=0,
    max_value=max_price,
    value=(0, 800),
    step=10,
    format="$%d"
)

# Filter based on price range
filtered_df = filtered_df[(filtered_df['price'] >= price_range[0]) & (filtered_df['price'] <= price_range[1])]

# --- Warning if nothing matches ---
if filtered_df.empty:
    st.warning("⚠️ No listings found for the selected filters. Please adjust neighborhood, room type, or price range.")
else:
    # --- Plot ---
    fig = px.histogram(
        filtered_df,
        x='price',
        nbins=50,
        color_discrete_sequence=[airbnb_colors[2]],  # Darker pink for bars
        labels={'price': 'Listing Price (USD)'}
    )

    fig.update_layout(
        template='plotly_white',
        width=1000,
        height=600,
        title_text=None,
        font=dict(color='black', family='Arial'),
        xaxis_title="Price (USD)",
        yaxis_title="Number of Listings",
        xaxis_tickformat="$,.0f",
        margin=dict(b=150),
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================
# Chart 3: Box Plot of Price by Room Type
# =========================

st.markdown("## Airbnb Price Spread")

# --- Sidebar Filters ---

# Neighborhood filter
neighborhoods = sorted(df2['neighbourhood'].unique())
neighborhood_options = ['All'] + neighborhoods

# Default selection
default_neighborhoods = ['Chelsea', 'Harlem', 'Hell\'s Kitchen', 'Lower East Side', 'Midtown']

selected_neighborhoods = st.multiselect(
    "Select Neighborhood(s):",
    neighborhood_options,
    default=[n for n in default_neighborhoods if n in neighborhoods],
    key="neighborhood_box_multiselect"
)

# Room type filter
room_types = sorted(df2['room_type'].unique())
room_type_options = ['All'] + room_types

selected_room_types = st.multiselect(
    "Select Room Type(s):",
    room_type_options,
    default=['All'],
    key="roomtype_box_multiselect"
)

# --- Apply filters ---

# Filter Neighborhood
if 'All' in selected_neighborhoods:
    filtered_df = df2.copy()
else:
    filtered_df = df2[df2['neighbourhood'].isin(selected_neighborhoods)]

# Filter Room Type
if 'All' not in selected_room_types:
    filtered_df = filtered_df[filtered_df['room_type'].isin(selected_room_types)]

# --- Warning if nothing matches ---
if filtered_df.empty:
    st.warning("⚠️ No listings found for the selected filters. Please adjust neighborhood or room type.")
else:
    # --- Plot ---
    fig = px.box(
        filtered_df,
        x='neighbourhood',
        y='price',
        color='room_type',
        points='outliers',  # Show outlier points
        color_discrete_sequence=airbnb_colors,
        labels={'price': 'Listing Price (USD)', 'neighbourhood': 'Neighborhood'}
    )

    fig.update_layout(
        template='plotly_white',
        width=1000,
        height=600,
        title_text=None,
        font=dict(color='black', family='Arial'),
        xaxis_title="Neighborhood",
        yaxis_title="Price (USD)",
        xaxis_tickangle=-30,
        yaxis_tickformat="$,.0f",
        legend_title_text="Room Type",
        legend_title_font=dict(color='black', size=16),
        legend_font=dict(color='black', size=14),
        margin=dict(b=150),
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Footer ---
st.caption("© 2025 · Columbia University")