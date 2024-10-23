import csv
from pathlib import Path
import utils


if __name__ == "__main__":

    url_site = "https://books.toscrape.com/"

    url_categories = utils.scrape_all_categories(url_site)

    for category in url_categories:
        url_books = utils.scrape_category(category,url_categories[category])
        data_book=[]
        # Initialisation du fichier CSV avec le header
        csv_path = Path("data/" + category + "/category book/" + category + ".csv").resolve()

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
                utils.save_cover_picture(data_book)
