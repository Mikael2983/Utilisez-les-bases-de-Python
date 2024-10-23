import csv
from pathlib import Path
import utils


if __name__ == "__main__":

    url_site = "https://books.toscrape.com/"

    url_categories = utils.scrape_all_categories(url_site)

    for category in url_categories:
        url_books = utils.scrape_category(category,url_categories[category])
        utils.write_data_on_csv(url_books,category)


