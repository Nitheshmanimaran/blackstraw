import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from config import Config


def split_dataset(data: pd.DataFrame, label: str):
    X, y = data.drop([label], axis=1), data[label]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.33,
        random_state=42
    )
    return X_train, X_test, y_train, y_test


def filter_useless_columns(X: pd.DataFrame) -> pd.DataFrame:
    useful_features = [
        'Foundation',
        'KitchenQual',
        'TotRmsAbvGrd',
        'WoodDeckSF',
        'YrSold',
        '1stFlrSF'
    ]
    X = X[useful_features]
    return X


def scale_continuous_features(X: pd.DataFrame):
    continuous_columns = [
        'TotRmsAbvGrd',
        'WoodDeckSF',
        'YrSold',
        '1stFlrSF'
    ]
    scaler = joblib.load(Config.SCALER_PATH)
    scaled_columns = scaler.transform(X[continuous_columns])
    continuous_features = pd.DataFrame(
        data=scaled_columns,
        columns=continuous_columns
    )
    return continuous_features


def convert_categorical_values(X: pd.DataFrame) -> pd.DataFrame:
    categorical_columns = [
        "Foundation",
        "KitchenQual"
    ]
    ohe = joblib.load(Config.ONE_HOT_ENCODER_PATH)
    array_hot_encoded = ohe.transform(X[categorical_columns])
    feature_columns = ohe.get_feature_names_out()
    categorical_features = pd.DataFrame.sparse.from_spmatrix(
        array_hot_encoded,
        columns=feature_columns
    )
    return categorical_features


def scale_convert_features(X: pd.DataFrame) -> pd.DataFrame:
    continuous_features = scale_continuous_features(X)
    categorical_features = convert_categorical_values(X)
    X_joined = continuous_features.join(categorical_features)
    return X_joined


def preprocess(X: pd.DataFrame, y: np.array):
    X = filter_useless_columns(X)
    X = scale_convert_features(X)
    return X, y


def make_multiple_predictions(input_data: pd.DataFrame) -> np.ndarray:
    dataframe = scale_convert_features(input_data)
    model = joblib.load(Config.MODEL_PATH)
    y_pred = model.predict(dataframe)
    return np.around(y_pred, 2)


def make_single_prediction(input_data: pd.DataFrame) -> np.ndarray:
    return make_multiple_predictions(input_data)[0]
