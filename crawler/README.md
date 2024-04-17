
## How to run

### Crawler

#### Installation

- use the python version above 3.10 (I am using pyton version 3.11.5)
- It is recommended that you create a virtual environment in python for this project
- I have Installed below dependencies with specified version
    - Flask : `3.0.0`
    - Flask-Cors: `4.0.0`
    - scikit-learn: `1.3.2`
    - scipy:  `1.11.4`
    - Scrapy: `2.11.1`

#### Locally Run

```
$ cd crawler
```
```
$ scrapy crawl wiki_spider
```

**Note**: You can customize the crawler in `crawler -> wiki_crawler -> spider -> wiki_spider.py`. In this file you can add the more wikipedia links to crawl and also modify the max_depth and max_page parameters
