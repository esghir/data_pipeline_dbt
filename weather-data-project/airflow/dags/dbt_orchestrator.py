from airflow import DAG
import sys
from airflow.operators.python import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime, timedelta
from docker.types import Mount


default_args = {
    'description': 'A Dag to orchestrate weather data processing',
    'start_date': datetime(2025, 8, 14),
    'catchup': False,
}

dag = DAG(
    dag_id="weather_dbt_orchestrator",
    default_args=default_args,
    schedule=timedelta(minutes=5)
)

with dag:
    task2= DockerOperator(
        task_id="Transform_data_task",
        image="ghcr.io/dbt-labs/dbt-postgres:1.9.latest",  # Replace with your actual dbt image
        command='run',
        working_dir="/usr/app",  # Replace with your actual dbt project directory
        mounts=[
            Mount(
                source="/home/amine/data_pipeline_dbt/weather-data-project/dbt/my_project",  # Replace with your actual dbt project directory
                target="/usr/app",
                type="bind"
            ),
            Mount(
                source="/home/amine/data_pipeline_dbt/weather-data-project/dbt/profiles.yml",  # Replace with your actual target directory
                target="/root/.dbt/profiles.yml",
                type="bind"
            )
        ],
        network_mode="weather-data-project_my_network",
        docker_url="unix://var/run/docker.sock",  # Ensure this matches your Docker setup
        auto_remove='success',
    )