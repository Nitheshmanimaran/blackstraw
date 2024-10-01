from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from config import Config
import psycopg2
from datetime import datetime
import warnings
warnings.filterwarnings("ignore")

# Load the model and other necessary artifacts
scaler = joblib.load(Config.SCALER_PATH)
one_hot_encoder = joblib.load(Config.ONE_HOT_ENCODER_PATH)
model = joblib.load(Config.MODEL_PATH)

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname=Config.DB_NAME,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT
    )
    return conn

app = FastAPI()

class HouseFeatures(BaseModel):
    TotRmsAbvGrd: int
    WoodDeckSF: int
    YrSold: int
    FirstFlrSF: int
    Foundation: str
    KitchenQual: str

@app.post("/predict")
def predict(features: HouseFeatures):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Prepare the input data
    continuous_features = np.array([[features.TotRmsAbvGrd, features.WoodDeckSF, features.YrSold, features.FirstFlrSF]])
    categorical_features = np.array([[features.Foundation, features.KitchenQual]])
    
    # Scale continuous features
    scaled_continuous_features = scaler.transform(continuous_features)
    
    # One-hot encode categorical features
    encoded_categorical_features = one_hot_encoder.transform(categorical_features).toarray()
    
    # Combine features
    combined_features = np.hstack((scaled_continuous_features, encoded_categorical_features))
    
    # Make prediction
    prediction = model.predict(combined_features)
    
    # Convert prediction to Python float with two decimal points
    sale_price = round(float(prediction[0]), 2)
    
    # Get current timestamp
    prediction_timestamp = datetime.now()
    
    # Insert prediction into the database
    cursor.execute(
        "INSERT INTO public.new_predictions (TotRmsAbvGrd, WoodDeckSF, YrSold, FirstFlrSF, Foundation, KitchenQual, SalePrice, PredictionTimestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (features.TotRmsAbvGrd, features.WoodDeckSF, features.YrSold, features.FirstFlrSF, features.Foundation, features.KitchenQual, sale_price, prediction_timestamp)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"SalePrice": f"{sale_price:.2f}", "PredictionTimestamp": prediction_timestamp}

@app.get("/check_db")
def check_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        return {"status": "Database connection successful"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)