CONTINUOUS_FEATURE_COLUMNS = ['TotRmsAbvGrd', 'WoodDeckSF', 'YrSold', '1stFlrSF']
CATEGORICAL_FEATURE_COLUMNS = ['Foundation', 'KitchenQual']
FEATURE_COLUMNS = CONTINUOUS_FEATURE_COLUMNS + CATEGORICAL_FEATURE_COLUMNS
LABEL_COLUMN = 'SalePrice'

SERIALIZER_EXTENSION = '.joblib'
ARTIFACTS_DIR = '../../models/house-prices'
SCALER_PATH = "/home/username/blackstraw/models/house-prices/scaler.joblib"
ONE_HOT_ENCODER_PATH = "/home/username/blackstraw/models/house-prices/one_hot_encoder.joblib"
MODEL_PATH = "/home/username/blackstraw/models/house-prices/model.joblib"
