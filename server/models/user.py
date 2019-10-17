from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine('postgresql://test:test@database/test')

meta = MetaData()

users = Table(
   'users', meta,
   Column('id', Integer, primary_key=True),
   Column('username', String),
)

meta.create_all(engine)
