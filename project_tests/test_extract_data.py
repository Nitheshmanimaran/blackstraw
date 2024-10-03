import pandas as pd
import sys
from project_tests import PROJECT_ROOT, TEST_FILE_PATH, EXTRACTED_DATA_PATH
import os

# Add the parent directory of project_tests to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from house_prices import FEATURE_COLUMNS
from house_prices.preprocess import preprocess

def extract_data(file_path):
    # Read the CSV file
    df_raw = pd.read_csv(file_path)
    
    # Preprocess the data (excluding saleprice)
    df = preprocess(df_raw[FEATURE_COLUMNS], is_training=False)

    df.to_csv('sample_data.csv', index=False)
    
    # Return the processed data
    return df.to_dict(orient='records')

# Test the function
if __name__ == "__main__":
    # Call the function
    extracted_data = extract_data(TEST_FILE_PATH)
    
    # Store the result in a CSV file
    pd.DataFrame(extracted_data).to_csv(EXTRACTED_DATA_PATH, index=False)
