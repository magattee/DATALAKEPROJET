from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import subprocess

# Fonction pour exécuter un script Python
def run_script(script_path):
    subprocess.run(["python", script_path], check=True)

# Définition des paramètres du DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 11),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    "football_data_pipeline",
    default_args=default_args,
    description="Pipeline Data Lake Football avec Airflow",
    schedule_interval=None,  # Manuelle pour l'instant
    catchup=False,
)

# Tâches Airflow
extract_task = PythonOperator(
    task_id="extract",
    python_callable=lambda: run_script("/opt/airflow/dags/src/extract.py"),
    dag=dag,
)

transform_task = PythonOperator(
    task_id="transform",
    python_callable=lambda: run_script("/opt/airflow/dags/src/transform.py"),
    dag=dag,
)

load_task = PythonOperator(
    task_id="load",
    python_callable=lambda: run_script("/opt/airflow/dags/src/load.py"),
    dag=dag,
)

# Définition de l'ordre d'exécution
extract_task >> transform_task >> load_task
