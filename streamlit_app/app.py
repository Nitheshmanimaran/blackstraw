import streamlit as st
import requests

# Define the FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/predict"

# Streamlit app
st.title("House Price Prediction")

# Input fields
TotRmsAbvGrd = st.number_input("Total Rooms Above Ground", min_value=0, step=1)
WoodDeckSF = st.number_input("Wood Deck SF", min_value=0, step=1)
YrSold = st.number_input("Year Sold", min_value=1900, step=1)
FirstFlrSF = st.number_input("First Floor SF", min_value=0, step=1)
Foundation = st.selectbox("Foundation", ["BrkTil", "CBlock", "PConc", "Slab", "Stone", "Wood"])
KitchenQual = st.selectbox("Kitchen Quality", ["Ex", "Gd", "TA", "Fa", "Po"])

# Predict button
if st.button("Predict"):
    # Prepare the payload
    payload = {
        "TotRmsAbvGrd": TotRmsAbvGrd,
        "WoodDeckSF": WoodDeckSF,
        "YrSold": YrSold,
        "FirstFlrSF": FirstFlrSF,
        "Foundation": Foundation,
        "KitchenQual": KitchenQual
    }
    
    # Make the request to the FastAPI endpoint
    response = requests.post(FASTAPI_URL, json=payload)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Predicted Sale Price: ${result['SalePrice']}")
    else:
        st.error("Error in prediction")