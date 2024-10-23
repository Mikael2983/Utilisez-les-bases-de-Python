import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def scrape_book_data(book_url):
    # Dictionnaire pour stocker les données extraites
    data = {}

    data["url product"] = "https://books.toscrape.com/catalogue/" + book_url.replace("../", "")

    page = requests.get(data["url product"])
    soup = BeautifulSoup(page.content, "html.parser")

    # extraction du titre
    product_title = soup.find_all("div", class_="col-sm-6 product_main")  # liste d'un seul élément des <div> avec la class col-sm-6 product_main
    data["title"] = product_title[0].h1.string  # extraction de la chaine de caractère constituant le titre

    # extraire les valeurs ( UPC, price_includingTax, price_excludingTax, Availability)  de la table
    rows = soup.find_all('tr')
    # Boucle pour extraire les paires clé-valeur (th et td)
    for row in rows:
        key = row.find('th').string  # Extraire le texte de l'élément <th>
        value = row.find('td').string  # Extraire le texte de l'élément <td>
        data[key] = value  # stockage dans le dictionnaire


    # extraire la description
    descriptions = soup.find_all("p", class_="")  # liste des <p> sans class ( 1 seul sur la page du livre)
    if descriptions:
        data["product_description"] = descriptions[0].string  # extraction de la chaine de caractère constituant la description depuis la liste
    else:
        data["product_description"] = "no description"

    # extraire la categorie
    ul = soup.find('ul', class_="breadcrumb")  # liste des élements de la liste de l'entête
    categories = ul.find_all("li")[2]  # récupération du troisième élement de la liste correspondant à la catégorie
    data["product_category"] = categories.find("a").string  # extraction de la chaine de caractère constituant le nom de la catégorie et stockage

    # extraire le review_rating
    review_rating = soup.find('p', class_='star-rating')  # liste des <p> avec la class "star_rating"

    # extraire l'url de l'image de la couverture
    img_tag = soup.find('img')  # extraction de la balise <img>
    img_url = img_tag['src']  # extraction de l'url de la source de l'image

    # Si l'URL de l'image est relative, il faut la compléter par l'URL du site
    url_site = "http://books.toscrape.com/"
    if img_url.startswith("../"):
        img_url = url_site + img_url.replace("../", "")

    data["image_url"] = img_url  # ajout de l'url de l'image au distionnaire.

    # transformer le review rating
    rating = {
        'Zero': 0,
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    data["rating_value"] = rating[
        review_rating.get('class')[1]
    ]
    # transformer du nombre d'exemplaire disponible

    available_quantity = re.search(r'\d+', data[
        "Availability"])  # rechercher un ou plusieurs chiffres (\d+) dans la chaîne de caractère

    if available_quantity:  # Stocker le résultat si un nombre est trouvé
        data["Availability"] = available_quantity.group()

    return data

# scraper une catégorie

def scrape_category(category,url_category):
    # pour suivre l'avancement lors de l'exécution du programme
    print("la catégorie " + category + " est en cours de traitement")
    # création des dossiers de stockage des éléments récupérés
    repertory = Path("data/" + category + "/images").resolve()
    repertory.mkdir(parents=True, exist_ok=True)
    url_books = []  # initialisation de la liste qui contiendra les url de tous les livres de la catégorie
    page_next = "index.html"  # seconde partie de l'url pour la premiere page de la catégorie.
    page = requests.get(url_category+page_next)
    soup = BeautifulSoup(page.content, "html.parser")
    page_number_li = soup.find("li", class_="current")
    if page_number_li:
        page_number = page_number_li.get_text(strip=True).split(" ")[-1]
    else:
        page_number = "1"

    for i in range(0, int(page_number)):
        url = url_category + page_next  # reconstitution de URL en fonction de la page suivante trouvée.
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # extraire la liste des Urls des livres de la catégorie
        list_books = soup.find_all("div", class_="image_container")
        for product in list_books:
            list_a = product.find("a")  # extraction des balises a
            url_book = list_a.get('href')  # extraction de l'url du livre
            url_books.append(url_book)

        page_next = "page-" + str(2+i) + ".html"  # affichage de la page suivante

    return url_books


# scraper les données de toutes les catégories
def scrape_all_categories(site_url):
    url_categories = {}
    page = requests.get(site_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    categories_div = soup.find('ul',
                               class_='nav-list')  # je devrai nommer la variable categories_ul mais trop proche de categories.url je garde celle-ci
    categories = categories_div.find_all('a')
    for category in categories:  # stockage des url dans un dictionnaire  "nom de la catéorie" = "url de la catégorie"
        url_categories[category.getText().strip()] = site_url + category.get('href').replace("index.html", "")
    del url_categories["Books"]  # cette catégorie n'en est pas réellement une car regroupe tous les livres du site

    return url_categories

#télécharger et enregistrer l'image de la couverture d'un livre
def save_cover_picture(data_book):
    picture_file = requests.get(data_book["image_url"])
    picture = Image.open(BytesIO(picture_file.content))
    picture_name = ("data/" + data_book["product_category"] + "/images/" + re.sub(r'[\\/*?:"<>|]', ' ', data_book["title"]) + "-" +
                    data_book["UPC"] + ".jpg")
    picture.save(picture_name)