import streamlit as st
import os
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="About the Project", page_icon="📄", layout="wide")

st.title("📄 About This Project: Manhattan Airbnb Listings Explorer")
st.markdown("---")

# --- Project Overview ---
st.markdown("""
## Project Overview
This project explores the landscape of Airbnb listings and guest experiences in **Manhattan, New York City**.
By leveraging detailed listing and review data, we aim to uncover patterns in pricing, neighborhood characteristics, room types, and guest sentiments.
The goal is to create an interactive, visual experience that allows users to intuitively understand Airbnb dynamics across Manhattan.
""")

st.markdown("---")

# --- Data Source ---
st.markdown("""
## Data Source
The data used in this project comes from the **Inside Airbnb** initiative —
a mission-driven platform that collects and analyzes publicly available information from Airbnb to provide insights into the platform's impact on residential communities.

🔗 [Learn more about Inside Airbnb](http://insideairbnb.com/)

### 📁 Dataset Preparation
We merged and filtered three original datasets:
- **listings.csv** — Detailed information about available listings.
- **reviews.csv** — User-generated reviews associated with each listing.
- **reviews.csv.gz** - Detailed review data for the listings.

The final dataset includes:
- Listings located in **Manhattan**.
- Reviews written in **English**.
- Reviews dated **after January 1, 2023**.
- Entries with **no missing values**.

👉 See full details in our [Data Dictionary](https://github.com/QMSS-G5063-2025/Group_B_Airbnb/tree/main/data#-data-dictionary).

### ✨ NLP Preprocessing for Review Analysis
To further prepare the review texts for text mining and visualization, we applied a series of **Natural Language Processing (NLP)** steps using **NLTK** and **TextBlob**, including:

- Tokenization
- Stopword Removal
- Adjective–Noun Phrase Extraction
- Sentiment Analysis
- Topic Modeling (LDA)

👉 The NLP preprocessed dataset can be viewed [here](https://github.com/QMSS-G5063-2025/Group_B_Airbnb/blob/main/data/airbnb_nlp_processes.csv).
""")

st.markdown("---")

# --- What We Did ---
st.markdown("""
## What We Did

We built a series of **interactive visualizations** across three major dimensions:

### 1. 🗺️ Map Exploration
- Mapped the geographical distribution of Airbnb listings across Manhattan neighborhoods.
- Visualized concentration and density by room types.

### 2. 💲 Price Analysis
- Investigated price distributions, average prices across neighborhoods and room types.
- Built interactive bar plots, histograms, and box plots.
- Added dynamic filters (price range sliders, room type and neighborhood selectors).

### 3. 📝 Review Sentiment and Topic Exploration
- Preprocessed guest reviews using NLP techniques with NLTK and TextBlob, including tokenization, stopword removal.
- Conducted LDA topic modeling to discover hidden themes within reviews.
- Extracted adjective–noun phrases for word clouds.
- Applied sentiment analysis on specific aspects and overall sentiment.
- Visualized results with radar charts, word cloud, scatter plots, heatmaps.
""")

st.markdown("---")

# --- Techniques Used ---
st.markdown("""
## Techniques Used

- **Streamlit** for interactive web app development.
- **Pandas** for data preprocessing and merging.
- **Plotly Express & Graph Objects** for rich, customizable visualizations.
- **PyDeck** for geospatial plotting.
- **NLTK** for text processing and basic natural language analysis.
- **Custom UI Design** for user-friendly dashboard creation.
""")

st.markdown("---")

# --- Process Book ---
st.markdown("""
## Process Book

Below is a snapshot from our Process Book, documenting the stages of our project development:

---

### ✏️ First Stage: Brainstorming Graphs from Airbnb Data

At the beginning of the project, we focused on outlining the types of graphs and analyses we could create based on the available Airbnb dataset.  
We mapped out visualizations including location maps, price distributions, review sentiment analysis, and correlation heatmaps to explore different aspects of Airbnb listings in Manhattan.

""")
# --- Safe path construction ---
CURRENT_DIR = os.path.dirname(__file__)
IMAGE_PATH_1 = os.path.join(CURRENT_DIR, "..", "images", "process_book_1.png")

# --- Display the image ---
st.image(IMAGE_PATH_1, use_container_width=True)

st.markdown("""
---

### ✏️ Second Stage: Designing Streamlit Website Layout and Interactivity

As we progressed, we moved into planning the layout for our Streamlit website.  
In this phase, we refined the project structure into sections (Home, Map, Statistics, Text Analysis) and detailed the interactive widgets, such as neighborhood filters, price sliders, room type selectors, and topic-specific dropdowns, to make the user experience dynamic and engaging.

""")
# --- Safe path construction ---
CURRENT_DIR = os.path.dirname(__file__)
IMAGE_PATH_2 = os.path.join(CURRENT_DIR, "..", "images", "process_book_2.jpg")

# --- Display the image ---
st.image(IMAGE_PATH_2, use_container_width=True)

st.markdown("---")

# --- Final Note ---
st.markdown("""
## Final Note
Through this project, we provide an accessible, insightful, and engaging way to explore Manhattan’s vibrant Airbnb landscape, empowering users with a deeper understanding of listing behaviors, pricing strategies, and guest experiences. 🏁 
""")

st.markdown("---")

# --- Footer ---
st.caption("© 2025 · Columbia University")
