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
git clone https://github.com/magattee/DATALAKEPROJET.git
cd datalake2
```

---

## **3. Configuration**

```ini
pip install -r requirements.txt
```
---

## **Lancer les services Docker**
```bash
docker-compose up -d --build
```
Vérifier que tous les conteneurs sont démarrés :
```bash
docker ps
```
### Vérifier
S’assurer que les services suivants sont bien définis :
- **MySQL** (stockage des données intermédiaires)
- **MongoDB** (stockage des données finales)
- **LocalStack** (simule AWS S3)
- **Airflow** (orchestration ETL)
- **API FastAPI** (exposition des données)
---

## **acceder Airflow**

```bash
docker exec -it airflow airflow users create --username admin --password admin --firstname Admin --lastname User --role Admin --email admin@example.com
```
Accéder à l’interface Airflow : [http://localhost:8080](http://localhost:8080)
et tester la pipeline ETL

---

## ** Exécuter le pipeline ETL**
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
Accéder aux données exemple:
```bash
curl http://localhost:8000/staging
curl http://localhost:8000/curated
```
Documentation interactive : [http://localhost:8000/docs](http://localhost:8000/docs)

---
