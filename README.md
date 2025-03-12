# **Guide d'Installation et de Déploiement**

## **1. Prérequis**
Avant de commencer, assurez-vous d’avoir installé :
- **Docker** et **Docker Compose**
- **Git**
- **Python 3.10**
- **Pip et virtualenv** (si exécution locale de l'API)

---

## **2. Cloner le projet**
```bash
git clone https://github.com/votre-repo/datalake-project.git
cd datalake-project
```

---

## **3. Configuration des services**

### **3.1 Configuration des variables d’environnement**
Créer un fichier `.env` à la racine du projet avec :
```ini
MYSQL_HOST=mysql
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=staging
MYSQL_PORT=3306
MONGO_URI=mongodb://mongodb:27017/
S3_ENDPOINT_URL=http://localstack:4566
```

### **3.2 Vérifier `docker-compose.yml`**
S’assurer que les services suivants sont bien définis :
- **MySQL** (stockage des données intermédiaires)
- **MongoDB** (stockage des données finales)
- **LocalStack** (simule AWS S3)
- **Airflow** (orchestration ETL)
- **API FastAPI** (exposition des données)

---

## **4. Lancer les services Docker**
```bash
docker-compose up -d --build
```
Vérifier que tous les conteneurs sont démarrés :
```bash
docker ps
```

---

## **5. Initialiser Airflow**
```bash
docker exec -it airflow airflow db migrate
docker exec -it airflow airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```
Accéder à l’interface Airflow : [http://localhost:8080](http://localhost:8080)

---

## **6. Exécuter le pipeline ETL**
Déclencher manuellement l’ETL via Airflow :
```bash
docker exec -it airflow airflow dags trigger etl_football_pipeline
```
Vérifier les logs :
```bash
docker exec -it airflow airflow tasks logs etl_football_pipeline extract_data
```

---

## **7. Tester l'API**
L’API est accessible sur : [http://localhost:8000](http://localhost:8000)

### **7.1 Tester les endpoints**
Vérification du statut des services :
```bash
curl http://localhost:8000/health
```
Accéder aux données :
```bash
curl http://localhost:8000/staging
curl http://localhost:8000/curated
```
Documentation interactive : [http://localhost:8000/docs](http://localhost:8000/docs)

---

## **8. Arrêter et nettoyer le projet**
```bash
docker-compose down
```
Supprimer les volumes de données :
```bash
docker volume rm $(docker volume ls -q)
```

---

## **9. Déploiement sur un serveur distant**
- **Option 1 : Déploiement Docker sur un serveur distant**
  - Copier les fichiers via `scp`
  - Lancer `docker-compose up -d --build`

- **Option 2 : Utilisation de Kubernetes**
  - Adapter les configurations à `Helm` ou `Kustomize`

---

## **10. Prochaines étapes**
- **Ajouter une CI/CD avec GitHub Actions**
- **Déployer sur AWS/GCP**
- **Optimiser les performances ETL**

Le projet est maintenant opérationnel.
