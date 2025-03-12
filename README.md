# DATALAKEPROJET

Data Lake avec Airflow, MySQL, MongoDB et FastAPI
Ce projet met en place un Data Lake avec un pipeline ETL automatisé sous Airflow et une API FastAPI permettant d’exposer les données. Il utilise Docker pour la conteneurisation.

1️  Prérequis
Avant d'installer et de lancer le projet, assure-toi d'avoir :

Docker (Installer Docker)
Docker Compose (Installer Docker Compose)
Git (Installer Git)
Python 3.10+ (Si besoin de tester localement)
2️ Cloner le projet
Clone le dépôt contenant l'ensemble des fichiers nécessaires :

bash
Copier
Modifier
git clone https://github.com/ton-projet/data-lake.git
cd data-lake
3️ Démarrer les services
Lance tous les conteneurs en une seule commande :

bash
Copier
Modifier
docker-compose up -d --build
  Services lancés :

Service	Port	Description
Airflow Web UI	8080	Interface de gestion des pipelines
MySQL	3306	Base de données relationnelle
MongoDB	27017	Base de données NoSQL
LocalStack (S3)	4566	Simule AWS S3 en local
FastAPI API	8000	API d’accès aux données
4️  Vérifier que les services tournent
Liste les conteneurs actifs :

bash
Copier
Modifier
docker ps
✅ Tous les services doivent être UP.

5️  Orchestration ETL avec Airflow
🛠 Initialiser la base Airflow
Si c'est la première exécution :

bash
Copier
Modifier
docker exec -it airflow airflow db migrate
docker exec -it airflow airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
🚀 Déclencher le pipeline Airflow
bash
Copier
Modifier
docker exec -it airflow airflow dags trigger etl_football_pipeline
🖥 Accéder à l’interface Airflow
http://localhost:8080

User : admin
Password : admin
6️  Tester l'API
📂 Endpoints disponibles
Endpoint	Méthode	Description
/raw	GET	Récupérer les fichiers bruts sur S3
/staging	GET	Récupérer les données MySQL
/curated	GET	Récupérer les données enrichies MongoDB
/stats	GET	Voir les statistiques générales
/health	GET	Vérifier le statut des services
🔗 Accéder à l'API
Swagger UI : http://localhost:8000/docs
Tester une requête :

bash
Copier
Modifier
curl http://localhost:8000/health
7️  Arrêter les services
Pour arrêter tous les conteneurs sans les supprimer :

bash
Copier
Modifier
docker-compose stop
Pour les arrêter et les supprimer :

bash
Copier
Modifier
docker-compose down
8️  Nettoyage des volumes Docker
Si besoin de supprimer toutes les données persistantes :

bash
Copier
Modifier
docker volume prune
