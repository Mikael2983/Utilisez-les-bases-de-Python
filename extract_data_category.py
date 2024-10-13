import re
import requests
import csv
from bs4 import BeautifulSoup

csv_path = "C:/Users/mikae/Documents/formation/Project2/data_one_category.csv"
url_base = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"

# Crétion de la liste des urls des pages de la catégorie
url_pages = ["index.html"]
url=url_base+url_pages[0]
url_livres = []

while True :
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # extraire la lsite des Url des livres de la catégorie
    liste_livres = soup.find_all("div", class_="image_container")
    for product in liste_livres:
        liste_a = product.find("a")  # extraction des balises a
        url_livre = liste_a.get('href')  # extraction de l'url du livre
        url_livres.append(url_livre)
    page_suivante = soup.find("li", class_="next")      #recherche d'une page suivante
    if page_suivante:
        liste_a= page_suivante.find("a")  #extraction des balises a
        url_page = liste_a.get('href') # extraction de l'url de la page
        url=url_base+url_page   #attribution de la nouvelle url
    else:
        break

print(url_livres)
print(len(url_livres))








# # Si l'URL de l'image est relative, il faut la compléter par l'URL de base
# base_url = "http://books.toscrape.com/"
# if img_url.startswith("../"):
#     img_url = base_url + img_url.replace("../", "")
# print(livres)
