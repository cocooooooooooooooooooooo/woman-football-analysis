import pandas as pd
import requests
import time

# 1. L'URL de la page de l'équipe féminine de Liverpool sur FBref
url = "https://fbref.com/en/squads/822bd0ba/Liverpool-Women-Stats"

# 2. Contourner la sécurité : FBref bloque les scripts automatisés.
# On ajoute un "User-Agent" pour faire croire au site que la requête vient d'un vrai navigateur.
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

print("Connexion à FBref en cours...")
reponse = requests.get(url, headers=headers)

# 3. Pandas scanne le code HTML et extrait TOUS les tableaux de la page
tableaux = pd.read_html(reponse.text)

# 4. Le tableau des "Standard Stats" (Joueurs) est le premier de la page, donc l'index 0
stats_effectif = tableaux[0]

# 5. Nettoyage : FBref utilise des en-têtes de colonnes sur deux niveaux (MultiIndex).
# On supprime le premier niveau pour avoir des noms de colonnes simples.
stats_effectif.columns = stats_effectif.columns.droplevel(0)

# On retire la dernière ligne qui est souvent le total de l'équipe
stats_effectif = stats_effectif[stats_effectif['Player'] != 'Squad Total']

# 6. Affichage des statistiques clés (Temps de jeu, Buts, Passes décisives, xG)
colonnes_cibles = ['Player', 'Age', 'Min', 'Gls', 'Ast', 'xG']
print(f"\nDonnées récupérées pour {len(stats_effectif)} joueuses :")
print(stats_effectif[colonnes_cibles].head(10))

# Règle d'or du scraping : Toujours faire une pause pour ne pas surcharger le serveur
time.sleep(3)