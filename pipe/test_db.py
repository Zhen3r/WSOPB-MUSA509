from os import environ
import pandas as pd
import psycopg2 as pg
from dotenv import load_dotenv
from pathlib import Path

envFilePath = '/Users/zh3n/Penn/OneDrive - PennO365/class/musa509/final-proj-509/pipe/.env'

load_dotenv(envFilePath)

# The database info is in env vars, thus using empty str to access.
engine = pg.connect("")

df = pd.read_sql('select 1 as hello_world', con=engine)
print(df)