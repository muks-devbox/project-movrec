import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def load_data(file_path="data/movies.csv"):
    movies = pd.read_csv(file_path)

    movies['genres'] = movies['genres'].str.replace('|', ' ', regex=False)

    movies = movies[movies['genres'] != '(no genres listed)']
    return movies

def build_similarity_matrix(movies):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])

    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
    return similarity_matrix

def get_recommendations(movie_title, movies, similarity_matrix, top_n=5):

    indices = pd.Series(movies.index, index=movies['title']).drop_duplicates()

    if movie_title not in indices:
        # Return an empty DataFrame with the same columns as movies plus similarity_score
        empty_df = movies.iloc[0:0].copy()
        empty_df['similarity_score'] = []
        return empty_df

    idx = indices[movie_title]

    sim_scores = list(enumerate(similarity_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    movie_indices = [i[0] for i in sim_scores]

    # Select all columns for the recommended movies
    result = movies.iloc[movie_indices].copy()
    result['similarity_score'] = [round(i[1], 3) for i in sim_scores]
    return result

movies = load_data()
cosine_sim = build_similarity_matrix(movies)
all_titles = movies["title"].tolist()