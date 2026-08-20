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

    extract = BashOperator(
        task_id="extract",
        bash_command="echo 'Extract: validando archivo de entrada'",
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="echo 'Transform: preparando datos'",
    )

    load = BashOperator(
        task_id="load",
        bash_command="python /opt/airflow/ETL/parse_logs.py",
    )

    extract >> transform >> load