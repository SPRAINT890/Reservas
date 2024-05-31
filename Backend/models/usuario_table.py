from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from Backend.config.BD import meta, engine

usuario = Table("usuario", meta, 
              Column("ci", Integer, primary_key=True), 
              Column("nombre", String(40)), 
              Column("apellido", String(40)),
              Column("email", String(100), unique=True, nullable=False), 
              Column("contraseña", String(256)))

meta.create_all(engine)
