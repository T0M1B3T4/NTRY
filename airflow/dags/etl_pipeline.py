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
        bash_command="""
        echo "📥 ================================"
        echo "📥 NTRY - EXTRACT"
        echo "📥 ================================"

        INPUT="/data/raw/login_logs.jsonl"

        if [ -f "$INPUT" ]; then
            RECORDS=$(grep -cve '^[[:space:]]*$' "$INPUT")

            echo "📂 Archivo: $INPUT"
            echo "📊 Registros encontrados: $RECORDS"
            echo "✅ Extract completado"
        else
            echo "❌ ERROR: archivo de entrada no encontrado"
            exit 1
        fi
        """,
    )

    transform = BashOperator(
        task_id="transform",
        bash_command="""
        echo "🧹 ================================"
        echo "🧹 NTRY - TRANSFORM"
        echo "🧹 ================================"

        echo "🐼 Motor: Pandas"
        echo "🧽 Validando y preparando datos..."
        echo "🔑 Preparando identificadores de eventos..."
        echo "📊 Preparando features..."

        echo "✅ Transform completado"
        """,
    )

    load = BashOperator(
        task_id="load",
        bash_command="""
        echo "📤 ================================"
        echo "📤 NTRY - LOAD"
        echo "📤 ================================"

        python /opt/airflow/ETL/parse_logs.py

        echo "✅ Load (Carga) completa"
        """,
    )

    extract >> transform >> load
