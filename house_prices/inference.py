import joblib
import pandas as pd

from house_prices import MODEL_PATH, LABEL_COLUMN
from house_prices.preprocess import preprocess


def make_predictions(filepath: str) -> pd.DataFrame:
    df_raw = pd.read_csv(filepath)
    df = preprocess(df_raw, is_training=False)
    model = joblib.load(MODEL_PATH)
    df_raw[LABEL_COLUMN] = model.predict(df)
    return df_raw

def make_predictions_df(df: pd.DataFrame) -> pd.DataFrame:
    df = preprocess(df, is_training=False)
    model = joblib.load(MODEL_PATH)
    df[LABEL_COLUMN] = model.predict(df)
    return df
