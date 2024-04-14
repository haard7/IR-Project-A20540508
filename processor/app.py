from flask import Flask, request, render_template_string, jsonify
import json

app = Flask(__name__)

# Load the inverted index with explicit encoding
with open("../indexer/inverted_index.json", "r", encoding="utf-8") as f:
    inverted_index = json.load(f)


def get_top_k_results(query_terms, k=5):
    # Calculate the aggregate tf-idf scores for documents
    doc_scores = {}
    for term in query_terms:
        if term in inverted_index:
            for doc, score in inverted_index[term]:
                if doc in doc_scores:
                    doc_scores[doc] += score
                else:
                    doc_scores[doc] = score

    # Sort documents based on scores in descending order and select top-k
    top_k_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)[:k]
    return top_k_docs


@app.route("/", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form["query"].strip()  # Trim whitespace from both ends
        if not query:  # Check if query is empty
            return render_template_string(
                FORM_TEMPLATE, error="Please enter a search query."
            )

        query_terms = query.split()
        top_k_results = get_top_k_results(query_terms, k=5)
        results = [{"document": doc, "score": score} for doc, score in top_k_results]
        return render_template_string(RESULTS_TEMPLATE, query=query, results=results)
    return render_template_string(FORM_TEMPLATE)


# def home():
#     if request.method == "POST":
#         query = request.form["query"]
#         query_terms = query.split()
#         top_k_results = get_top_k_results(query_terms, k=5)
#         results = [{"document": doc, "score": score} for doc, score in top_k_results]
#         return render_template_string(RESULTS_TEMPLATE, query=query, results=results)
#     return render_template_string(FORM_TEMPLATE)


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
                <div class="document-name">{{ result.document }}</div>
                <div class="score">Score: {{ result.score | round(4) }}</div>
            </div>
        {% endfor %}
        </div>
    {% else %}
        <p>No results found</p>
    {% endif %}
    <a href="/">New search</a>
</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)
