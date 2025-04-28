import streamlit as st
import os
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Map Exploration", page_icon="🗺️", layout="wide")

st.title("🗺️ Manhattan Airbnb Map")
st.markdown("---")

# Load and clean data
# --- Build safe file path ---
CURRENT_DIR = os.path.dirname(__file__)  # this points to /pages/
DATA_PATH = os.path.join(CURRENT_DIR, "..", "data", "airbnb_cleaned.csv")

# --- Load data ---
df = pd.read_csv(DATA_PATH)
df1 = df.copy()
df1['price'] = df1['price'].replace('[\$,]', '', regex=True).astype(float)
df1['rating'] = df1['review_scores_rating'] if 'review_scores_rating' in df1.columns else None
df1 = df1.dropna(subset=['latitude', 'longitude', 'price', 'room_type', 'neighbourhood', 'rating'])

# Rename and deduplicate
df1 = df1.rename(columns={"room_type": "Room Type"})
if 'listing_id' in df1.columns and 'review_date' in df1.columns:
    df1 = df1.sort_values('review_date').drop_duplicates('listing_id', keep='last')


# Sidebar filters
st.sidebar.header("Filters")

neighborhoods = st.sidebar.multiselect(
    "Neighborhood:",
    options=sorted(df1['neighbourhood'].unique()),
    default=[]
)

room_types = st.sidebar.multiselect(
    "Room Type:",
    options=sorted(df1['Room Type'].unique()),
    default=[]
)

price_range = st.sidebar.slider(
    "Price Range:",
    0, int(df1['price'].clip(upper=1000).max()),
    value=(330, 500),
    step=10
)

rating_range = st.sidebar.slider(
    "Rating (1–5):",
    0.0, 5.0,
    value=(4.0, 5.0),
    step=0.1
)

# Filter Data
dff = df1.copy()

if neighborhoods:
    dff = dff[dff['neighbourhood'].isin(neighborhoods)]
if room_types:
    dff = dff[dff['Room Type'].isin(room_types)]
dff = dff[(dff['price'] >= price_range[0]) & (dff['price'] <= price_range[1])]
dff = dff[(dff['rating'] >= rating_range[0]) & (dff['rating'] <= rating_range[1])]

# Drop duplicates again if needed
if 'listing_id' in dff.columns and 'review_date' in dff.columns:
    dff = dff.sort_values('review_date').drop_duplicates('listing_id', keep='last')

# Assign different colors based on Room Type
room_type_colors = {
    "Entire home/apt": [255, 0, 0, 160],   
    "Private room": [135, 206, 250, 160],       
    "Shared room": [0, 255, 0, 160],        
    "Hotel room": [255, 165, 0, 160]        
}
dff["color"] = dff["Room Type"].map(lambda x: room_type_colors.get(x, [128, 128, 128, 160]))

# Map
st.markdown("## Explore the Map")

if dff.empty:
    st.warning("⚠️ No listings match your filters.")
else:
    st.markdown(f"#### ✅ {len(dff)} listings match your selection")

    # Color Legend
    st.markdown("###### Room Type Color Legend")
    st.markdown(
        """
        <div style='display: flex; gap: 20px;'>
            <div style='display: flex; align-items: center;'>
                <div style='width: 15px; height: 15px; background-color: red; margin-right: 5px;'></div> Entire home/apt
            </div>
            <div style='display: flex; align-items: center;'>
                <div style='width: 15px; height: 15px; background-color: #87CEFA; margin-right: 5px;'></div> Private room
            </div>
            <div style='display: flex; align-items: center;'>
                <div style='width: 15px; height: 15px; background-color: green; margin-right: 5px;'></div> Shared room
            </div>
            <div style='display: flex; align-items: center;'>
                <div style='width: 15px; height: 15px; background-color: orange; margin-right: 5px;'></div> Hotel room
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=dff,
        get_position='[longitude, latitude]',
        get_fill_color='color',
        get_radius=80,
        pickable=True,
    )

    view_state = pdk.ViewState(
        latitude=dff['latitude'].mean(),
        longitude=dff['longitude'].mean(),
        zoom=11.5,
        pitch=0,
    )

    tooltip = {
        "html": "<b>{listing_name}</b><br/>🏘️ {neighbourhood}<br/>💲{price} USD<br/>⭐ Rating: {rating}<br/>🏠 {Room Type}",
        "style": {
            "backgroundColor": "white",
            "color": "black",
            "fontSize": "12px"
        }
    }

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/light-v9"
    )

    st.pydeck_chart(deck)

st.markdown("---")

# Section: Explore Raw Data
st.markdown("## 🗂️ Explore Raw Data")

st.dataframe(
    dff[['listing_name', 'neighbourhood', 'Room Type', 'price', 'rating', 'latitude', 'longitude']],
    use_container_width=True
)

st.markdown("---")

# --- Footer ---
st.caption("© 2025 · Columbia University")