from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id="ntry_etl_pipeline",
    start_date=datetime(2026, 8, 1),
    schedule=None,
    catchup=False,
    tags=["ntry", "etl", "cybersecurity"],
) as dag:

    run_etl = BashOperator(
        task_id="run_etl",
        bash_command="python /opt/airflow/ETL/parse_logs.py",
    )