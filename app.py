'''import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=cddc3f9fcf337b3cc63456e156c7c8ed&language=en-US'.format(movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w185" + data["poster_path"]
#def fetch_poster(movie_id):
    #url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=cddc3f9fcf337b3cc63456e156c7c8ed&language=en-US"
    #response = requests.get(url)
    #data = response.json()

    #if "poster_path" in data and data["poster_path"]:
        #return "https://image.tmdb.org/t/p/w185" + data["poster_path"]
    #else:
        #return "https://via.placeholder.com/185x278.png?text=No+Poster"




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        #movie_id = i[0]
        movie_id = movies.iloc[i[0]].movie_id
        #fetch movie
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters
movies_dict=pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)
if st.button("Recommend"):
    names,posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])'''

import streamlit as st
import pickle
import pandas as pd
import requests
import time


# Function to fetch a poster with retry logic
def fetch_poster(movie_id, max_retries=3, backoff_factor=0.5):
    """
    Fetches a movie poster from TMDb API with retry logic for network errors.
    """
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=cddc3f9fcf337b3cc63456e156c7c8ed&language=en-US'

    for i in range(max_retries):
        try:
            response = requests.get(url, timeout=10)  # Added a timeout
            response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if "poster_path" in data and data["poster_path"]:
                return "https://image.tmdb.org/t/p/w185" + data["poster_path"]
            else:
                return "https://via.placeholder.com/185x278.png?text=No+Poster"

        except requests.exceptions.RequestException as e:
            # Catch all requests-related exceptions (ConnectionError, SSLError, Timeout, etc.)
            print(f"Attempt {i + 1} failed: {e}")
            if i < max_retries - 1:
                # Calculate sleep time with exponential backoff
                sleep_time = backoff_factor * (2 ** i)
                print(f"Retrying in {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)
            else:
                # All retries failed, return a placeholder or raise an error
                print("Max retries exceeded. Returning placeholder image.")
                return "https://via.placeholder.com/185x278.png?text=Error"

    # Fallback in case the loop finishes unexpectedly
    return "https://via.placeholder.com/185x278.png?text=Error"


def recommend(movie):
    try:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        recommended_movies = []
        recommended_movies_posters = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)

            # Call the robust fetch_poster function
            recommended_movies_posters.append(fetch_poster(movie_id))

        return recommended_movies, recommended_movies_posters
    except IndexError:
        st.error("Movie not found in the database. Please select another one.")
        return [], []
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return [], []


# Load data
try:
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error(
        "Data files (movies_dict.pkl or similarity.pkl) not found. Please ensure they are in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading data files: {e}")
    st.stop()

# Streamlit UI
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

if st.button("Recommend"):
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie_name)

    if names:  # Check if names list is not empty before proceeding
        # Create columns for the display
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.image(posters[0])
            st.text(names[0])

        with col2:
            st.image(posters[1])
            st.text(names[1])

        with col3:
            st.image(posters[2])
            st.text(names[2])

        with col4:
            st.image(posters[3])
            st.text(names[3])

        with col5:
            st.image(posters[4])
            st.text(names[4])


