import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
import pandas as pd
import joblib
import great_expectations as gx
from great_expectations.exceptions import DataContextError
from house_prices import FEATURE_COLUMNS, MODEL_PATH
from house_prices.preprocess import preprocess

MONITOR_DIR = "/home/username/blackstraw/raw_data"

def extract_data(**kwargs):
    import glob

    directory_to_monitor = MONITOR_DIR

    #Getting list of csv files
    csv_files = [f for f in glob.glob(os.path.join(directory_to_monitor, '*.csv')) if '_checked' not in f]
    
    if not csv_files:
        print("All csv files are already scanned. No new files" + csv_files)
    
    for file_path in csv_files:
        df_raw = pd.read_csv(file_path)
        
        df = preprocess(df_raw[FEATURE_COLUMNS], is_training=False)
        kwargs['ti'].xcom_push(key='extracted_rows', value=df.to_dict(orient='records'))
        
        df.to_csv('/home/username/blackstraw/sample.csv', index=False)
        # Rename the processed file
        new_file_path = file_path.replace('.csv', '_checked.csv')
        os.rename(file_path, new_file_path)

def validate_data():
    try:
        # Initialize the GE context
        context = gx.get_context()

        # Load the checkpoint configuration
        checkpoint_name = "my_checkpoint"
        checkpoint = context.get_checkpoint(checkpoint_name)

        # Run the checkpoint
        checkpoint_result = checkpoint.run()

        # Check if the validation was successful
        if checkpoint_result["success"]:
            print("Data quality check passed.")
        else:
            print("Data quality check failed.")
            for validation_result in checkpoint_result["run_results"].values():
                if not validation_result["validation_result"]["success"]:
                    print(validation_result["validation_result"])

        # Build and open Data Docs
        context.build_data_docs()
        validation_result_identifier = checkpoint_result.list_validation_result_identifiers()[0]
        context.open_data_docs(resource_identifier=validation_result_identifier)

    except DataContextError as e:
        print(f"Error loading GE context: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def load_data(**kwargs):
    # Pull rows from XCom
    rows = kwargs['ti'].xcom_pull(key='extracted_rows', task_ids='extract_data')

    target_hook = PostgresHook(postgres_conn_id='target_postgres_conn')
    target_conn = target_hook.get_conn()
    target_cursor = target_conn.cursor()

    # Create the updated table schema
    target_cursor.execute("""
        CREATE TABLE IF NOT EXISTS target_predictions (
            id SERIAL PRIMARY KEY,
            Foundation_BrkTil TEXT,
            Foundation_CBlock TEXT,
            Foundation_PConc TEXT,
            Foundation_Slab TEXT,
            Foundation_Stone TEXT,
            Foundation_Wood TEXT,
            KitchenQual_Ex TEXT,
            KitchenQual_Fa TEXT,
            KitchenQual_Gd TEXT,
            KitchenQual_TA TEXT,
            TotRmsAbvGrd TEXT,
            WoodDeckSF TEXT,
            YrSold TEXT,
            "1stFlrSF" TEXT,
            "SalePrice" TEXT,
            "PredictionTimestamp" TEXT
        );
    """)

    for row in rows:
        try:
            target_cursor.execute("""
                INSERT INTO target_predictions (
                    Foundation_BrkTil, Foundation_CBlock, Foundation_PConc, Foundation_Slab, 
                    Foundation_Stone, Foundation_Wood, KitchenQual_Ex, KitchenQual_Fa, 
                    KitchenQual_Gd, KitchenQual_TA, TotRmsAbvGrd, WoodDeckSF, YrSold, 
                    "1stFlrSF"
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                row['Foundation_BrkTil'], row['Foundation_CBlock'], row['Foundation_PConc'], row['Foundation_Slab'],
                row['Foundation_Stone'], row['Foundation_Wood'], row['KitchenQual_Ex'], row['KitchenQual_Fa'],
                row['KitchenQual_Gd'], row['KitchenQual_TA'], row['TotRmsAbvGrd'], row['WoodDeckSF'], row['YrSold'],
                row['1stFlrSF']
            ))
        except Exception as e:
            print(f"Error inserting row {row}: {e}")

    target_conn.commit()
    target_cursor.close()
    target_conn.close()

with DAG(
    'data_ingestion_dag',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2023, 1, 1),
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    schedule=None,  # Set to None to run manually
    catchup=False,
) as dag:

    sense_file_task = FileSensor(
        task_id='sense_file',
        filepath=MONITOR_DIR,
        fs_conn_id='fs_default',
        poke_interval=10,
        timeout=600,
    )

    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    validate_data_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    sense_file_task >> extract_data_task >> validate_data_task >> load_data_task