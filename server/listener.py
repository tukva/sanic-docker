from aiopg.sa import create_engine

from db import connection


async def prepare_db(app, loop):
    async with create_engine(connection) as engine:
        async with engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS tb_user')
            await conn.execute('''CREATE TABLE tb_user (
                                user_id serial PRIMARY KEY,
                                username varchar(255) NOT NULL UNIQUE, 
                                password varchar(255) NOT NULL,
                                permission TEXT [])''')
            await conn.execute('DROP TABLE IF EXISTS tb_session')
            await conn.execute('''CREATE TABLE tb_session (
                                            session_id varchar(255),
                                            user_id INTEGER NOT NULL)''')
