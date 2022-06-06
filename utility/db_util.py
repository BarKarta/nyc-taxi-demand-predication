from typing import Final
import pandas as pd
import sqlalchemy as db


# Constants
HOST: Final[str] = 'localhost'

NYC_DB: Final[str] = 'nyc_taxis_db'
MANHATTAN_DB: Final[str] = 'manhattan'
POST_PREP: Final[str] = 'post_prep'
POST_PROCESS: Final[str] = 'post_procces_data'

USER: Final[str] = 'root'
PASSWORD: Final[str] = '12341234'
PORT: Final[str] = '3306'


def db_reader(sql: str, database_name: str) -> pd.DataFrame:
    conn = init_connection(database_name)
    reader = pd.read_sql(sql, conn, chunksize=20000)
    df = pd.concat(reader)
    return df


def db_writer(df: pd.DataFrame, table_name: str, database_name: str):
    conn = init_connection(database_name)
    df.to_sql(table_name, conn, chunksize=1000,
              method='multi', index=False, if_exists='replace')


def init_connection(db_name: str):
    match db_name:
        case 'nyc_taxis_db':
            engine = db.create_engine(
                f'mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{NYC_DB}')
        case 'manhattan':
            engine = db.create_engine(
                f'mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{MANHATTAN_DB}')
        case 'post_prep':
            engine = db.create_engine(
                f'mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{POST_PREP}')
        case 'post_procces_data':
            engine = db.create_engine(
                f'mariadb+mariadbconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{POST_PROCESS}')
    conn = engine.connect()
    return conn
