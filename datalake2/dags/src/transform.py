import pandas as pd
import mysql.connector
import os
import boto3
from io import StringIO


# Détecter si on tourne dans Docker (Airflow)
if os.getenv("AIRFLOW_HOME"):
    S3_ENDPOINT_URL = "http://localstack:4566"  # Pour exécution depuis Airflow
else:
    S3_ENDPOINT_URL = "http://localhost:4566"  # Pour exécution locale

S3_BUCKET_RAW = "raw"
S3_OBJECT_NAME = "football_stats_raw.csv"
DB_HOST = "mysql"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "staging"

# Configure boto3 to use LocalStack
s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
)

def fetch_s3_file():
    """Télécharge le fichier brut depuis S3 et charge en mémoire"""
    response = s3.get_object(Bucket=S3_BUCKET_RAW, Key=S3_OBJECT_NAME)
    return pd.read_csv(StringIO(response["Body"].read().decode('ISO-8859-1')), delimiter=";")

def clean_and_store():
    """Nettoie les données, supprime les doublons et insère dans MySQL"""
    df = fetch_s3_file()

    # Renommer les colonnes pour une meilleure lisibilité
    df = df.rename(columns={
        "Player": "name",
        "Nation": "nation",
        "Pos": "position",
        "Squad": "club",
        "Comp": "competition",
        "Age": "age",
        "Born": "born_year",
        "MP": "matches_played",
        "Starts": "starts",
        "Min": "minutes_played",
        "90s": "nineties_played",
        "Goals": "goals",
        "Assists": "assists",
        "PasTotCmp": "passes_completed",
        "PasTotAtt": "passes_attempted",
        "PasTotCmp%": "pass_accuracy",
        "Tkl": "tackles",
        "Int": "interceptions",
        "Clr": "clearances",
        "Recov": "recoveries",
        "CrdY": "yellow_cards",
        "CrdR": "red_cards",
    })

    # Suppression des valeurs nulles
    df = df.dropna()

    # Suppression des doublons en gardant la **dernière occurrence**
    df = df.drop_duplicates(subset=["name", "age", "nation"], keep="last")

    conn = mysql.connector.connect(
    host="mysql",  # Docker service name
    port=3306,  # Port MySQL interne dans Docker
    user="root",
    password="root",
    database="staging",
    auth_plugin="mysql_native_password"
)



    cursor = conn.cursor()

    # Création de la table avec les nouvelles colonnes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            nation VARCHAR(50),
            position VARCHAR(10),
            club VARCHAR(100),
            competition VARCHAR(100),
            age INT,
            born_year INT,
            matches_played INT,
            starts INT,
            minutes_played INT,
            nineties_played FLOAT,
            goals INT,
            assists INT,
            passes_completed INT,
            passes_attempted INT,
            pass_accuracy FLOAT,
            tackles INT,
            interceptions INT,
            clearances INT,
            recoveries INT,
            yellow_cards INT,
            red_cards INT
        )
    """)

    cursor.execute("TRUNCATE TABLE players")

    # Insertion des données dans MySQL
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO players (name, nation, position, club, competition, age, born_year, 
                                 matches_played, starts, minutes_played, nineties_played, goals, assists,
                                 passes_completed, passes_attempted, pass_accuracy, tackles, interceptions,
                                 clearances, recoveries, yellow_cards, red_cards)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row["name"], row["nation"], row["position"], row["club"], row["competition"],
            row["age"], row["born_year"], row["matches_played"], row["starts"], row["minutes_played"],
            row["nineties_played"], row["goals"], row["assists"], row["passes_completed"], 
            row["passes_attempted"], row["pass_accuracy"], row["tackles"], row["interceptions"],
            row["clearances"], row["recoveries"], row["yellow_cards"], row["red_cards"]
        ))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"{len(df)} joueurs insérés dans MySQL (staging) après suppression des doublons et mise à jour de la syntaxe(encodage).")

if __name__ == "__main__":
    clean_and_store()