from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Define the DAG
with DAG(
    'ingest_dag',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2023, 1, 1),
    },
    schedule_interval='@daily',
    catchup=False,
) as dag:
    
    start = BashOperator(
        task_id='start',
        bash_command='echo "Ingest DAG started"',
    )

    # Set task dependencies
    start

    end = BashOperator(
        task_id='end',
        bash_command='echo "Ingest DAG completed"',
    )

    # Set task dependencies
    end

    start >> end


