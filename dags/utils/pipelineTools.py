import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# loading the remote database info (hostname, pwd, port, etc.)
# into environment variables.
envFilePath = '/Users/zh3n/Penn/OneDrive - PennO365/class/musa509/final-proj-509/dags/utils/.env'
load_dotenv(envFilePath)
PGHOST = os.getenv("PGHOST")
PGPORT = os.getenv("PGPORT")
PGDATABASE = os.getenv("PGDATABASE")
PGUSER = os.getenv("PGUSER")
PGPASSWORD = os.getenv("PGPASSWORD")

engine = create_engine(f"postgresql+psycopg2://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}")

def gpd_to_postgres(gdf: gpd.GeoDataFrame, tablename: str, if_exists: str = "replace"):
    gdf.to_postgis(
        con=engine,
        name=tablename,
        if_exists=if_exists
    )
    return True


def postgres_to_gpd(sql: str):
    gdf = gpd.read_postgis(
        sql=sql,
        con=engine,
        geom_col="geometry"
    )
    return gdf

def pd_to_postgres(df: pd.DataFrame, tablename: str, if_exists: str = "replace"):
    df.to_sql(
        tablename, 
        con=engine, 
        if_exists=if_exists, 
        index=False
    )
    return True

def postgres_to_pd(sql: str):
    df = pd.read_sql(
        sql=sql,
        con=engine,
    )
    return df

if __name__ == "__main__":
    # gdf = gpd.GeoDataFrame(
    #     {"a": [1]}, geometry=gpd.points_from_xy(x=[1], y=[2], crs=4326))
    # print(gdf)
    # gpd_to_postgres(gdf,"test_table")
    # print(postgres_to_gpd("select * from test_table"))

    data = pd.DataFrame({"a":[1,2]})
    print(data)
    pd_to_postgres(data,"test_table")
    print(postgres_to_pd("select * from test_table"))
