import pandas as pd
import psycopg2 as pg
from dotenv import load_dotenv

# loading the remote database info (hostname, pwd, port, etc.)
# into environment variables.
envFilePath = '/Users/zh3n/Penn/OneDrive - PennO365/class/musa509/final-proj-509/pipe/.env'
load_dotenv(envFilePath)

# Passing empty str to use env vars to access db.
engine = pg.connect("")

df = pd.read_sql('select 1 as hello_world', con=engine)
print(df)