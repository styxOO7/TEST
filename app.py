import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('moviesDict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    similarity_scores = similarity[idx]
    movie_list = sorted(list(enumerate(similarity_scores)),
                        reverse=True, key=lambda x: x[1])[1:6]

    recommendations = []
    posters = []
    overview = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommendations.append(movies.iloc[i[0]].title)
        overview.append(movies.iloc[i[0]].description)
        posters.append(fetch_poster(movie_id))

    return recommendations, overview, posters


st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Select any movie: ',
    movies['title'].values)

if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_desc, recommended_movie_posters = recommend(
        selected_movie_name)

    for i in range(0, 5):
        with st.container():
            st.header(f"{i+1}. {recommended_movie_names[i]}")
            st.image(recommended_movie_posters[i], width=222)
            st.write(recommended_movie_desc[i])


