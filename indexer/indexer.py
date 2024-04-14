import os
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup


# Modified to return filenames
def extract_text_from_html(directory):
    documents = []
    filenames = []
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file.read(), "lxml")
                text = soup.get_text()
                documents.append(text)
                filenames.append(filename)
    return documents, filenames


def build_tfidf_index(documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    # Save the model and matrix for later use
    with open("tfidf_model.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open("tfidf_matrix.pkl", "wb") as f:
        pickle.dump(tfidf_matrix, f)

    return vectorizer, tfidf_matrix


def save_inverted_index_json(vectorizer, tfidf_matrix, filenames):
    feature_names = vectorizer.get_feature_names_out()
    dense = tfidf_matrix.todense()
    densed_list = dense.tolist()

    inverted_index = {}
    for col in range(tfidf_matrix.shape[1]):
        term = feature_names[col]
        for row in range(tfidf_matrix.shape[0]):
            if densed_list[row][col] > 0:  # Term is present in the document
                if term not in inverted_index:
                    inverted_index[term] = []
                inverted_index[term].append((filenames[row], densed_list[row][col]))

    with open("inverted_index.json", "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=4)


# Example usage
directory = "../crawler/data"
documents, filenames = extract_text_from_html(directory)
vectorizer, tfidf_matrix = build_tfidf_index(documents)
save_inverted_index_json(vectorizer, tfidf_matrix, filenames)


# Load and query the index
def query_index(query, vectorizer, tfidf_matrix, filenames):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Map similarities to filenames
    doc_similarities = sorted(
        zip(filenames, similarities), key=lambda x: x[1], reverse=True
    )
    return doc_similarities[
        :5
    ]  # Adjust this number to change how many results you want


def load_index():
    with open("tfidf_model.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)
    return vectorizer, tfidf_matrix


# vectorizer, tfidf_matrix = load_index()
# query = "solar energy"
# top_docs = query_index(query, vectorizer, tfidf_matrix, filenames)

# print("Top documents based on cosine similarity:")
# for doc, score in top_docs:
#     print(f"Document: {doc}, Similarity Score: {score}")

### new stuff


def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["top_k"], config["query"]


def query_index(query, vectorizer, tfidf_matrix, filenames, top_k):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    doc_similarities = sorted(
        zip(filenames, similarities), key=lambda x: x[1], reverse=True
    )
    return doc_similarities[:top_k]


top_k, query_text = load_config()

# Assuming you have already built and saved the index
vectorizer, tfidf_matrix = load_index()
filenames = [
    filename
    for filename in os.listdir("../crawler/data")
    if filename.endswith(".html")
]  # Re-collect filenames

top_docs = query_index(query_text, vectorizer, tfidf_matrix, filenames, top_k)

print(f"Top {top_k} documents based on cosine similarity:")
for doc, score in top_docs:
    print(f"Document: {doc}, Similarity Score: {score}")


###### VESRION-1 ########

# below code is not having json output and also the console output of names of top documents.


# import os
# import pickle
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from bs4 import BeautifulSoup


# def extract_text_from_html(directory):
#     documents = []
#     for filename in os.listdir(directory):
#         if filename.endswith(".html"):
#             filepath = os.path.join(directory, filename)
#             with open(filepath, "r", encoding="utf-8") as file:
#                 soup = BeautifulSoup(file.read(), "lxml")
#                 text = soup.get_text()
#                 documents.append(text)
#     return documents


# def build_tfidf_index(documents):
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(documents)

#     # Save the model and matrix for later use
#     with open("tfidf_model.pkl", "wb") as f:
#         pickle.dump(vectorizer, f)
#     with open("tfidf_matrix.pkl", "wb") as f:
#         pickle.dump(tfidf_matrix, f)

#     return vectorizer, tfidf_matrix


# def load_index():
#     with open("tfidf_model.pkl", "rb") as f:
#         vectorizer = pickle.load(f)
#     with open("tfidf_matrix.pkl", "rb") as f:
#         tfidf_matrix = pickle.load(f)
#     return vectorizer, tfidf_matrix


# def query_index(query, vectorizer, tfidf_matrix):
#     query_vector = vectorizer.transform([query])
#     similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
#     return similarities


# directory = "../wiki_crawler/data"

# # Extract text from HTML documents
# documents = extract_text_from_html(directory)

# # Build the Tf-idf index
# vectorizer, tfidf_matrix = build_tfidf_index(documents)

# # Load the index (this step is illustrative; you would do this in a different script or session)
# vectorizer, tfidf_matrix = load_index()

# # Query the index
# query = "solar energy"
# similarities = query_index(query, vectorizer, tfidf_matrix)

# # Display top 5 similar documents
# top_docs = similarities.argsort()[-5:][::-1]
# print("Top 5 documents based on cosine similarity:")
# for i in top_docs:
#     print(f"Document {i}, Similarity Score: {similarities[i]}")
