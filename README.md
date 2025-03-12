
# Data Lake Project - Installation & Deployment

## Prérequis

Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre machine :

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Git](https://git-scm.com/downloads)
- Python 3.10+ (si besoin d'exécuter des scripts en local)

## 1. Cloner le dépôt

Clonez le projet depuis le repository GitHub :

```bash
git clone https://github.com/votre-repo/datalake-project.git
cd datalake-project


## 2. Configuration des fichiers

### 2.1 `.env` (Optionnel)

Créez un fichier `.env` à la racine pour définir les variables d'environnement :

```ini
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=staging
MYSQL_PORT=3306
MONGO_URI=mongodb://mongodb:27017/
S3_ENDPOINT_URL=http://localstack:4566
```

### 2.2 `docker-compose.yml`

Assurez-vous que le fichier `docker-compose.yml` est bien configuré avec les services suivants :

```yaml
version: '3.8'
services:
  mysql:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_DATABASE=staging
    ports:
      - "3306:3306"

  mongodb:
    image: mongo
    ports:
      - "27017:27017"

  localstack:
    image: localstack/localstack
    environment:
      - SERVICES=s3
    ports:
      - "4566:4566"

  airflow:
    build:
      context: .
      dockerfile: Dockerfile.airflow
    ports:
      - "8080:8080"
    depends_on:
      - mysql
      - mongodb
      - localstack

  api:
    build:
      context: .
      dockerfile: Dockerfile.api
    ports:
      - "8000:8000"
    depends_on:
      - mysql
      - mongodb
      - localstack
```

## 3. Construire et démarrer les conteneurs

Exécutez les commandes suivantes pour **construire et démarrer** l'ensemble des services :

```bash
docker-compose up -d --build
```

Vérifiez que les conteneurs tournent bien :

```bash
docker ps
```

## 4. Initialisation de la base de données Airflow

Si nécessaire, exécutez :

```bash
docker exec -it airflow airflow db migrate
```

## 5. Déploiement du pipeline ETL

Dans l'interface **Airflow** ([http://localhost:8080](http://localhost:8080)), activez et exécutez le DAG `etl_football_pipeline`.

Ou via la commande CLI :

```bash
docker exec -it airflow airflow dags trigger etl_football_pipeline
```

## 6. Tester l'API

L'API est accessible via **FastAPI** sur [http://localhost:8000](http://localhost:8000).

### 6.1 Vérifier le statut de l'API

```bash
curl http://localhost:8000/health
```

### 6.2 Accéder aux endpoints principaux

| Endpoint   | Description                       |
| ---------- | --------------------------------- |
| `/raw`     | Liste des fichiers stockés sur S3 |
| `/staging` | Données transformées dans MySQL   |
| `/curated` | Données finales dans MongoDB      |
| `/stats`   | Statistiques générales            |
| `/health`  | Vérification des services         |

## 7. Arrêter les services

Pour arrêter tous les conteneurs :

```bash
docker-compose down
```

## 8. Dépannage

### **Problème : Airflow ne se lance pas**

Vérifiez les logs :

```bash
docker logs airflow --tail 50
```

Essayez de redémarrer Airflow :

```bash
docker-compose restart airflow
```

### **Problème : Connexion MySQL refusée**

Assurez-vous que MySQL est bien démarré :

```bash
docker-compose up -d mysql
```

Testez la connexion :

```bash
docker exec -it mysql mysql -u root -proot -e "SHOW DATABASES;"
```

### **Problème : API ne répond pas**

Vérifiez que l'API tourne bien :

```bash
docker ps | grep api
```

Si besoin, redémarrez l'API :

```bash
docker-compose restart api
```

##
