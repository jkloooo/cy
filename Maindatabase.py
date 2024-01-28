from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

username = "root"
password = "root"
host = "localhost"
databasename = "horizon"
engine = create_engine(f"mysql://{username}:{password}@{host}:3306/{databasename}")
base = declarative_base()
