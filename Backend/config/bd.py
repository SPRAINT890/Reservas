from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine("mysql+pymysql://root:root@db:3306/reservas")

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

meta = MetaData()

Base = declarative_base()
