# DATALAKEPROJET

🔌 4. Tester l’API
📜 4.1 Accéder à la documentation API (Swagger UI)
🔗 http://localhost:8000/docs

🔍 4.2 Tester les endpoints
📂 Voir les fichiers bruts sur S3

bash
Toujours afficher les détails

Copier
curl http://localhost:8000/raw
🛢 Voir les joueurs depuis MySQL

bash
Toujours afficher les détails

Copier
curl http://localhost:8000/staging
🔍 Voir les joueurs depuis MongoDB

bash
Toujours afficher les détails

Copier
curl http://localhost:8000/curated
📊 Voir les statistiques des bases

bash
Toujours afficher les détails

Copier
curl http://localhost:8000/stats
🩺 Vérifier le statut des services

bash
Toujours afficher les détails

Copier
curl http://localhost:8000/health
🛑 5. Arrêter le projet
Si vous souhaitez arrêter les services, utilisez :

bash
Toujours afficher les détails

Copier
docker-compose down
📌 Optionnel : Supprimer tous les volumes associés

bash
Toujours afficher les détails

Copier
docker-compose down -v
🎯 6. Prochaines Améliorations
 Automatiser le déclenchement du pipeline à l’arrivée de nouveaux fichiers.
 Ajouter des analyses avancées et dashboards.
 Déployer sur un cloud réel (AWS S3, RDS, MongoDB Atlas).
 Sécuriser l’API avec une authentification.
