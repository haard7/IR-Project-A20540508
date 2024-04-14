## How to run

#### Crawler

1. Crawler
```
$ cd crawler
```
```
$ scrapy crawl wiki_spider
```

Note: You can customize the crawler in crawler -> wiki_crawler -> spider -> wiki_spider.py. In this file you can add the more wikipedia links to crawl and also modify the max_depth and max_page


2. Indexer

```
$ cd indexer
```
```
$ python indexer.py
```

Note: You can edit the config.json file in indexer folder to give customize query to get top-k results in console

3. Processor

```
$ cd processor
```
```
$ flask run
```
visit [http://127.0.0.1:5000](http://127.0.0.1:5000) on browser
