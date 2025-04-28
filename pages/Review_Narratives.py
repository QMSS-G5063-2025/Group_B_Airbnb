import streamlit as st
import os
import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from collections import Counter


st.set_page_config(page_title="Review Narratives", page_icon="📝", layout="wide")

# --- Title ---
st.title("📝 Manhattan Airbnb Review Analysis")
st.markdown("---")

# --- Load the processed data ---
CURRENT_DIR = os.path.dirname(__file__)  # this points to /pages/
DATA_PATH = os.path.join(CURRENT_DIR, "..", "data", "airbnb_nlp_processes.csv")
df = pd.read_csv(DATA_PATH)

# --- Clean 'price' ---
if not np.issubdtype(df['price'].dtype, np.number):
    df['price'] = (
        df['price']
        .astype(str)
        .str.replace(r'[\$,]', '', regex=True)
        .astype(float)
    )

# --- LDA Radar Chart ---

# --- LDA Radar Chart ---
st.markdown("## Review Topic Distribution")

# --- Neighborhood filter with "All" option ---
neighborhoods = sorted(df['neighbourhood'].dropna().unique())
neighborhood_options = ['All'] + neighborhoods

selected_neighborhoods = st.multiselect(
    "Select Neighborhood(s):",
    options=neighborhood_options,
    default=['All']
)

# --- Price Range Slider ---
min_price = int(df['price'].min())
max_price = int(df['price'].max())

selected_price_range = st.slider(
    "Select Price Range:",
    min_value=min_price,
    max_value=max_price,
    value=(0, max_price),
    step=10,
    format="$%d"
)

# --- Apply Filters ---
if 'All' in selected_neighborhoods:
    filtered_df = df[
        (df['price'] >= selected_price_range[0]) &
        (df['price'] <= selected_price_range[1])
    ]
else:
    filtered_df = df[
        (df['neighbourhood'].isin(selected_neighborhoods)) &
        (df['price'] >= selected_price_range[0]) &
        (df['price'] <= selected_price_range[1])
    ]

# --- Proceed if filtered data is not empty ---
if filtered_df.empty:
    st.warning("⚠️ No listings found for the selected filters.")
else:
    # --- LDA Topic Modeling ---

    sample_df = filtered_df.sample(min(3000, len(filtered_df)), random_state=42)

    vectorizer = CountVectorizer(max_df=0.9, min_df=10, max_features=3000, stop_words="english")
    dtm = vectorizer.fit_transform(sample_df['joined_tokens'].fillna(""))

    lda_topics = 5
    lda = LatentDirichletAllocation(n_components=lda_topics, random_state=42)
    lda.fit(dtm)
    sample_df["topic"] = lda.transform(dtm).argmax(axis=1)

    default_labels = [
        "Transportation", "Service", "Host/Location", "Amenities", "Cleanliness",
        "Pricing", "Check‑in", "Food", "Noise"
    ]
    labels = default_labels[:lda_topics]

    radar_df = (
        sample_df["topic"].value_counts().sort_index()
        .reindex(range(lda_topics), fill_value=0)
        .rename("Mentions")
        .to_frame()
        .assign(Topic=labels)
    )

    # --- Plot Radar Chart in Airbnb Red ---
    fig_radar = px.line_polar(
        radar_df,
        r="Mentions",
        theta="Topic",
        line_close=True,
        width=600,
        height=600
    )

    fig_radar.update_traces(
        fill="toself",
        line_color="#FF5A5F"
    )

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showticklabels=False,
                ticks='',
                gridcolor="lightgray",
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color="black")
            )
        ),
        template="plotly_white",
        font=dict(color='black', family='Arial')
    )

    st.plotly_chart(fig_radar, use_container_width=True)

st.markdown("---")

# --- Word Cloud ---
st.markdown("## Review Phrase Word‑Cloud")

# --- Neighborhood Filter with "All" option ---
neighborhoods = sorted(df['neighbourhood'].dropna().unique())
neighborhood_options = ['All'] + neighborhoods

selected_neighborhoods_wc = st.multiselect(
    "Select Neighborhood(s) for Word Cloud:",
    options=neighborhood_options,
    default=['All'],
    key="wc_neighborhood_multiselect"
)

# --- Price Range Filter ---
min_price = int(df['price'].min())
max_price = int(df['price'].max())

selected_price_range_wc = st.slider(
    "Select Price Range for Word Cloud:",
    min_value=min_price,
    max_value=max_price,
    value=(0, max_price),
    step=10,
    format="$%d",
    key="wc_price_slider"
)

# --- Apply Filters ---
filtered_df_wc = df.copy()

if 'All' not in selected_neighborhoods_wc:
    filtered_df_wc = filtered_df_wc[filtered_df_wc['neighbourhood'].isin(selected_neighborhoods_wc)]


filtered_df_wc = filtered_df_wc[
    (filtered_df_wc['price'] >= selected_price_range_wc[0]) &
    (filtered_df_wc['price'] <= selected_price_range_wc[1])
]

# --- Generate Word Cloud ---
phrases = Counter(
    p for plist in filtered_df_wc['adj_noun_phrases'].dropna()
    for p in eval(plist)  # careful: convert string list back to list
)

if phrases:
    wc = WordCloud(width=800, height=400, background_color="white", colormap="Reds").generate_from_frequencies(phrases)
    fig_wc, ax_wc = plt.subplots(figsize=(12, 6))
    ax_wc.imshow(wc, interpolation="bilinear")
    ax_wc.axis("off")
    st.pyplot(fig_wc)
else:
    st.warning("⚠️ Word‑cloud skipped – no adjective–noun phrases found in filtered sample.")

st.markdown("---")

# --- Sentiment vs Rating Scatter Plots ---

st.markdown("## Sentiment vs Rating by Topic")

# --- Neighborhood filter with "All" option ---
neighborhoods = sorted(df['neighbourhood'].dropna().unique())
neighborhood_options = ['All'] + neighborhoods

selected_neighborhoods_scatter = st.multiselect(
    "Select Neighborhood(s) for Scatter Plot:",
    options=neighborhood_options,
    default=['All'],
    key="scatter_neighborhood_multiselect"
)

# --- Price Range Slider ---
min_price = int(df['price'].min())
max_price = int(df['price'].max())

selected_price_range_scatter = st.slider(
    "Select Price Range for Scatter Plot:",
    min_value=min_price,
    max_value=max_price,
    value=(0, max_price),
    step=10,
    format="$%d",
    key="scatter_price_slider"
)

# --- Apply Filters ---
if 'All' in selected_neighborhoods_scatter:
    filtered_df_scatter = df[
        (df['price'] >= selected_price_range_scatter[0]) &
        (df['price'] <= selected_price_range_scatter[1])
    ]
else:
    filtered_df_scatter = df[
        (df['neighbourhood'].isin(selected_neighborhoods_scatter)) &
        (df['price'] >= selected_price_range_scatter[0]) &
        (df['price'] <= selected_price_range_scatter[1])
    ]

# --- Build Scatter Plots ---
categories = ["cleanliness", "price", "location"]
sent_cols = [f"sentiment_{k}" for k in categories]

df_sent = filtered_df_scatter.dropna(subset=sent_cols + ["review_scores_rating"])

if not df_sent.empty:
    fig_scatter, axes = plt.subplots(1, 3, figsize=(18, 5))

    for i, (col, title) in enumerate(zip(sent_cols, [k.capitalize() for k in categories])):
        ax = axes[i]
        sns.regplot(
            data=df_sent,
            x="review_scores_rating",
            y=col,
            scatter_kws={'alpha':0.3, 'color':'#FF5A5F'},
            line_kws={'color':'firebrick'},
            ax=ax
        )
        ax.set_title(title)
        ax.set_xlabel("Review Rating (1‑5)")
        ax.set_ylabel("Sentiment Polarity")
        ax.grid(True, linestyle="--", alpha=0.6)

    st.pyplot(fig_scatter)

else:
    st.warning("⚠️ Insufficient data for sentiment scatter plots after applying filters.")

st.markdown("---")

# --- Price Bin Heatmaps ---

st.markdown("## Price‑Tier Heatmaps")

# --- Price: Ensure Numeric ---
if not np.issubdtype(df["price"].dtype, np.number):
    df["price"] = df["price"].astype(str).str.replace(r"[\$,]", "", regex=True).astype(float)

# --- Neighborhood Filter ---
neighborhoods = sorted(df['neighbourhood'].dropna().unique())
neighborhood_options = ['All'] + neighborhoods

selected_neighborhoods_ht = st.multiselect(
    "Select Neighborhood(s) for Price-Tier Heatmap: (Tier 1 - Lowest Price Bin)",
    options=neighborhood_options,
    default=['All'],
    key="heatmap_neighborhood_multiselect"
)

# --- Price Bin Size Slider ---
bin_options = {
    "Tertile (3 bins)": 3,
    "Quartile (4 bins)": 4,
    "Quintile (5 bins)": 5,
    "Decile (10 bins)": 10
}
bin_choice = st.select_slider(
    "Select Number of Price Tiers:",
    options=list(bin_options.keys()),
    value="Quartile (4 bins)"
)
selected_bins = bin_options[bin_choice]

# --- Apply Neighborhood Filter ---
filtered_df_ht = df.copy()

if 'All' not in selected_neighborhoods_ht:
    filtered_df_ht = filtered_df_ht[filtered_df_ht['neighbourhood'].isin(selected_neighborhoods_ht)]

# --- Generate Price Bins ---
bin_labels = [f"Tier {i+1}" for i in range(selected_bins)]
filtered_df_ht["price_bin"] = pd.qcut(filtered_df_ht["price"], q=selected_bins, labels=bin_labels)

# --- Calculate Metrics ---
avg_score = filtered_df_ht.groupby("price_bin")["review_scores_rating"].mean().reindex(bin_labels)
sent_by_price = filtered_df_ht.groupby("price_bin")["sentiment_compound"].mean().reindex(bin_labels)

# --- Color Settings ---
airbnb_colors = ["#FFCDD2", "#EF9A9A", "#E57373", "#EF5350", "#F44336", "#E53935", "#D32F2F", "#C62828", "#B71C1C"]

col1, col2 = st.columns(2)

# --- Plot Average Rating ---
with col1:
    fig_h1, ax_h1 = plt.subplots(figsize=(4, 5))
    cmap1 = plt.cm.colors.LinearSegmentedColormap.from_list("AirbnbRed", airbnb_colors)
    im1 = ax_h1.imshow(avg_score.values.reshape(-1, 1), cmap=cmap1, aspect="auto", origin="lower", vmin=4.6, vmax=5.0)
    for i, val in enumerate(avg_score):
        ax_h1.text(0, i, f"{val:.2f}", ha="center", va="center", color="black")
    ax_h1.set_yticks(range(selected_bins)); ax_h1.set_yticklabels(bin_labels)
    ax_h1.set_xticks([]); ax_h1.set_title("Average Rating")
    plt.colorbar(im1, ax=ax_h1, shrink=0.8)
    st.pyplot(fig_h1)

# --- Plot Average Sentiment ---
with col2:
    fig_h2, ax_h2 = plt.subplots(figsize=(4, 5))
    cmap2 = plt.cm.colors.LinearSegmentedColormap.from_list("AirbnbRed", airbnb_colors)
    im2 = ax_h2.imshow(sent_by_price.values.reshape(-1, 1), cmap=cmap2, aspect="auto", origin="lower", vmin=0.65, vmax=0.85)
    for i, val in enumerate(sent_by_price):
        ax_h2.text(0, i, f"{val:.2f}", ha="center", va="center", color="black")
    ax_h2.set_yticks(range(selected_bins)); ax_h2.set_yticklabels(bin_labels)
    ax_h2.set_xticks([]); ax_h2.set_title("Average Sentiment")
    plt.colorbar(im2, ax=ax_h2, shrink=0.8)
    st.pyplot(fig_h2)

st.markdown("---")

# --- Correlation Heatmap of Review Scores ---
st.markdown("## Correlation of Review Sub‑Scores")

# --- Neighborhood Filter ---
neighborhoods = sorted(df['neighbourhood'].dropna().unique())
neighborhood_options = ['All'] + neighborhoods

selected_neighborhoods_corr = st.multiselect(
    "Select Neighborhood(s) for Correlation Analysis:",
    options=neighborhood_options,
    default=['All'],
    key="corr_neighborhood_multiselect"
)

# --- Apply Neighborhood Filter ---
filtered_df_corr = df.copy()

if 'All' not in selected_neighborhoods_corr:
    filtered_df_corr = filtered_df_corr[filtered_df_corr['neighbourhood'].isin(selected_neighborhoods_corr)]

# --- Review Sub-score Columns ---
score_cols = [
    "review_scores_accuracy", "review_scores_cleanliness", "review_scores_checkin",
    "review_scores_communication", "review_scores_location", "review_scores_value", "review_scores_rating"
]

pretty_labels = [
    "Description Accuracy", "Cleanliness", "Smooth Checkin",
    "Host Communication", "Location", "Value", "Overall Rating"
]

available_cols = [c for c in score_cols if c in filtered_df_corr.columns]

# --- Plot Correlation Heatmap ---
if len(available_cols) >= 2:
    corr = filtered_df_corr[available_cols].corr()
    fig_corr, ax_corr = plt.subplots(figsize=(10, 8))
    cax = ax_corr.matshow(corr, cmap="Reds", vmin=0, vmax=1)
    fig_corr.colorbar(cax, ax=ax_corr)
    ax_corr.set_xticks(range(len(available_cols)))
    ax_corr.set_xticklabels(pretty_labels, rotation=45, ha="left")
    ax_corr.set_yticks(range(len(available_cols)))
    ax_corr.set_yticklabels(pretty_labels)
    ax_corr.set_title("Correlation Matrix of Review Sub-Scores", pad=20)
    st.pyplot(fig_corr)
else:
    st.info("⚠️ Not enough detailed score columns to compute correlations after applying filters.")

st.markdown("---")

# --- Footer ---
st.caption("© 2025 · Columbia University")