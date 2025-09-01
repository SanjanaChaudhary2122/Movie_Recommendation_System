# Movie_Recommendation_System
A content-based movie recommendation system built using Python, pandas, scikit-learn, NLTK, and Streamlit.
This project processes movie metadata, builds a similarity model, and serves recommendations via a user-friendly web app.

# Features
Preprocesses TMDB 5000 Movie Dataset (movies + credits CSV files).
Extracts and combines metadata like genres, keywords, cast, crew, and overview.
Cleans and normalizes data using NLTK PorterStemmer.
Vectorizes movie tags using CountVectorizer (max_features=5000).
Computes movie similarity using cosine similarity.
Saves processed data into Pickle files (movies_dict.pkl, similarity.pkl).
Interactive web app using Streamlit:
Select a movie from a dropdown.
Get top 5 recommended movies with posters (from TMDB API).

# Tech Stack
Python 3.x
Libraries:
- pandas, numpy
- scikit-learn
- nltk
- requests
- pickle
- streamlit

# How It Works
Data Preprocessing
- Merge movies and credits datasets.
- Extract useful fields (genres, keywords, cast, crew, overview).
- Clean and normalize tags (lowercasing + stemming).

Feature Engineering
- Convert tags into numerical vectors using CountVectorizer.
- Build a cosine similarity matrix to measure how similar two movies are.
  
Recommendation System
- Input: Movie title.
- Output: Top 5 similar movies (sorted by cosine similarity).

Web App
- Dropdown menu to select movies.
- Fetch posters using TMDB API.
- Display recommendations with movie posters and titles.

<img width="972" height="657" alt="image" src="https://github.com/user-attachments/assets/8cc6a223-bfc7-422b-a9ac-36b4d77e4603" />
