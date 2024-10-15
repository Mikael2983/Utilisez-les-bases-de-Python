# Utilisez les bases de Python pour l'analyse de marché

## Description
Ce projet est une application Python conçue pour extraire les prix des livres d'occasion vendus sur le site web **Books to Scrape**. Le programme récupère les informations tarifaires au moment de l'exécution et génère un fichier contenant les prix et les titres des livres disponibles.

Ce projet est une version bêta et n'automatise pas encore la surveillance en temps réel. Cependant, il peut être exécuté à la demande pour extraire les prix actuels des livres.

## Fonctionnalités
- Extraction des titres de livres et de leurs prix sur **Books to Scrape**.
- Export des données extraites dans un fichier CSV.
- Téléchargement et enregistrement des covers.

## Prérequis
- Python 3.x
- Modules listés dans le fichier `requirements.txt`

## Installation
1. Clonez ce repository sur votre machine locale :
   ```bash
   git clone https://github.com/Mikael2983/OpenclassroomsProject2.git
  
2. Accédez au dossier du projet :
   ```bash
   cd users/Documents/projet2

3. Créez et activez un environnement virtuel (facultatif mais recommandé) :
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows : env\Scripts\activate

4. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt

5. Utilisation
  Exécutez le script principal pour récupérer les prix :
   ```bash
   python extract_data.py
