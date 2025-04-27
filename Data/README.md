# 🗽 Manhattan Airbnb Listings & Reviews Data

This dataset contains Airbnb listings and associated reviews in **Manhattan**, New York City. The data has been filtered and cleaned for focused analysis on recent, detailed, English-language reviews.

---

## 📌 Data Source

The original data is sourced from the **Inside Airbnb** project, a mission-driven initiative that provides data and advocacy about Airbnb's impact on residential communities. Inside Airbnb collects and analyzes publicly available information from the Airbnb website to empower communities with insights into how Airbnb is being used in various cities. For more information and to access the original datasets, visit [Inside Airbnb](https://insideairbnb.com/).

---

## 📁 Dataset Description

This dataset is the result of merging and filtering three original data sources:

- `listings.csv`: Detailed  information and metrics for listings in New York City. 
- `reviews.csv`: Summary user-generated reviews for the listings.
-  `reviews.csv.gz`: Detailed review data for the listings.

After filtering, the final dataset includes:

- Listings located **only in Manhattan**
- Reviews written **in English**
- Reviews **on or after January 1, 2023**
- Rows with **no missing values**

---

## 📚 Data Dictionary

| Column                         | Type     | Description                                                                 |
|--------------------------------|----------|-----------------------------------------------------------------------------|
| `listing_id`                   | int64    | Unique identifier for each listing                                          |
| `listing_name`                 | object   | Title or name of the listing                                                |
| `host_id`                      | int64    | Unique identifier for the host                                              |
| `host_name`                    | object   | Name of the host                                                            |
| `neighbourhood_group`         | object   | Borough of the listing (e.g., Manhattan, Brooklyn)                         |
| `neighbourhood`               | object   | Specific neighborhood within the borough                                    |
| `latitude`                    | float64  | Latitude coordinate of the listing                                          |
| `longitude`                   | float64  | Longitude coordinate of the listing                                         |
| `room_type`                   | object   | Type of room offered (e.g., Entire home/apt, Private room)                 |
| `minimum_nights`              | int64    | Minimum number of nights required per booking                              |
| `number_of_reviews`           | int64    | Total number of reviews for the listing                                     |
| `review_id`                   | float64  | Unique identifier for each review                                           |
| `review_date`                 | object   | Date the review was posted (format: yyyy-mm-dd)                            |
| `reviewer_id`                 | float64  | Unique identifier for the reviewer                                          |
| `reviewer_name`               | object   | Name of the reviewer                                                        |
| `review_content`              | object   | Full text of the review                                                     |
| `bedrooms`                    | float64  | Number of bedrooms in the listing                                           |
| `beds`                        | float64  | Number of beds available in the listing                                     |
| `price`                       | float64  | Price per night in USD                                                      |
| `last_scraped_date`          | object   | Last date the data was scraped from Airbnb                                 |
| `review_scores_rating`        | float64  | Overall rating given by reviewers (typically out of 100)                   |
| `review_scores_accuracy`      | float64  | Accuracy of the listing description vs reality                              |
| `review_scores_cleanliness`   | float64  | Cleanliness score                                                           |
| `review_scores_checkin`       | float64  | Ease and convenience of the check-in process                                |
| `review_scores_communication` | float64  | Host’s responsiveness and communication quality                             |
| `review_scores_location`      | float64  | Location score based on guests’ satisfaction                                |
| `review_scores_value`         | float64  | Value for money score                                                       |
| `review_language`             | object   | Detected language of the review (only 'en' retained in final dataset)       |
