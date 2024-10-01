from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime


def extract_data(**kwargs):
    source_hook = PostgresHook(postgres_conn_id='source_postgres_conn')
    source_conn = source_hook.get_conn()
    source_cursor = source_conn.cursor()

    source_cursor.execute("SELECT * FROM new_predictions")
    rows = source_cursor.fetchall()

    # Push rows to XCom
    kwargs['ti'].xcom_push(key='extracted_rows', value=rows)


def load_data(**kwargs):
    # Pull rows from XCom
    rows = kwargs['ti'].xcom_pull(key='extracted_rows', task_ids='extract_data')

    target_hook = PostgresHook(postgres_conn_id='target_postgres_conn')
    target_conn = target_hook.get_conn()
    target_cursor = target_conn.cursor()

    target_cursor.execute("""
        CREATE TABLE IF NOT EXISTS target_predictions (
            id INT PRIMARY KEY,
            totrmsabvgrd FLOAT,
            wooddecksf FLOAT,
            yrsold FLOAT,
            firstflrsf FLOAT,
            foundation FLOAT,
            kitchenqual FLOAT,
            saleprice FLOAT,
            predictiontimestamp TIMESTAMP
        );
    """)

    for row in rows:
        target_cursor.execute("""
            INSERT INTO target_predictions (id, totrmsabvgrd, wooddecksf, yrsold, firstflrsf, foundation, kitchenqual, saleprice, predictiontimestamp) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, row)

    target_conn.commit()
    target_cursor.close()
    target_conn.close()


with DAG(
    'test_postgres_connection_dag',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2023, 1, 1),
    },
    schedule_interval=None,  # Set to None to run manually
    catchup=False,
) as dag:

    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        provide_context=True,
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        provide_context=True,
    )

    extract_data_task >> load_data_task
