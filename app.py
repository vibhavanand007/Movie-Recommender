import streamlit as st
import compress_pickle

import pandas as pd
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=80668b158739828caac25bb7f4488dad&language=en-US"
    data = requests.get(url)
    data = data.json()
    st.text(data)
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return "No poster available"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']

        recommended_movies.append(movies.iloc[i[0]]['title'])

        #fetchPosterFromAPI--
        if fetch_poster(movie_id)!="No poster available":
            recommended_movies_posters.append((fetch_poster(movie_id)))
        else:
            pass


    return recommended_movies, recommended_movies_posters


movies = compress_pickle.load('movie_dict.gz', compression="gzip")
movies = pd.DataFrame(movies)

similarity = compress_pickle.load('similarity.gz', compression="gzip")

st.title("Movie Recommendation System")

selected_movie_names = st.selectbox(
    'Select a movie!',
    movies['title'].values
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_names)
    col1, col2, col3, col4, col5 = st.beta_columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])