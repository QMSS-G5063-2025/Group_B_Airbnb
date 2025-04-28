
# 🗽 Manhattan Airbnb Project

## Project Overview

Manhattan Airbnb Explorer is the a project of Group B at Columbia University’s GSAS (QMSS Program), developed as the final showcase for G5063 Data Visualization under the mentorship of Professor Thomas Brambor.

This project offers a data-driven exploration of Airbnb listings across Manhattan, using visualization and text analysisto reveal patterns in pricing, location, and guest feedback.

[Launch the project](https://airbnb-homepy.streamlit.app/)

---

## Project Objectives
- 🏙️ **Visualize** the geographic distribution of Airbnb listings across Manhattan neighborhoods.
- 📊 **Analyze** how factors like location, room type, and amenities influence listing prices.
- 📝 **Explore** guest reviews through simple text analysis to capture key themes of guest experiences.
- 💬 **Present** interactive visuals that allow users to filter, explore, and draw their own insights.

---

## Technologies Used
Streamlit for interactive web app development.
Pandas for data preprocessing and merging.
Plotly Express & Graph Objects for rich, customizable visualizations.
PyDeck for geospatial plotting.
NLTK for text processing and basic natural language analysis.
Custom UI Design for user-friendly dashboard creation.

---

## Project Layout

Group_B_Airbnb/
├── data/                         # Cleaned datasets for analysis
│   ├── airbnb_cleaned.csv        # Core cleaned Airbnb listing + review dataset
│   ├── airbnb_nlp_processed.csv  # Dataset after NLP text preprocessing (sentiment, topics, phrases)
│   └── README.md                 # Explains data preparation, filtering criteria, and field descriptions
│
├── images/                       # Project assets and process documentation
│   ├── banner_airbnb.png         # Airbnb banner picture
│   ├── process_book_1.png        # Initial process book sketch (brainstorming visualizations)
│   └── process_book_2.jpg        # Final website layout and widget planning
│
├── pages/                        # Streamlit app pages (multi-page structure)
│   ├── About_the_Project.py      # Project introduction, data source, and process book
│   ├── Map_Exploration.py        # Geographical mapping of listings
│   ├── Price_Insights.py         # Price analysis visualizations
│   ├── Review_Narratives.py      # Text analysis visualizations
│
├── Home.py                       # Main landing page (Streamlit homepage)
├── requirements.txt              # Python package requirements
├── README.md                     # Project overview, app usage guide, features, and team information
└── .DS_Store                     # (System file, can be ignored or deleted)


---

## How to Run Locally

1. Clone the repository:
    ```bash
    git clone https://github.com/QMSS-G5063-2025/Group_B_Airbnb
    cd your-repo-name
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Launch the Streamlit app:
    ```bash
    streamlit run app.py
    ```

---

## Team Members 
This project is a collaborative effort by 
Weixuan Shao
Yue Xi 
Xinyuan Xu 
Jiawen Zou

---

## License
This project is for educational purposes only.

---
