from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_log_error
from sklearn.model_selection import train_test_split

from house_prices import FEATURE_COLUMNS, LABEL_COLUMN, MODEL_PATH
from house_prices.preprocess import preprocess

# TODO:
"""
- ...
"""


def build_model(filepath: str) -> dict[str, float]:
    df_raw = pd.read_csv(filepath)
    df = preprocess(df_raw[FEATURE_COLUMNS], is_training=True)
    X_train, X_test, y_train, y_test = train_test_split(df, df_raw[LABEL_COLUMN], test_size=0.33, random_state=42)
    model = train_model(X_train, y_train)
    y_test_pred = model.predict(X_test)
    return {'rmsle': compute_rmsle(y_test, y_test_pred)}


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> Any:
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    return model


def compute_rmsle(y_test: np.ndarray, y_pred: np.ndarray, precision: int = 2) -> float:
    rmsle = np.sqrt(mean_squared_log_error(y_test, y_pred))
    return round(rmsle, precision)
