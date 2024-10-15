import re
import requests
import csv
from PIL import Image
from io import BytesIO
from pathlib import Path
from bs4 import BeautifulSoup


site_url = "https://books.toscrape.com/"
page = requests.get(site_url)
soup = BeautifulSoup(page.content, 'html.parser')

# Extraire les URLs des catégories
categories_url={}
categories_div = soup.find('ul', class_='nav-list')  # je devrai nommer la variable categories_ul mais trop proche de categories.url je garde celle-ci
categories = categories_div.find_all('a')
for category in categories:  #stockage des url dans un dictionnaire  "nom de la catéorie" = "url de la catégorie"
    categories_url[category.getText().strip()] = site_url + category.get('href').replace("index.html","")
del categories_url["Books"]  # cette catégorie n'en est pas réellement une car regroupe tous les livres du site

#extraire tous les livres de chaque catégorie
for category in categories_url:
    # création des dossiers de stockage des éléments récupérer
    dossier = Path("data/"+category+"/images").resolve()
    dossier.mkdir(parents=True, exist_ok=True)
    url_livres = []     #initialisation de la liste qui contiendra les url de tous les livres de la catégorie

    url_base = categories_url[category]     #attribution de la premiere partie de l'URL qui contient le nom de la catégorie.
    url_page = "index.html"                 #seconde partie de l'url pour la premiere page de la catégorie.
    while True:                             # boucle tant qu'il trouve une page suivante.
        url = url_base + url_page           #reconstitution de URL en fonction de la page suiavnte trouvée.
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # extraire la liste des Urls des livres de la catégorie
        liste_livres = soup.find_all("div", class_="image_container")
        for product in liste_livres:
            liste_a = product.find("a")  # extraction des balises a
            url_livre = liste_a.get('href')  # extraction de l'url du livre
            url_livres.append(url_livre)
        page_suivante = soup.find("li", class_="next")  # recherche d'une page suivante
        if page_suivante:
            liste_a = page_suivante.find("a")  # extraction des balises a
            url_page = liste_a.get('href')  # extraction de l'url de la page
        else:
            break
    # extraire les données pour chaque livre à partir de la liste précédement établie
    book_info=[] #liste qui va contenir les différents dictionnaire des livres d'une catégorie en attendant de l'ecrire dans le cvs. le but est d'éviter l'ouverture et la fermeture du fichier pour chaque itération
    for url in url_livres:
        url_livre = "https://books.toscrape.com/catalogue/" + url.replace("../", "")
        page = requests.get(url_livre)
        soup = BeautifulSoup(page.content, "html.parser")

        # Dictionnaire pour stocker les données de chaque livre extraites
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
        if descriptions:   # Si le livre a bien une description
            data["product_description"] = descriptions[0].string  # extraction de la chaine de caractère constituant la description depuis la liste
        else:              # sinon préciser qu'il n'y a pas de description
            data["product_description"] =  "pas de description trouvée"

        # extraire la categorie

        # ul = soup.find('ul', class_="breadcrumb")  # liste des élements de la liste de l'entête
        # categories = ul.find_all("li")[2]  # récupération du troisième élement de la liste correspondant à la catégorie
        # data["product_category"] = categories.find("a").string  # extraction de la chaine de caractère constituant le nom de la catégorie et stockage

        data["product_category"] = category #ancienne recherche est obsolète car à présent, elle est déjà faites plus haut dans le code

        # extraire le review rating
        review_rating = soup.find('p', class_='star-rating')  # liste des balises <p> avec la class "star_rating"
        data["rating_value"] = review_rating.get('class')[1]  # Extraire le nombre d'étoile de la liste extraite de la classe de la balise <p>

        # extraire l'url de la cover
        div_active_item = soup.find("div", class_="item active")  # liste d'un seul élément des <div> avec la class item active
        img_tag = div_active_item.find('img')  # extraction de la balise <img>
        img_url = img_tag['src']  # extraction de l'url de la source de l'image

        # Si l'URL de l'image est relative, il faut la compléter par l'URL de base
        if img_url.startswith("../"):
            img_url = site_url + img_url.replace("../", "")

        data["image_url"] = img_url  # ajout de l'url de l'image au distionnaire.
        #extraction de l'image
        image_file=requests.get(img_url)
        image= Image.open(BytesIO(image_file.content))
        image_nom = "data/"+ category +"/images/"+re.sub(r'[\\/*?:"<>|]', ' ', data["title"])+"-"+data["UPC"]+".jpg"
        image.save(image_nom)

        book_info.append(
            [data["url product"], data["UPC"], data["title"], data["Price (incl. tax)"], data["Price (excl. tax)"],
             data["Availability"], data["product_description"], data["product_category"], data["rating_value"],
             data["image_url"]])


    # Stockage des informations dans le CSV
    # initialisation du fichier CVS avec le header
    csv_path = Path("data/"+category+"/livres_de_la_categorie_" + category + ".csv").resolve()  # création du chemin et nom du fichier CVS incluant le nom de la catégorie
    with open(csv_path, 'w', encoding='utf-8') as data_book: # création et ouverture du CSV
    # le <head> de la page web indique charset=utf-8 pour éviter un problème d'encodage du csv (le caracère # en particulier) j'ai dû repréciser
        writer = csv.writer(data_book, delimiter=",")
        writer.writerow( # mise en place du header selon les exigences du projet
        ["product_page_url", "universal_ product_code", "title", "price_including_tax", "price_excluding_tax",
         "number_available", "product_description", "category", "review_rating", "image_url"])
    #écriture des informations de book_info dans le CSV
        for row in book_info:
            writer.writerow(row)
