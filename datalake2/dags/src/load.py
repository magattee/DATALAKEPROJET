import pymongo
import mysql.connector
import os

# Détection de l'environnement Docker/Airflow
if os.getenv("AIRFLOW_HOME"):
    DB_HOST = "mysql"  # Nom du service dans Docker Compose
    MONGO_URI = "mongodb://mongodb:27017/"  # Nom du service dans Docker Compose
else:
    DB_HOST = "localhost"  # Pour exécution locale
    MONGO_URI = "mongodb://localhost:27017/"

DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "staging"
MONGO_DB = "curated"
MONGO_COLLECTION = "football_players"

# Connexion MySQL
# Connexion à MySQL
conn = mysql.connector.connect(
host=DB_HOST,
port=3306,  
user=DB_USER,
password=DB_PASSWORD,
database=DB_NAME,
auth_plugin="mysql_native_password"  # Force l'authentification
)  
cursor = conn.cursor(dictionary=True)

# Récupération des données nettoyées
cursor.execute("SELECT * FROM players")
players = cursor.fetchall()
cursor.close()
conn.close()

print(f"Nombre de joueurs récupérés depuis MySQL : {len(players)}")

# Connexion MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]
collection = db[MONGO_COLLECTION]

print("Connexion MongoDB réussie ✅")
print("Base sélectionnée :", db.name)
print("Collections existantes :", db.list_collection_names())

# Nettoyer la collection avant d'insérer de nouvelles données (optionnel)
collection.delete_many({})

# Transformation et insertion des données enrichies
for player in players:
    # Éviter une division par zéro
    #print(f"Insertion en cours pour {player['name']} ...")
    goal_per_match = round(player["goals"] / player["matches_played"], 2) if player["matches_played"] > 0 else 0
    recov_per_match = round(player["recoveries"] / player["matches_played"], 2) if player["matches_played"] > 0 else 0

    player_doc = {
        "name": player["name"],
        "nation": player["nation"],
        "position": player["position"],
        "club": player["club"],
        "competition": player["competition"],
        "age": player["age"],
        "born_year": player["born_year"],
        "matches_played": player["matches_played"],
        "goals": player["goals"],
        "assists": player["assists"],
        "recoveries": player["recoveries"],
        "goal_per_match": goal_per_match,  # Nouvelle colonne calculée
        "recov_per_match": recov_per_match  # Nouvelle colonne calculée
    }

    try:
        collection.insert_one(player_doc)
    except Exception as e:
        print(f"Erreur lors de l'insertion du joueur {player['name']} : {e}")

print(f"{len(players)} joueurs stockés dans MongoDB avec les statistiques enrichies.")
