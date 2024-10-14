import re
import requests
import csv
from bs4 import BeautifulSoup
from pathlib import Path

csv_path = Path("data/data_one_category.csv").resolve()
url_base = "https://books.toscrape.com/catalogue/category/books/sequential-art_5/"
url_page = "index.html"
url_site = "http://books.toscrape.com/"
url_livres = []
data_book = open(csv_path,'w',encoding='utf-8')
#le <head> de la page indique charset=utf-8 pour éviter un problème d'encodage du csv (le caracère #) j'ai dû repréciser
#initialisation du fichier CVS avec le header
writer = csv.writer(data_book, delimiter=",")
writer.writerow(["product_page_url", "universal_ product_code", "title", "price_including_tax", "price_excluding_tax",
          "number_available", "product_description", "category", "review_rating", "image_url"])

while True :
    url = url_base + url_page
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # extraire la liste des Urls des livres de la catégorie
    liste_livres = soup.find_all("div", class_="image_container")

    for product in liste_livres:
        liste_a = product.find("a")  # extraction des balises a
        url_livre = liste_a.get('href')  # extraction de l'url du livre
        url_livres.append(url_livre)
    page_suivante = soup.find("li", class_="next")      #recherche d'une page suivante
    if page_suivante:
        liste_a= page_suivante.find("a")  #extraction des balises a
        url_page = liste_a.get('href') # extraction de l'url de la page
    else:
        break

for url in url_livres :
    url_livre = "https://books.toscrape.com/catalogue/"+ url.replace("../", "")
    page = requests.get(url_livre)
    soup = BeautifulSoup(page.content, "html.parser")

    # Dictionnaire pour stocker les données extraites
    data = {}
    data["url product"] = url_livre

    # extraction du titre
    producttitle = soup.find_all("div", class_="col-sm-6 product_main")  # liste d'un seul élément des <div> avec la class col-sm-6 product_main
    data["title"] = producttitle[0].h1.string  # extraction de la chaine de caractère constituant le titre

    # extraire les valeurs de la table
    rows = soup.find_all('tr')
    # Boucle pour extraire les paires clé-valeur (th et td)
    for row in rows:
        key = row.find('th').string  # Extraire le texte de l'élément <th>
        value = row.find('td').string  # Extraire le texte de l'élément <td>
        data[key] = value  # création du dictionnaire

    # extraction du nombre d'exemplaire disponible
    nombre_dispo = re.search(r'\d+', data["Availability"])  # rechercher un ou plusieurs chiffres (\d+) dans la chaîne de caractère

    if nombre_dispo:  # Stocker le résultat si un nombre est trouvé
        data["Availability"] = nombre_dispo.group()

    # extraire la description
    descriptions = soup.find_all("p", class_="")  # liste des <p> sans class ( 1 seul sur la page du livre)
    data["product_description"] = descriptions[0].string  # extraction de la chaine de caractère constituant la description depuis la liste

    # extraire la categorie
    ul = soup.find('ul', class_="breadcrumb")  # liste des élements de la liste de l'entête
    categories = ul.find_all("li")[2]  # récupération du troisième élement de la liste correspondant à la catégorie
    data["product_category"] = categories.find("a").string  # extraction de la chaine de caractère constituant le nom de la catégorie et stockage

    # extraire le review rating
    review_rating = soup.find('p', class_='star-rating')  # liste des <p> avec la class "star_rating"
    data["rating_value"] = review_rating.get('class')[1]  # Extraire le nombre d'étoile de la liste extraite de la classe de la balise <p>

    # extraire l'url de la cover
    div_active_item = soup.find("div", class_="item active")  # liste d'un seul élément des <div> avec la class item active
    img_tag = div_active_item.find('img')  # extraction de la balise <img>
    img_url = img_tag['src']  # extraction de l'url de la source de l'image

    # Si l'URL de l'image est relative, il faut la compléter par l'URL de base

    if img_url.startswith("../"):
      img_url = url_site + img_url.replace("../", "")

    data["image_url"] = img_url  # ajout de l'url de l'image au distionnaire.

    # Stockage des informations dans le CSV
    writer.writerow([data["url product"], data["UPC"], data["title"], data["Price (incl. tax)"], data["Price (excl. tax)"],
         data["Availability"], data["product_description"], data["product_category"], data["rating_value"],
         data["image_url"]])

data_book.close()