import requests
import csv
from bs4 import BeautifulSoup

csv_path = "C:/Users/mikae/Documents/formation/Project2/sample.csv"
url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# Dictionnaire pour stocker les données extraites
data = {}
data["url product"]=url

#extraction du titre
producttitle = soup.find_all("div", class_="col-sm-6 product_main") #liste d'un seul élément des <div> avec la class col-sm-6 product_main
data["title"] = producttitle[0].h1.string       #extraction de la chaine de caractère constituant le titre

#extraire les valeurs de la table
rows = soup.find_all('tr')
# Boucle pour extraire les paires clé-valeur (th et td)
for row in rows:
    key = row.find('th').string  # Extraire le texte de l'élément <th>
    value = row.find('td').string  # Extraire le texte de l'élément <td>
    data[key] = value #création du dictionnaire

#extraire la description
descriptions = soup.find_all("p", class_="")    # liste des <p> sans class ( 1 seul sur la page du livre)
data["product_description"] = descriptions[0].string    # extraction de la chaine de caractère constituant la description depuis la liste

#extraire la categorie
ul = soup.find('ul', class_="breadcrumb")   #liste des élements de la liste de l'entête
categories = ul.find_all("li")[2]                 # récupération du troisième élement de la liste correspondant à la catégorie
data["product_category"] = categories.find("a").string     # extraction de la chaine de caractère constituant le nom de la catégorie et stockage

#extraire le review rating
review_rating = soup.find('p', class_='star-rating') # liste des <p> avec la class "star_rating"
data["rating_value"] = review_rating.get('class')[1] # Extraire le nombre d'étoile de la liste extraite de la classe de la balise <p>



#extraire l'url de la cover
div_active_item = soup.find("div", class_="item active")  #liste d'un seul élément des <div> avec la class item active
img_tag = div_active_item.find('img')       # extraction de la balise <img>
img_url = img_tag['src']                    # extraction de l'url de la source de l'image

# Si l'URL de l'image est relative, il faut la compléter par l'URL de base
base_url = "http://books.toscrape.com/"
if img_url.startswith("../"):
    img_url = base_url + img_url.replace("../", "")

data["image_url"] = img_url  #ajout de l'url de l'image au distionnaire.


# Afficher les données extraites
for key, value in data.items():
    print(f'{key}: {value}')

#Stockage des informations dans le CSV
header = ["product_page_url","universal_ product_code","title","price_including_tax","price_excluding_tax",
              "number_available","product_description","category","review_rating","image_url"]
with open(csv_path, "w") as data_book:
   writer = csv.writer(data_book, delimiter=",")
   writer.writerow(header)
   writer.writerow([data["url product"],data["UPC"],data["title"],data["Price (incl. tax)"],data["Price (excl. tax)"],
                    data["Availability"],data["product_description"],data["product_category"],data["rating_value"],data["image_url"]])
