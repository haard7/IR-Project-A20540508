import os
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from bs4 import BeautifulSoup
from w3lib.html import replace_entities, remove_tags


def extract_text_from_html(directory):
    documents = []
    filenames = []
    document_contents = {}
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file.read(), "lxml")
                paragraphs = soup.find_all("p")
                clean_text = " ".join(
                    replace_entities(remove_tags(str(p))) for p in paragraphs
                ).strip()
                documents.append(clean_text)
                filenames.append(filename)
                document_id = len(documents) - 1  # Use document index as ID
                document_contents[document_id] = {
                    "document_name": filename,
                    "content": clean_text,
                }
    with open("content.json", "w", encoding="utf-8") as f:
        json.dump(document_contents, f, ensure_ascii=False, indent=4)
    return documents, filenames


def build_tfidf_index(documents):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
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
            if densed_list[row][col] > 0:
                if term not in inverted_index:
                    inverted_index[term] = []
                document_entry = {
                    "filename": filenames[row],
                    "tfidf": densed_list[row][col],
                    "document_id": row,  # Using the row index as a document ID
                }
                inverted_index[term].append(document_entry)

    with open("inverted_index.json", "w", encoding="utf-8") as f:
        json.dump(inverted_index, f, ensure_ascii=False, indent=4)


# Example usage
directory = "../crawler/data"
documents, filenames = extract_text_from_html(directory)
vectorizer, tfidf_matrix = build_tfidf_index(documents)
save_inverted_index_json(vectorizer, tfidf_matrix, filenames)


# below code is to see the console output


def load_index():
    with open("tfidf_model.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("tfidf_matrix.pkl", "rb") as f:
        tfidf_matrix = pickle.load(f)
    return vectorizer, tfidf_matrix

def load_config(config_path="config.json"):
    with open(config_path, "r") as f:
        config = json.load(f)
    return config["top_k"], config["query"]


def query_index(query, vectorizer, tfidf_matrix, filenames, top_k):
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    doc_similarities = sorted(
        enumerate(zip(filenames, similarities)), key=lambda x: x[1][1], reverse=True
    )
    top_documents = [
        {"document_id": doc_id, "filename": filename, "tfidf_score": score}
        for doc_id, (filename, score) in doc_similarities[:top_k]
    ]
    return top_documents


# Load index and configuration
top_k, query_text = load_config()
vectorizer, tfidf_matrix = load_index()
filenames = [
    filename for filename in os.listdir("../crawler/data") if filename.endswith(".html")
]

# Fetch top documents based on the query
top_docs = query_index(query_text, vectorizer, tfidf_matrix, filenames, top_k)

# Print the top documents with their details
print(f"Top {top_k} documents based on cosine similarity:")
for doc in top_docs:
    print(
        f"Document ID: {doc['document_id']}, Document: {doc['filename']}, TF-IDF Score: {doc['tfidf_score']}"
    )


# import os
# import pickle
# import json
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# from bs4 import BeautifulSoup


# def extract_text_from_html(directory):
#     documents = []
#     filenames = []
#     for filename in os.listdir(directory):
#         if filename.endswith(".html"):
#             filepath = os.path.join(directory, filename)
#             with open(filepath, "r", encoding="utf-8") as file:
#                 soup = BeautifulSoup(file.read(), "lxml")
#                 text = soup.get_text()
#                 documents.append(text)
#                 filenames.append(filename)
#     return documents, filenames


# def build_tfidf_index(documents):
#     vectorizer = TfidfVectorizer()
#     tfidf_matrix = vectorizer.fit_transform(documents)
#     with open("tfidf_model.pkl", "wb") as f:
#         pickle.dump(vectorizer, f)
#     with open("tfidf_matrix.pkl", "wb") as f:
#         pickle.dump(tfidf_matrix, f)
#     return vectorizer, tfidf_matrix


# def save_inverted_index_json(vectorizer, tfidf_matrix, filenames):
#     feature_names = vectorizer.get_feature_names_out()
#     dense = tfidf_matrix.todense()
#     densed_list = dense.tolist()

#     inverted_index = {}
#     for col in range(tfidf_matrix.shape[1]):
#         term = feature_names[col]
#         for row in range(tfidf_matrix.shape[0]):
#             if densed_list[row][col] > 0:
#                 if term not in inverted_index:
#                     inverted_index[term] = []
#                 document_entry = {
#                     "filename": filenames[row],
#                     "tfidf": densed_list[row][col],
#                     "document_id": row,  # Using the row index as a document ID
#                 }
#                 inverted_index[term].append(document_entry)

#     with open("inverted_index.json", "w", encoding="utf-8") as f:
#         json.dump(inverted_index, f, ensure_ascii=False, indent=4)


# # Example usage
# directory = "../crawler/data"
# documents, filenames = extract_text_from_html(directory)
# vectorizer, tfidf_matrix = build_tfidf_index(documents)
# save_inverted_index_json(vectorizer, tfidf_matrix, filenames)


# def load_index():
#     with open("tfidf_model.pkl", "rb") as f:
#         vectorizer = pickle.load(f)
#     with open("tfidf_matrix.pkl", "rb") as f:
#         tfidf_matrix = pickle.load(f)
#     return vectorizer, tfidf_matrix

# def load_config(config_path="config.json"):
#     with open(config_path, "r") as f:
#         config = json.load(f)
#     return config["top_k"], config["query"]


# def query_index(query, vectorizer, tfidf_matrix, filenames, top_k):
#     query_vector = vectorizer.transform([query])
#     similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
#     doc_similarities = sorted(
#         enumerate(zip(filenames, similarities)), key=lambda x: x[1][1], reverse=True
#     )
#     top_documents = [
#         {"document_id": doc_id, "filename": filename, "tfidf_score": score}
#         for doc_id, (filename, score) in doc_similarities[:top_k]
#     ]
#     return top_documents


# # Load index and configuration
# top_k, query_text = load_config()
# vectorizer, tfidf_matrix = load_index()
# filenames = [
#     filename for filename in os.listdir("../crawler/data") if filename.endswith(".html")
# ]

# # Fetch top documents based on the query
# top_docs = query_index(query_text, vectorizer, tfidf_matrix, filenames, top_k)

# # Print the top documents with their details
# print(f"Top {top_k} documents based on cosine similarity:")
# for doc in top_docs:
#     print(
#         f"Document ID: {doc['document_id']}, Document: {doc['filename']}, TF-IDF Score: {doc['tfidf_score']}"
#     )
