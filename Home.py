import streamlit as st
import os

# --- Page Config ---
st.set_page_config(page_title="AirbnbManhattan", page_icon="🏡", layout="wide")

# --- Hero Banner Image  ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(CURRENT_DIR, "images", "banner_airbnb.png")
st.image(IMAGE_PATH, use_container_width=True)

# --- Title Section ---
st.markdown("""
# Airbnb Listings in Manhattan
#### Affordable · Cozy · Unique Experiences
""")

st.markdown("---")

# --- Project Description ---

st.markdown("""
As one of the **most iconic and vibrant destinations in the world**, Manhattan draws millions of visitors each year with its rich culture, diverse neighborhoods, and endless attractions. In 2024, New York City welcomed over **64 million** visitors, marking a significant milestone in its post-pandemic tourism recovery. Moreover, NYC has been ranked as the **#1 trending city to visit in 2025** by global hospitality group Accor , and it secured the **#1 U.S. destinations** in Tripadvisor's 2025 Travelers' Choice Awards.​

Amid this bustling landscape, **Airbnb** has become a **key player** in shaping how people experience the city. This project is a deep dive into the dynamic world of **Airbnb listings across Manhattan, New York City**. Born from the collective efforts of our members, this project harnesses data visualization and text analysis to uncover patterns behind **price, location, and guest experiences**.
""")

# --- Journey Section with Buttons ---
st.markdown("Our discovery journey unfolds across **four vibrant chapters**:")

rows = [
    ("📄 **About the Project**", "pages/About_the_Project.py", "Project background, data sources, and research goals."),
    ("🗺️ **Map Exploration**", "pages/Map_Exploration.py", "An interactive map of Airbnb listings across neighborhoods."),
    ("💲 **Price Insights**", "pages/Price_Insights.py", "Active dives into pricing trends, distribution, and spreads."),
    ("📝 **Review Narratives**", "pages/Review_Narratives.py", "Sentiment and topic analysis of guest reviews.")
]

for label, page, description in rows:
    button_col, desc_col = st.columns([1, 3])
    with button_col:
        if st.button(label, key=label):
            st.switch_page(page)
    with desc_col:
        st.markdown(description)
    st.markdown("<br>", unsafe_allow_html=True)  # add spacing between rows

st.markdown("""
Join us as we map, decode, and visualize the Airbnb tapestry of the Big Apple — 
where every listing tells a story.
""")

st.markdown("---")

# --- Team Info (Researchers Section) ---
st.markdown("""
#### 👩🏻‍💻 Meet the Team
Group B · QMSS · Columbia University  
- **Weixuan Shao** [@weixuanshao](https://github.com/weixuanshao)
- **Yue Xi** [@linxi75](https://github.com/linxi75)
- **Xinyuan Xu** [@Carolxu2473](https://github.com/Carolxu2473)
- **Jiawen Zou** [@zjiawenz](https://github.com/zjiawenz)
""")

st.markdown("---")

# --- Footer ---
st.caption("© 2025 · Columbia University")
