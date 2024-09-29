import joblib
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

from house_prices import CONTINUOUS_FEATURE_COLUMNS, CATEGORICAL_FEATURE_COLUMNS, SCALER_PATH, \
    ONE_HOT_ENCODER_PATH

# TODO:
"""
- manage errors (scaler not found, etc)
"""


def preprocess(dataframe: pd.DataFrame, is_training: bool = False) -> pd.DataFrame:
    continuous_features_df = preprocess_continuous_features(dataframe, is_training)
    categorical_features_df = preprocess_categorical_features(dataframe, is_training)
    return categorical_features_df.join(continuous_features_df)


def preprocess_continuous_features(dataframe: pd.DataFrame, is_training: bool) -> pd.DataFrame:
    if is_training:
        scaler = StandardScaler()
        scaler.fit(dataframe[CONTINUOUS_FEATURE_COLUMNS])
        joblib.dump(scaler, SCALER_PATH)
    else:
        # TODO: manage error if file not found
        scaler = joblib.load(SCALER_PATH)

    scaled_features_array = scaler.transform(dataframe[CONTINUOUS_FEATURE_COLUMNS])
    scaled_features_df = pd.DataFrame(data=scaled_features_array,
                                      columns=CONTINUOUS_FEATURE_COLUMNS,
                                      index=dataframe.index)
    return scaled_features_df


def preprocess_categorical_features(dataframe: pd.DataFrame, is_training: bool) -> pd.DataFrame:
    if is_training:
        one_hot_encoder = OneHotEncoder(handle_unknown='ignore', dtype='int')
        one_hot_encoder.fit(dataframe[CATEGORICAL_FEATURE_COLUMNS])
        joblib.dump(one_hot_encoder, ONE_HOT_ENCODER_PATH)
    else:
        # TODO: manage errors
        one_hot_encoder = joblib.load(ONE_HOT_ENCODER_PATH)

    categorical_features_sparse = one_hot_encoder.transform(dataframe[CATEGORICAL_FEATURE_COLUMNS])
    categorical_features_df = pd.DataFrame.sparse.from_spmatrix(data=categorical_features_sparse,
                                                                columns=one_hot_encoder.get_feature_names_out(),
                                                                index=dataframe.index)
    return categorical_features_df
