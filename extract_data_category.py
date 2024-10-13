import re
import requests
import csv
from bs4 import BeautifulSoup

csv_path = "C:/Users/mikae/Documents/formation/Project2/data_one_category.csv"
url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

#extraire la lsite des Url des livres de la catégorie
url_livres=[]
liste_livres = soup.find_all("div", class_="image_container")

for product in liste_livres:
    liste_a= product.find("a")  #extraction des balises a
    url_livre = liste_a.get('href') # extraction de l'url du livre
    url_livres.append(url_livre)


print(url_livres)

# # Si l'URL de l'image est relative, il faut la compléter par l'URL de base
# base_url = "http://books.toscrape.com/"
# if img_url.startswith("../"):
#     img_url = base_url + img_url.replace("../", "")
# print(livres)
