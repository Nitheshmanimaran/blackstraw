class Config:
    SCALER_PATH = "/home/username/blackstraw/models/house-prices/scaler.joblib"
    ONE_HOT_ENCODER_PATH = "/home/username/blackstraw/models/house-prices/one_hot_encoder.joblib"
    MODEL_PATH = "/home/username/blackstraw/models/house-prices/model.joblib"
    DB_NAME = "house_predictions"
    DB_USER = "postgres"
    DB_PASSWORD = "postgres"
    DB_HOST = "localhost"
    DB_PORT = "5432"

    #export PATH=$PATH:~/.local/bin
    #export AIRFLOW_HOME=${PWD}/airflow
    #ps aux | grep airflow
    #kill -9 <PID>
    #pkill -f "airflow scheduler"
    #pkill -f "airflow webserver"
    #export SENDER_EMAIL="nithesh.kumar@blackstraw.ai"
    #export SENDER_PASSWORD="npcr lgni nors byst"
    #export RECEIVER_EMAIL="nithesh.kumar@blackstraw.ai"