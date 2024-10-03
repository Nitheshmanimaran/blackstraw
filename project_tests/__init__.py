import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Path to the test CSV file
TEST_FILE_PATH = os.path.join(PROJECT_ROOT, 'raw_data', 'test.csv')

# Path to store the extracted data
EXTRACTED_DATA_PATH = os.path.join(PROJECT_ROOT, 'extracted_data.csv')

CONTINUOUS_FEATURE_COLUMNS = ['TotRmsAbvGrd', 'WoodDeckSF', 'YrSold', '1stFlrSF']
CATEGORICAL_FEATURE_COLUMNS = ['Foundation', 'KitchenQual']
FEATURE_COLUMNS = CONTINUOUS_FEATURE_COLUMNS + CATEGORICAL_FEATURE_COLUMNS

LABEL_COLUMN = 'SalePrice'
DB_NAME = "house_predictions"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
MONITOR_DIR = "/home/username/blackstraw/raw_data"
PATH = "/home/username/blackstraw"