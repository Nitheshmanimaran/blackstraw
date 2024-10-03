import pandas as pd
import sys
import os
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from house_prices.preprocess import preprocess
from house_prices.inference import make_predictions_df

def read_from_db() -> pd.DataFrame:
    # Hardcoded connection details
    db_user = 'postgres'
    db_password = 'postgres'
    db_host = '172.23.167.43'
    db_port = '5432'
    db_name = 'house_predictions_target'

    # Create a SQLAlchemy engine
    engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
    
    sql = """
    SELECT 
        foundation_brktil, foundation_cblock, foundation_pconc, foundation_slab, 
        foundation_stone, foundation_wood, kitchenqual_ex, kitchenqual_fa, 
        kitchenqual_gd, kitchenqual_ta, totrmsabvgrd, wooddecksf, yrsold, 
        "1stFlrSF"
    FROM target_predictions
    """ 
    df = pd.read_sql(sql, engine)

    # Print columns from DB
    print("Columns from DB:", df.columns.tolist())

    # Rename columns to match the expected format
    df.columns = [
        'Foundation_BrkTil', 'Foundation_CBlock', 'Foundation_PConc',
        'Foundation_Slab', 'Foundation_Stone', 'Foundation_Wood',
        'KitchenQual_Ex', 'KitchenQual_Fa', 'KitchenQual_Gd', 'KitchenQual_TA',
        'TotRmsAbvGrd', 'WoodDeckSF', 'YrSold', '1stFlrSF'
    ]

    # Create combined categorical columns if needed
    df['Foundation'] = df[['Foundation_BrkTil', 'Foundation_CBlock', 'Foundation_PConc', 
                           'Foundation_Slab', 'Foundation_Stone', 'Foundation_Wood']].idxmax(axis=1)
    df['KitchenQual'] = df[['KitchenQual_Ex', 'KitchenQual_Fa', 'KitchenQual_Gd', 'KitchenQual_TA']].idxmax(axis=1)

    # Print columns before preprocess
    print("Columns before preprocess:", df.columns.tolist())

    return df

def preprocess_task():
    data = read_from_db()
    preprocessed_data = preprocess(data, is_training=False)

    # Print columns after preprocess
    print("Columns after preprocess:", preprocessed_data.columns.tolist())

    return preprocessed_data

def make_predictions_task():
    # Get preprocessed data
    preprocessed_data = preprocess_task()

    # Ensure the data is in the correct format for prediction
    # If make_predictions_df expects certain columns, ensure they are present
    # This might involve renaming or adding columns as needed

    predictions = make_predictions_df(preprocessed_data)
    return predictions

if __name__ == "__main__":
    predictions = make_predictions_task()
    print(predictions.head())
    print(predictions.columns)