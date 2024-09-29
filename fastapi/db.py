import psycopg2
import json
import os


def get_db_conection():
    db_data_path = f"{os.path.dirname(__file__)}/db-data.json"
    with open(db_data_path, "r") as f:
        db_data = json.load(f)
    con = psycopg2.connect(**db_data)
    return con


def insert_single_prediction(prediction: dict):
    con = get_db_conection()
    cur = con.cursor()

    columns = ', '.join(str(x) for x in prediction.keys()
                        ).replace("1stFlrSF", "FirstFlrSF"
                                  ).replace("2ndFlrSF", "SecondFlrSF").replace(
                            "3SsnPorch", "ThreeSsnPorch")
    values = ', '.join(str(x) if type(
        x) == 'int' else f"'{x}'" for x in prediction.values())

    cur.execute(f"INSERT INTO predictions({columns}) VALUES({values});")
    con.commit()

    con.close()


def insert_multiple_predictions(predictions: list[dict]):
    for prediction in predictions:
        insert_single_prediction(prediction)


def get_predictions_by_time_interval(start_date: str,
                                     end_date: str) -> list[tuple]:
    con = get_db_conection()
    cur = con.cursor()
    cur.execute(
        f"""SELECT * FROM predictions WHERE predictiondate >= '{start_date}'
        AND predictiondate <= '{end_date}';""")

    rows = cur.fetchall()

    return rows
