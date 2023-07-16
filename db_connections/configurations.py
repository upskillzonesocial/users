import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_connection_url = "postgresql://postgres:1995@localhost:5432/postgres"

engine = create_engine(url=db_connection_url,echo=True)
conn = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()
