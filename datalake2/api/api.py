from fastapi import FastAPI
import pymysql
import pymongo
import boto3
import os

app = FastAPI()

# 🛢 Configuration MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root")
MYSQL_DB = os.getenv("MYSQL_DB", "staging")
MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))

# 🔍 Configuration MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/")
mongo_client = pymongo.MongoClient(MONGO_URI)
mongo_db = mongo_client["curated"]
mongo_collection = mongo_db["football_players"]

# 📂 Configuration S3 (LocalStack)
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", "http://localstack:4566")
s3_client = boto3.client("s3", endpoint_url=S3_ENDPOINT_URL)
S3_BUCKET_RAW = "raw"

# ✅ Fonction de connexion MySQL
def get_mysql_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        port=MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

# 📂 Endpoint `/raw` → Récupérer les fichiers S3
@app.get("/raw")
def get_raw_data():
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_RAW)
        files = [obj["Key"] for obj in response.get("Contents", [])]
        return {"status": "success", "files": files}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 🛢 Endpoint `/staging` → Récupérer les joueurs depuis MySQL
@app.get("/staging")
def get_players_mysql():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players LIMIT 20;")
        players = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"status": "success", "players": players}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 🔍 Endpoint `/curated` → Récupérer les joueurs depuis MongoDB
@app.get("/curated")
def get_players_mongodb():
    try:
        players = list(mongo_collection.find({}, {"_id": 0}).limit(20))
        return {"status": "success", "players": players}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 🩺 Endpoint `/health` → Vérifier l'état des services
@app.get("/health")
def health_check():
    return {"status": "ok", "services": ["S3", "MySQL", "MongoDB"]}

# 📊 Endpoint `/stats` → Récupérer des métriques
@app.get("/stats")
def get_stats():
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM players;")
        total_players = cursor.fetchone()["total"]
        cursor.close()
        conn.close()

        mongo_count = mongo_collection.count_documents({})

        return {
            "status": "success",
            "mysql_players": total_players,
            "mongodb_players": mongo_count,
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
