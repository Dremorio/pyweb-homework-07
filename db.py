from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

url = 'postgresql+psycopg2://postgres:password@localhost:5432/pyweb2'
Base = declarative_base()
engine = create_engine(url, echo=True, pool_size=5)

DBSession = sessionmaker(bind=engine)
session = DBSession()
