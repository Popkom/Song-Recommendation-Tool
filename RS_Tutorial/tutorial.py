import pandas as pd

# Read data
metadata = pd.read_csv("movies_metadata.csv", low_memory=False)

# Recommender that just lists top movies based on weighted movie reviews

# Get average score of all movies
C = metadata["vote_average"].mean()

# Get number of votes received by a movie in the 90th percentile
m = metadata["vote_count"].quantile(0.90)

# Create independent DataFrame to filter out movies with less than 160 votes
q_movies = metadata.copy().loc[metadata["vote_count"] >= m]


# Calculate weighted rating for each qualified movie
def weighted_rating(x, m=m, C=C):
    v = x["vote_count"]
    R = x["vote_average"]
    # Calculation is based on IMDB formula
    return (v / (v + m) * R) + (m / (m + v) * C)


# score is a new feature, calculate is value with the func defined above
q_movies["score"] = q_movies.apply(weighted_rating, axis=1)

# Sort movies based on score
q_movies = q_movies.sort_values("score", ascending=False)

# Print top 25 movies
# print(q_movies[["title", "vote_count", "vote_average", "score"]].head(25))

# Recommender based on movie plot
# Print plot overviews of the first 5 movies
# print(metadata["overview"].head())

from sklearn.feature_extraction.text import TfidfVectorizer

# Define a TF-IDF(Term Frequency-Inverse Document Frequency) object. Remove all stop words
tfidf = TfidfVectorizer(stop_words="english")

# Replace NaN with empty string
metadata["overview"] = metadata["overview"].fillna("")

# Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(metadata["overview"])

# Print shape of matrix
# print(tfidf_matrix.shape)

# Array mapping from feature integer indices to feature name
# print(tfidf.get_feature_names_out()[5000:5010])

# Calculate matrix of similarity scores between movies
from sklearn.metrics.pairwise import linear_kernel

# Compute the cosine similarity matrix
# cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Print shape
# print(cosine_sim.shape)

# Construct a reverse map of indices and movie titles
indices = pd.Series(metadata.index, index=metadata["title"]).drop_duplicates()


# Function that takes movie title as input and prints a list of the 10 most similar movies
def get_recommendations(title, cosine_sim):
    # Get index of movie given
    idx = indices[title]

    # Get the pairwise similarity scores of all movies with that title
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort movies based on similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:11]

    # Get movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return metadata["title"].iloc[movie_indices]


# print(get_recommendations("Your Name."))
# print("#####")
# print(get_recommendations("The Dark Knight Rises"))

# Credits, Genres, and Keywords Based Recommender
# Load keywords and credits
credits = pd.read_csv("credits.csv")
keywords = pd.read_csv("keywords.csv")

# Remove rows with bad IDs
metadata = metadata.drop([19730, 29503, 35587])

# Convert IDs to int
keywords["id"] = keywords["id"].astype("int")
credits["id"] = credits["id"].astype("int")
metadata["id"] = metadata["id"].astype("int")

# Merge keywords and credits into your main metadata dataframe
metadata = metadata.merge(credits, on="id")
metadata = metadata.merge(keywords, on="id")

# Parse the stringified features into their corresponding python objects
from ast import literal_eval

features = ["cast", "crew", "keywords", "genres"]
for feature in features:
    metadata[feature] = metadata[feature].apply(literal_eval)

import numpy as np


def get_director(x):
    for i in x:
        if i["job"] == "Director":
            return i["name"]
    return np.nan


def get_list(x):
    if isinstance(x, list):
        names = [i["name"] for i in x]
        # Check if more than 3 elements exist. If yes, return only the first three. If no, return the entire list
        if len(names) > 3:
            names = names[:3]
        return names
    # return empty list in case of missing/malformed data
    return []


# Define new director, cast, genres and keywords features that are in a suitable form
metadata["director"] = metadata["crew"].apply(get_director)

features = ["cast", "keywords", "genres"]
for feature in features:
    metadata[feature] = metadata[feature].apply(get_list)

# Print features of the first three films
# print(metadata[["title", "cast", "director", "keywords", "genres"]].head(3))


# Function to convert all strings to lowercase and strip names of spaces
def clean_data(x):
    if isinstance(x, list):
        return [str.lower(i.replace(" ", "")) for i in x]
    else:
        # Check if director exists. If not, return empty string
        if isinstance(x, str):
            return str.lower(x.replace(" ", ""))
        else:
            return ""


# Apply clean_data to the features
features = ["cast", "keywords", "director", "genres"]

for feature in features:
    metadata[feature] = metadata[feature].apply(clean_data)


# Create metadata soup
def create_soup(x):
    return (
        " ".join(x["keywords"])
        + " "
        + " ".join(x["cast"])
        + " "
        + x["director"]
        + " "
        + " ".join(x["genres"])
    )


# Create a new soup feature
metadata["soup"] = metadata.apply(create_soup, axis=1)

# print(metadata[["soup"]].head(2))

# Import CountVectorizer and create the count matrix
from sklearn.feature_extraction.text import CountVectorizer

count = CountVectorizer(stop_words="english")
count_matrix = count.fit_transform(metadata["soup"])

# Compute the Cosine Similarity matrix based on the count_matrix
from sklearn.metrics.pairwise import cosine_similarity

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

# Reset index of main DataFrame and construct reverse mapping as before
metadata = metadata.reset_index()
indices = pd.Series(metadata.index, index=metadata["title"])

print(get_recommendations("Your Name.", cosine_sim2))
print("###")
print(get_recommendations("The Dark Knight Rises", cosine_sim2))
