from sqlalchemy import create_engine, MetaData
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)

meta = MetaData()

conexionDB = engine.connect()