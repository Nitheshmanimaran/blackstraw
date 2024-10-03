import os
import shutil

# Define the source and destination directories
source_dir = '/home/username/blackstraw'
template_dir = '/home/username/blackstraw_automation/{{cookiecutter.project_slug}}'

# List of directories to create
dirs_to_create = [
    'airflow/airflow/dags',
    'airflow/airflow/logs',
    'data/house-prices',
    'diagrams',
    'fastapi/prediction_model/models',
    'grafana',
    'gx/checkpoints',
    'gx/expectations/public/new_predictions',
    'gx/plugins/custom_data_docs/renderers',
    'gx/plugins/custom_data_docs/styles',
    'gx/plugins/custom_data_docs/views',
    'gx/profilers',
    'gx/uncommitted/data_docs/local_site/expectations/public/new_predictions',
    'gx/uncommitted/data_docs/local_site/static/fonts/HKGrotesk',
    'gx/uncommitted/data_docs/local_site/static/images',
    'gx/uncommitted/data_docs/local_site/static/styles',
    'gx/uncommitted/data_docs/local_site/validations/public/new_predictions/warning/__none__',
    'house_prices',
    'models/house-prices',
    'notebooks/modeling',
    'notebooks/pipeline-extraction',
    'raw_data',
    'streamlit_app',
    'tests'
]

# Create directories
for dir in dirs_to_create:
    os.makedirs(os.path.join(template_dir, dir), exist_ok=True)

# List of files to copy
files_to_copy = [
    ('airflow/airflow/dags/data_ingestion_dag.py', 'airflow/airflow/dags/data_ingestion_dag.py'),
    ('airflow/airflow/dags/prediction_dag.py', 'airflow/airflow/dags/prediction_dag.py'),
    ('airflow/airflow/params.py', 'airflow/airflow/params.py'),
    ('airflow/airflow/webserver_config.py', 'airflow/airflow/webserver_config.py'),
    ('airflow/airflow.cfg', 'airflow/airflow.cfg'),
    ('airflow/airflow.db', 'airflow/airflow.db'),
    ('airflow/webserver_config.py', 'airflow/webserver_config.py'),
    ('data/house-prices/continuous_df.parquet', 'data/house-prices/continuous_df.parquet'),
    ('data/house-prices/processed_df.parquet', 'data/house-prices/processed_df.parquet'),
    ('data/house-prices/test.csv', 'data/house-prices/test.csv'),
    ('data/house-prices/train.csv', 'data/house-prices/train.csv'),
    ('diagrams/archi.drawio', 'diagrams/archi.drawio'),
    ('diagrams/archi.png', 'diagrams/archi.png'),
    ('diagrams/snip.png', 'diagrams/snip.png'),
    ('fastapi/config.py', 'fastapi/config.py'),
    ('fastapi/db-data.json', 'fastapi/db-data.json'),
    ('fastapi/db.py', 'fastapi/db.py'),
    ('fastapi/main.py', 'fastapi/main.py'),
    ('fastapi/prediction_model/__init__.py', 'fastapi/prediction_model/__init__.py'),
    ('fastapi/prediction_model/models/model.joblib', 'fastapi/prediction_model/models/model.joblib'),
    ('fastapi/prediction_model/models/one_hot_encoder.joblib', 'fastapi/prediction_model/models/one_hot_encoder.joblib'),
    ('fastapi/prediction_model/models/scaler.joblib', 'fastapi/prediction_model/models/scaler.joblib'),
    ('fastapi/prediction_model/predict.py', 'fastapi/prediction_model/predict.py'),
    ('fastapi/prediction_model/preprocess.py', 'fastapi/prediction_model/preprocess.py'),
    ('grafana/dashboard.json', 'grafana/dashboard.json'),
    ('gx/checkpoints/my_checkpoint.yml', 'gx/checkpoints/my_checkpoint.yml'),
    ('gx/expectations/public/new_predictions/warning.json', 'gx/expectations/public/new_predictions/warning.json'),
    ('gx/great_expectations.yml', 'gx/great_expectations.yml'),
    ('gx/plugins/custom_data_docs/styles/data_docs_custom_styles.css', 'gx/plugins/custom_data_docs/styles/data_docs_custom_styles.css'),
    ('gx/uncommitted/config_variables.yml', 'gx/uncommitted/config_variables.yml'),
    ('gx/uncommitted/data_docs/local_site/expectations/public/new_predictions/warning.html', 'gx/uncommitted/data_docs/local_site/expectations/public/new_predictions/warning.html'),
    ('gx/uncommitted/data_docs/local_site/index.html', 'gx/uncommitted/data_docs/local_site/index.html'),
    ('gx/uncommitted/data_docs/local_site/static/styles/data_docs_custom_styles_template.css', 'gx/uncommitted/data_docs/local_site/static/styles/data_docs_custom_styles_template.css'),
    ('gx/uncommitted/data_docs/local_site/static/styles/data_docs_default_styles.css', 'gx/uncommitted/data_docs/local_site/static/styles/data_docs_default_styles.css'),
    ('house_prices/__init__.py', 'house_prices/__init__.py'),
    ('house_prices/inference.py', 'house_prices/inference.py'),
    ('house_prices/preprocess.py', 'house_prices/preprocess.py'),
    ('house_prices/train.py', 'house_prices/train.py'),
    ('models/house-prices/model.joblib', 'models/house-prices/model.joblib'),
    ('models/house-prices/one_hot_encoder.joblib', 'models/house-prices/one_hot_encoder.joblib'),
    ('models/house-prices/scaler.joblib', 'models/house-prices/scaler.joblib'),
    ('notebooks/modeling/house-prices-modeling-nw.ipynb', 'notebooks/modeling/house-prices-modeling-nw.ipynb'),
    ('notebooks/pipeline-extraction/model-industrialization-1-remove-get-dummies.ipynb', 'notebooks/pipeline-extraction/model-industrialization-1-remove-get-dummies.ipynb'),
    ('notebooks/pipeline-extraction/model-industrialization-2-split-in-the-top.ipynb', 'notebooks/pipeline-extraction/model-industrialization-2-split-in-the-top.ipynb'),
    ('notebooks/pipeline-extraction/model-industrialization-final.ipynb', 'notebooks/pipeline-extraction/model-industrialization-final.ipynb'),
    ('raw_data/test.csv', 'raw_data/test.csv'),
    ('streamlit_app/app.py', 'streamlit_app/app.py'),
    ('tests/config.py', 'tests/config.py'),
    ('tests/db_connection.py', 'tests/db_connection.py'),
    ('tests/test_airflow_connection.py', 'tests/test_airflow_connection.py'),
    ('tests/test_email.py', 'tests/test_email.py'),
    ('tests/test_extract_data.py', 'tests/test_extract_data.py'),
    ('tests/test_ge.py', 'tests/test_ge.py')
]

# Copy files
for src, dst in files_to_copy:
    shutil.copy(os.path.join(source_dir, src), os.path.join(template_dir, dst))