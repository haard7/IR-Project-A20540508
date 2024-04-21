
**Note:** To Run this project please refer the Readme.md file in respective folders (crawler, indexer, and processor).There I have described in detail that how to run each component.
Here you will only find the project Report.


#### Video Demo : [https://youtu.be/2FCJG22ZYxQ](https://youtu.be/2FCJG22ZYxQ)

# Project Report

#### Student Name: Haard Patel
#### CWID: A20540508

## Abstract
- There are three components developed in this projects which is aimed to articulate the end to end search engine functionality at small scale to understand how actually the web search engines work.


## Overview

### 1) Crawler
- It is **Scrapy** based crawler which download the `html` documents based on given URLs and parameters of `max_depth` and `max_pages`.

- In the given project I have used wikipedia URLs, mostly related to renewable energy and power. basically I am downloading the bunch of html documents in `-->crawler-->Data` directory. those all html documents will be used in the next component to build the inverted index. Documents are downloaded with the name of last path of the url to keep track of the documents.

Example Scnreeshot:

![1_crawler](https://github.com/haard7/IR-Project-A20540508/assets/69381806/90b18f45-631d-4f84-81a6-f64ddf2ed57e)


### 2) Indexer
- It is sci-kit learn based indexer which create the inverted index on the data by parsing the html documents from the crawler.
- It uses the functionality of Tf-IDf score and Cosine Similarity to create the inverted-index
- In this components there are two files get generated. one, `inverted_index.json` which containes the postings corresponding to each term. second, `content.json` to store the document id and corrersponding document_name and Content which will also print in Flask based processor to debug whether our search results are working well or not.
- You can also locally test the indexer by running `python indexer.py` and modifying the `config.json` to see the console output of the list of top-k documents being printed

Example Screenshots

![2_Indexer](https://github.com/haard7/IR-Project-A20540508/assets/69381806/b56188af-2ae1-470c-9f60-8e770fed86ba)


### 3) Processor
- It `Flask` based processor to print print the top-k results by performing the query validation/error checking and spelling correction. I have used `NLTK` for stopword removal and `FuzzyWuzzy` for `spelling correction`.
- my flask app give the UI results of top-k resutls for searched queries. It also give the JSON documents of top-k results. It includes the document name, document ID and Content as well.

Example Screenshots

![3 1_new](https://github.com/haard7/IR-Project-A20540508/assets/69381806/f5629964-5726-4cf6-8a97-8226202b3003)

![3 2_new](https://github.com/haard7/IR-Project-A20540508/assets/69381806/81cfde06-0146-4d9d-b253-f6e2b68879df)

![3 3_new](https://github.com/haard7/IR-Project-A20540508/assets/69381806/689aa261-3e1e-4bde-bd3d-3e04bc091285)
## Design
- Basically its monolithic design where we have three separate components run separately but they are depended on the output of previous component

## Architecture

- **Web Crawler**: Downloads web documents in HTML format using Scrapy.
- **Indexer**: Constructs an inverted index using Scikit-Learn.
- **Query Processor**: Handles text queries and returns relevant documents via a Flask server.


## Operation

### Crawler Operation

Uses Scrapy to fetch and store web pages. Initiated with user-defined settings for depth and breadth of the crawl.

### Indexing Operation

Processes documents and constructs an inverted index using TF-IDF vectors, stored in pickle format.

### Query Processing

Flask application receives, validates, and processes queries, using the inverted index to fetch and rank documents.


## Conclusion

- Finally, This project is successfully demonstrating how the simplest search engine work
- It is very important to limit the depth of crawling to maintain the relavacy of documents. Also, In this project the documents fetched in flask app can be made more relevant using machine learning techniques as well as advances search algorithms using vector classification, probabilistic method and many others.
- Basic functionalities are working well but it is not production ready. As we have to create the microservices and automate the three components to interact with each other via API.
- However, this project demonsrate the basic seach functionalities very well with good precision. In terms of recall it is upto use how many results he want to fetch. so there is no any limit on recall. But in the future work it can be imporved

## Data Sources

- For scrapping I have used the wikipedia documents related to power and energy.Specifically, Most of the documents are related to renewable energy. Below is the list of urls which has been scrapped.

Note: you can replace the links by the choice of your wikipedia links to test it


- [Renewable Energy in the United States](https://en.wikipedia.org/wiki/Renewable_energy_in_the_United_States)
- [List of Renewable Energy Topics by Country and Territory](https://en.wikipedia.org/wiki/List_of_renewable_energy_topics_by_country_and_territory)
- [Renewable Energy (Simple English)](https://simple.wikipedia.org/wiki/Renewable_energy)
- [List of Books About Renewable Energy](https://en.wikipedia.org/wiki/List_of_books_about_renewable_energy)
- [Renewable Energy in the United Kingdom](https://en.wikipedia.org/wiki/Renewable_energy_in_the_United_Kingdom)
- [Solar Power](https://en.wikipedia.org/wiki/Solar_power)
- [Wind Power](https://en.wikipedia.org/wiki/Wind_power)
- [Bioenergy](https://en.wikipedia.org/wiki/Bioenergy)
- [Geothermal Energy](https://en.wikipedia.org/wiki/Geothermal_energy)
- [Hydropower](https://en.wikipedia.org/wiki/Hydropower)

## Test Cases

### Crawler

- **Input urls**: You can try with the different urls of wikipedia. to modify this go to crawler > wiki_crawler > spiders > wiki_spider.py
- **Depth Control Test**: test with the various parameters of maximum depth and number of pages to scrap.

### Indexer

- **Index Creation Test**: To test the Indexer you can write a free text query to see the console output for retrieved document for given query. Modify the `config.json` file
- you can see the resulted inverted index at `inverted_index.json` file.


### Processor

- **Main Test**: go to `/json` to view the complete output of top-k results including the content where we can debug and cross check whether the results are accurate or not.
- **Query Handling Test**: after ruuning the flask server with `flask run`, write a query in search box like `Sun the renewable source of energy`to see the relevant document fetched. because we have scrapped the documents related to energy. For more detail output go to `/json` output
- **Error Handling Test**: Tests system's response to malformed queries.
- **Accuracy and Recall test**: you can modify the parameter `k` to retrieve the specific number of document you want to fetch when you enter a query. you can change the value of k in `>crawler > processor > app.py`. change the k value in function `get_top_k_results(query_terms, k=5)`
- **Spell-correction Test**: you can misspelled something like `hydropover energi` but it will give the output of documents for corrected query `hydropower energy`

## Source code

This repository is public. Feel free to contribute.

#### code structure

- `crawler/`: Scrapy spiders and settings.
- `indexer/`: Scripts for document processing and index construction.
- `processor/`: Flask application for query processing.

#### Code Documentation

you can find the source code documentation at [Documentation](https://www.overleaf.com/read/xrrsjhpzcrsb#0abf05). Currently I am writting it. very soon you will see the complete documentation.

## Bibliography

- Scrapy Documentation: "Scrapy Documentation." Accessed April 17, 2024. [https://docs.scrapy.org/en/latest/](https://docs.scrapy.org/en/latest/)

- Scikit-Learn Tutorials: "Scikit-Learn Tutorials." Accessed April 17, 2024. [https://scikit-learn.org/stable/tutorial/index.html](https://scikit-learn.org/stable/tutorial/index.html)

- Flask Documentation: "Flask Documentation." Accessed April 17, 2024. [https://flask.palletsprojects.com/en/2.2.x/](https://flask.palletsprojects.com/en/2.2.x/)

- ChatGPT prompt: "How to Use Pickle Format in Python." ChatGPT prompt.

- Blog on extracting the text from HTML document: "How Do I Extract Text from HTML Elements Using Beautiful Soup?" Last modified 2024. [https://webscraping.ai/faq/beautiful-soup/how-do-i-extract-text-from-html-elements-using-beautiful-soup](https://webscraping.ai/faq/beautiful-soup/how-do-i-extract-text-from-html-elements-using-beautiful-soup)

- HTML Documentation: "HTML Forms." W3Schools. Accessed April 17, 2024. [https://www.w3schools.com/html/html_forms.asp](https://www.w3schools.com/html/html_forms.asp)
