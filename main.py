import re
import requests
import csv
from PIL import Image
from io import BytesIO
from pathlib import Path
from bs4 import BeautifulSoup
import utils


if __name__ == __main__:

    url_site = "https://books.toscrape.com/"

    url_categories = utils.scrape_all_categories(url_site)

    for category in url_categories:
        url_books = utils.scrape_category(category,url_categories[category])
        data_book=[]
        # Initialisation du fichier CSV avec le header
        csv_path = Path("data/" + category + "/livres_de_la_categorie_" + category + ".csv").resolve()

        with open(csv_path, 'w', encoding='utf-8', newline='') as backup_file:
            writer = csv.writer(backup_file, delimiter=",")
            writer.writerow(
                ["product_page_url", "universal_product_code", "title", "price_including_tax", "price_excluding_tax",
                 "number_available", "product_description", "category", "review_rating", "image_url"])

            for  url_book in url_books:
                data_book = utils.scrape_book_data(url_book)
                writer.writerow(
                    [data_book["url product"], data_book["UPC"], data_book["title"], data_book["Price (incl. tax)"],
                     data_book["Price (excl. tax)"], data_book["Availability"], data_book["product_description"],
                     data_book["product_category"], data_book["rating_value"],data_book["image_url"]])

                image_file = requests.get(data_book["image_url"])
                image= Image.open(BytesIO(image_file.content))
                image_name = "data/"+ category +"/images/"+re.sub(r'[\\/*?:"<>|]', ' ', data_book["title"])+"-"+data_book["UPC"]+".jpg"
                image.save(image_name)