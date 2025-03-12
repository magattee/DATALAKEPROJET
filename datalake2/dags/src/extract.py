import boto3
import os

# Détection de l'environnement (Docker/Airflow ou exécution locale)
if os.getenv("AIRFLOW_HOME"):
    S3_ENDPOINT_URL = "http://localstack:4566"  # Utilisé dans Docker
else:
    S3_ENDPOINT_URL = "http://localhost:4566"  # Utilisé en local

S3_BUCKET_RAW = "raw"
LOCAL_FILE_PATH = "/opt/airflow/dags/data/raw/2022-2023_Football_Player_Stats.csv"
S3_OBJECT_NAME = "football_stats_raw.csv"

# Création du client S3 avec des credentials fictifs
s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT_URL,
    aws_access_key_id="test",   # Valeur fictive (obligatoire pour LocalStack)
    aws_secret_access_key="test" # Valeur fictive (obligatoire pour LocalStack)
)

def create_bucket_if_not_exists(bucket_name):
    """Vérifie si le bucket existe, sinon le crée."""
    try:
        existing_buckets = [bucket['Name'] for bucket in s3.list_buckets().get('Buckets', [])]
        if bucket_name not in existing_buckets:
            print(f"📌 Bucket '{bucket_name}' introuvable. Création en cours...")
            s3.create_bucket(Bucket=bucket_name)
            print(f"✅ Bucket '{bucket_name}' créé avec succès.")
        else:
            print(f"✅ Bucket '{bucket_name}' déjà existant.")
    except Exception as e:
        print(f"❌ Erreur lors de la vérification/création du bucket : {e}")

def upload_to_s3():
    """Charge le fichier CSV dans le bucket S3 (LocalStack)"""
    if not os.path.exists(LOCAL_FILE_PATH):
        print(f"❌ Erreur : Fichier {LOCAL_FILE_PATH} non trouvé.")
        return

    # Vérifier et créer le bucket si nécessaire
    create_bucket_if_not_exists(S3_BUCKET_RAW)

    # Envoi du fichier vers S3
    try:
        s3.upload_file(LOCAL_FILE_PATH, S3_BUCKET_RAW, S3_OBJECT_NAME)
        print(f"✅ Fichier {LOCAL_FILE_PATH} chargé sur S3 dans {S3_BUCKET_RAW}/{S3_OBJECT_NAME}")
    except Exception as e:
        print(f"❌ Erreur lors de l'upload du fichier : {e}")

if __name__ == "__main__":
    upload_to_s3()
