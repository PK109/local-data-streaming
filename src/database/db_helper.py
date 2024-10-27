import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import urllib.parse

# Load environment variables from the .env file to config
def load_config(path= '.env'):
    load_dotenv(dotenv_path=path)
    config = {}
    config['dialect']='postgresql'
    config['host']=os.getenv("POSTGRES_HOST")
    config['user']=os.getenv("POSTGRES_USER")
    config['password']=os.getenv("POSTGRES_PASSWORD")
    config['database']=os.getenv("POSTGRES_DB")
    config['port']=os.getenv("POSTGRES_PORT")
    return config

def get_engine(config):
    """ Connect to the PostgreSQL database server """
    dialect = config['dialect']
    user = config['user']
    password = urllib.parse.quote_plus(config['password'])
    host = config['host']
    port = config['port']
    database = config['database']

    try:
        conn_string =f"{dialect}://{user}:{password}@{host}:{port}/{database}"
        # connecting to the PostgreSQL server
        engine = create_engine(conn_string)
        # print(f"Engine for {dialect} created.")
        return engine
    except (Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    get_engine(config)