import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exceptions import CloseSpider
from urllib.parse import urlparse, unquote


class WikiSpider(scrapy.Spider):
    name = "wiki_spider"
    allowed_domains = ["en.wikipedia.org", "simple.wikipedia.org"]
    start_urls = [
        "https://en.wikipedia.org/wiki/Renewable_energy_in_the_United_States",
        "https://en.wikipedia.org/wiki/List_of_renewable_energy_topics_by_country_and_territory",
        "https://simple.wikipedia.org/wiki/Renewable_energy",
        "https://en.wikipedia.org/wiki/List_of_books_about_renewable_energy",
        "https://en.wikipedia.org/wiki/Renewable_energy_in_the_United_Kingdom",
        "https://en.wikipedia.org/wiki/Solar_power",
        "https://en.wikipedia.org/wiki/Wind_power",
        "https://en.wikipedia.org/wiki/Bioenergy",
        "https://en.wikipedia.org/wiki/Geothermal_energy",
        "https://en.wikipedia.org/wiki/Hydropower",
        "https://en.wikipedia.org/wiki/Future_Energy",
        "https://en.wikipedia.org/wiki/Energy_development",
        "https://en.wikipedia.org/wiki/Sustainable_energy",
        "https://en.wikipedia.org/wiki/UN-Energy",
        "https://en.wikipedia.org/wiki/World_energy_supply_and_consumption",
    ]
    max_depth = 2
    max_pages = 20

    custom_settings = {
        "DEPTH_LIMIT": max_depth,
        "CLOSESPIDER_PAGECOUNT": max_pages,
    }

    def parse(self, response):
        # Generate a filename from the URL
        parsed_url = urlparse(response.url)
        page_title = parsed_url.path.split("/")[-1]
        filename = f"data/{unquote(page_title)}.html"

        # Save the raw HTML content to an HTML file
        with open(filename, "wb") as file:
            file.write(response.body)

        # Follow links to next pages, within allowed_domains
        for next_page in response.css("a::attr(href)"):
            if next_page is not None:
                yield response.follow(next_page, self.parse)


# To run the spider without a project (script way)
if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(WikiSpider)
    process.start()
