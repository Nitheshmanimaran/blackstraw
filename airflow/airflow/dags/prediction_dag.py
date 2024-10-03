import os
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from house_prices.preprocess import preprocess
from house_prices.inference import make_predictions

# Define the directory to watch for new CSV files
WATCH_DIRECTORY = "/home/username/blackstraw/data/ingest_raw_directory"
PROCESSED_FILES_LOG = "/home/username/blackstraw/data/processed_files.txt"

def check_for_new_files(**kwargs):
    # Read the list of already processed files
    if os.path.exists(PROCESSED_FILES_LOG):
        with open(PROCESSED_FILES_LOG, 'r') as f:
            processed_files = set(f.read().splitlines())
    else:
        processed_files = set()

    # List all CSV files in the directory
    all_csv_files = {f for f in os.listdir(WATCH_DIRECTORY) if f.endswith('.csv')}
    
    # Determine new files that haven't been processed
    new_files = all_csv_files - processed_files
    
    # Push the list of new files to XCom
    kwargs['ti'].xcom_push(key='csv_files', value=list(new_files))

def process_and_predict(**kwargs):
    # Pull the list of new CSV files from XCom
    csv_files = kwargs['ti'].xcom_pull(key='csv_files', task_ids='check_for_new_files')
    
    for csv_file in csv_files:
        file_path = os.path.join(WATCH_DIRECTORY, csv_file)
        
        predictions = make_predictions(file_path)        
        # Save predictions to a csv file in /home/username/blackstraw/data/predicted_csv_files
        predictions.to_csv(f'/home/username/blackstraw/data/predicted_csv_files/{csv_file}_predictions.csv', index=False)
        
        # Log the processed file
        with open(PROCESSED_FILES_LOG, 'a') as f:
            f.write(f"{csv_file}\n")

# Define the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 10, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'prediction_dag',
    default_args=default_args,
    description='A DAG to make predictions on new CSV files',
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    check_for_new_files_task = PythonOperator(
        task_id='check_for_new_files',
        python_callable=check_for_new_files,
        provide_context=True,
    )

    process_and_predict_task = PythonOperator(
        task_id='process_and_predict',
        python_callable=process_and_predict,
        provide_context=True,
    )

    check_for_new_files_task >> process_and_predict_task