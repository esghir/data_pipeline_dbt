# End-to-End Weather Data Pipeline Project

This project demonstrates a complete, automated ELT (Extract, Load, Transform) data pipeline built with modern data engineering tools. It ingests real-time weather data from a public API, orchestrates the workflow with **Apache Airflow**, stores the data in **PostgreSQL**, transforms it with **dbt**, and visualizes it with **Apache Superset**. The entire environment is containerized with **Docker** for portability and ease of development.



## 🏛️ Project Architecture

The pipeline follows a modern ELT approach where raw data is first loaded into the database and then transformed in place.

`[Weatherstack API] -> [Airflow (Python Operator)] -> [PostgreSQL (Raw Schema)] -> [dbt (Transformation)] -> [PostgreSQL (Analytics Schema)] -> [Superset (Dashboard)]`

---
## 🛠️ Technologies Used

* **Orchestration:** Apache Airflow
* **Containerization:** Docker, Docker Compose
* **Database:** PostgreSQL
* **Transformation:** dbt (data build tool)
* **Data Visualization & BI:** Apache Superset
* **Core Language:** Python, SQL

---
## ⚙️ Project Components

* **Apache Airflow**: Orchestrates the entire pipeline. A primary DAG schedules and triggers the data ingestion and transformation tasks in the correct order and handles failures.
* **PostgreSQL**: Acts as the central data warehouse. It is used to store both the raw, unprocessed data and the final, transformed analytical tables.
* **dbt (Data Build Tool)**: Manages the "Transform" step of the pipeline. It takes the raw data loaded by the Python script and transforms it into clean, tested, and analytics-ready data models.
* **Apache Superset**: Serves as the business intelligence layer. It connects directly to the PostgreSQL database to create interactive dashboards and charts for data exploration.
* **API Request Module**: A set of Python scripts responsible for fetching data from the Weatherstack API and loading it into PostgreSQL. Includes a mock function for testing without making live API calls.

---
## 🗄️ PostgreSQL Database Usage

Although we are running a single PostgreSQL container instance, it serves as a backend for multiple applications, each with its own isolated database. This is a common and efficient pattern. In this project, we use **three distinct databases** within the single PostgreSQL instance:

1.  **`db`**: The primary data warehouse for this project. It contains the `dev` schema where the `raw_weather_data` table is stored, as well as the analytics-ready tables created by dbt.
2.  **`airflow_db`**: The metadata database used internally by Apache Airflow. Airflow stores the state of all its DAGs, task instances, connections, and variables here.
3.  **`superset_db`**: The metadata database for Apache Superset. Superset stores all of its information—users, dashboards, charts, and database connection settings—in this database.

---
## 🔄 Pipeline Flow & Transformation Logic

1.  **Data Ingestion**:
    * An Airflow DAG, `weather_data_orchestrator`, is triggered on a schedule (e.g., every 5 minutes).
    * The DAG executes the `ingest_data_task`, which runs the `insert_records.py` Python script.
    * The script fetches the latest weather data for a predefined list of cities from the Weatherstack API.
    * The raw JSON data is then inserted into the `dev.raw_weather_data` table in the `db` database.

2.  **Data Transformation**:
    * Upon successful completion of the ingestion task, Airflow triggers a `dbt_run_task`.
    * This task executes `dbt run` inside its own Docker container, which runs the following models in sequence:
        * **`stg_weather_data.sql`**: A staging model that selects from the raw data, cleans column names, casts data types, and deduplicates records.
        * **`daily_average.sql`**: An intermediate model that computes the daily average temperature and wind speed for each city based on the staged data.
        * **`weather_report.sql`**: A final analytics-ready "mart" table that joins the staged data with the daily averages, providing a clean and enriched dataset for visualization.

3.  **Analytics & Visualization**:
    * Apache Superset is connected to the PostgreSQL `db` database as a data source.
    * Users can explore the `weather_report` table and other transformed tables to build charts.
    * An example dashboard is provided to visualize the latest weather trends and historical data.

