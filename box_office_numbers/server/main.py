from fastapi import FastAPI
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, 'cache')
dataset = os.path.join(CACHE_DIR, "box_office_dataset_cleaned.csv")
app = FastAPI()


@app.get('/')
def read_root():
    return {"Hello" : "World"}


# use postgreSQL or nosql for production
@app.get("/box-office")
def box_office_numbers():
    df = pd.read_csv(dataset)
    # order using rank
    return df.to_dict("Rank")