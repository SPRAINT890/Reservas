from sqlalchemy import create_engine, MetaData
import os

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine("mysql+pymysql://root:root@db:3306/reservas")

meta = MetaData()

conexionDB = engine.connect().execution_options(isolation_level="AUTOCOMMIT")