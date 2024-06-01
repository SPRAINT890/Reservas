from sqlalchemy import Table, Column, Integer, String
from Backend.config.bd import meta, engine

usuario = Table("usuario", meta, 
              Column("ci", Integer, primary_key=True), 
              Column("nombre", String(40)), 
              Column("apellido", String(40)),
              Column("email", String(100)), 
              Column("contrasena", String(556)))

meta.create_all(bind=engine, tables=[usuario])