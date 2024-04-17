from flask import Flask, request, render_template_string, jsonify
import json
from fuzzywuzzy import process

# Import NLTK for stop words removal
import nltk
from nltk.corpus import stopwords

# Download NLTK stopwords list if not already downloaded
nltk.download("stopwords")

app = Flask(__name__)

# Load the inverted index with explicit encoding
with open("../indexer/inverted_index.json", "r", encoding="utf-8") as f:
    inverted_index = json.load(f)

# Load NLTK English stopwords
stop_words = set(stopwords.words("english"))

# Global variable to store the latest query results
latest_results = []


def get_top_k_results(query_terms, k=5):
    # Calculate the aggregate tf-idf scores for documents and store document IDs
    doc_scores = {}
    doc_ids = {}
    for term in query_terms:
        if term in inverted_index:
            for entry in inverted_index[term]:
                doc = entry["filename"]
                score = entry["tfidf"]
                doc_id = entry["document_id"]
                if doc in doc_scores:
                    doc_scores[doc] += score
                else:
                    doc_scores[doc] = score
                    doc_ids[doc] = doc_id  # Store document ID corresponding to filename

    # Sort documents based on scores in descending order and select top-k
    top_k_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:k]
    return [
        (doc, doc_ids[doc], score) for doc, score in top_k_docs
    ]  # Return doc, doc_id, score


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        query = request.form["query"].strip()  # Trim whitespace from both ends

        if not query:  # Check if query is empty
            return render_template_string(
                FORM_TEMPLATE, error="Please enter a search query."
            )

        # Correct misspelled terms
        corrected_terms = []
        for term in query.split():
            corrected_term, score = process.extractOne(term, inverted_index.keys())
            if score >= 80:  # Adjust this threshold according to your preference
                corrected_terms.append(corrected_term)
            else:
                corrected_terms.append(term)
        query_terms = [
            word for word in corrected_terms if word.lower() not in stop_words
        ]

        global latest_results
        latest_results = get_top_k_results(query_terms, k=5)
        results = [
            {"document_id": doc_id, "document": doc, "score": score}
            for doc, doc_id, score in latest_results
        ]
        return render_template_string(RESULTS_TEMPLATE, query=query, results=results)
    return render_template_string(FORM_TEMPLATE)


@app.route("/json", methods=["GET"])
def json_results():
    # Load content data from JSON file
    with open("../indexer/content.json", "r", encoding="utf-8") as file:
        content_data = json.load(file)

    # Prepare and return the latest results in JSON format, including the content
    results = []
    for doc, doc_id, score in latest_results:
        doc_content = content_data.get(str(doc_id), {}).get(
            "content", "No content available"
        )
        results.append(
            {
                "content": doc_content,
                "document_id": doc_id,
                "document_name": doc,
                "tfidf_score": score,
            }
        )
    return jsonify(results)


FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Search</title>
</head>
<body>
    <h2>Enter your search query</h2>
    <form method="post">
        <input type="text" name="query" />
        <input type="submit" value="Search" />
    </form>
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
"""

RESULTS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Search Results</title>
    <style>
        .result-item {
            margin-bottom: 10px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .document-name {
            font-size: 18px;
            font-weight: bold;
        }
        .document-id {
            font-size: 14px;
            color: #666;
        }
        .score {
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
    <h2>Results for "{{ query }}"</h2>
    {% if results %}
        <div>
        {% for result in results %}
            <div class="result-item">
                <div class="document-name">Document: {{ result.document }}</div>
                <div class="document-id">Document ID: {{ result.document_id }}</div>
                <div class="score">TF-IDF Score: {{ result.score | round(4) }}</div>
            </div>
        {% endfor %}
        </div>
    {% else %}
        <p>No results found</p>
    {% endif %}
    <a href="/">New search</a> | <a href="/json">JSON</a>
    <h4>Note: Click on json link to view the json output which contains "document_id", "url" and most importantly "Content". so it is easy to review.</h4>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)


# from flask import Flask, request, render_template_string, jsonify
# import json

# # Import NLTK for stop words removal
# import nltk
# from nltk.corpus import stopwords

# # Download NLTK stopwords list if not already downloaded
# nltk.download("stopwords")

# app = Flask(__name__)

# # Load the inverted index with explicit encoding
# with open("../indexer/inverted_index.json", "r", encoding="utf-8") as f:
#     inverted_index = json.load(f)

# # Load NLTK English stopwords
# stop_words = set(stopwords.words("english"))

# # Global variable to store the latest query results
# latest_results = []


# def get_top_k_results(query_terms, k=5):
#     # Calculate the aggregate tf-idf scores for documents and store document IDs
#     doc_scores = {}
#     doc_ids = {}
#     for term in query_terms:
#         if term in inverted_index:
#             for entry in inverted_index[term]:
#                 doc = entry["filename"]
#                 score = entry["tfidf"]
#                 doc_id = entry["document_id"]
#                 if doc in doc_scores:
#                     doc_scores[doc] += score
#                 else:
#                     doc_scores[doc] = score
#                     doc_ids[doc] = doc_id  # Store document ID corresponding to filename

#     # Sort documents based on scores in descending order and select top-k
#     top_k_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:k]
#     return [
#         (doc, doc_ids[doc], score) for doc, score in top_k_docs
#     ]  # Return doc, doc_id, score


# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":

#         query = request.form["query"].strip()  # Trim whitespace from both ends

#         if not query:  # Check if query is empty
#             return render_template_string(
#                 FORM_TEMPLATE, error="Please enter a search query."
#             )

#         # Tokenize query and remove stop words
#         query_terms = [word for word in query.split() if word.lower() not in stop_words]

#         global latest_results
#         latest_results = get_top_k_results(query_terms, k=5)
#         results = [
#             {"document_id": doc_id, "document": doc, "score": score}
#             for doc, doc_id, score in latest_results
#         ]
#         return render_template_string(RESULTS_TEMPLATE, query=query, results=results)
#     return render_template_string(FORM_TEMPLATE)


# @app.route("/json", methods=["GET"])
# def json_results():
#     # Load content data from JSON file
#     with open("../indexer/content.json", "r", encoding="utf-8") as file:
#         content_data = json.load(file)

#     # Prepare and return the latest results in JSON format, including the content
#     results = []
#     for doc, doc_id, score in latest_results:
#         doc_content = content_data.get(str(doc_id), {}).get(
#             "content", "No content available"
#         )
#         results.append(
#             {
#                 "content": doc_content,
#                 "document_id": doc_id,
#                 "document_name": doc,
#                 "tfidf_score": score,
#             }
#         )
#     return jsonify(results)


# # def json_results():
# #     # Return the latest results in JSON format
# #     results = [
# #         {"document_id": doc_id, "document_name": doc, "tfidf_score": score}
# #         for doc, doc_id, score in latest_results
# #     ]
# #     return jsonify(results)


# FORM_TEMPLATE = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Search</title>
# </head>
# <body>
#     <h2>Enter your search query</h2>
#     <form method="post">
#         <input type="text" name="query" />
#         <input type="submit" value="Search" />
#     </form>
#     {% if error %}
#         <p style="color: red;">{{ error }}</p>
#     {% endif %}
# </body>
# </html>
# """

# RESULTS_TEMPLATE = """
# <!DOCTYPE html>
# <html>
# <head>
#     <title>Search Results</title>
#     <style>
#         .result-item {
#             margin-bottom: 10px;
#             padding: 10px;
#             border: 1px solid #ddd;
#             border-radius: 5px;
#         }
#         .document-name {
#             font-size: 18px;
#             font-weight: bold;
#         }
#         .document-id {
#             font-size: 14px;
#             color: #666;
#         }
#         .score {
#             font-size: 14px;
#             color: #666;
#         }
#     </style>
# </head>
# <body>
#     <h2>Results for "{{ query }}"</h2>
#     {% if results %}
#         <div>
#         {% for result in results %}
#             <div class="result-item">
#                 <div class="document-name">Document: {{ result.document }}</div>
#                 <div class="document-id">Document ID: {{ result.document_id }}</div>
#                 <div class="score">TF-IDF Score: {{ result.score | round(4) }}</div>
#             </div>
#         {% endfor %}
#         </div>
#     {% else %}
#         <p>No results found</p>
#     {% endif %}
#     <a href="/">New search</a> | <a href="/json">JSON</a>
#     <h4>Note: Click on json link to view the json output which contains "document_id", "url" and most importantly "Content". so it is easy to review.</h4>
# </body>
# </html>
# """

# if __name__ == "__main__":
#     app.run(debug=True)
