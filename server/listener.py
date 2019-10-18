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
                               session_id varchar(255) NOT NULL UNIQUE,
                               user_id INTEGER NOT NULL)''')
            await conn.execute('DROP TABLE IF EXISTS tb_permission')
            await conn.execute('''CREATE TABLE tb_permission (
                               permission_id serial PRIMARY KEY,
                               name varchar(50) NOT NULL UNIQUE)''')
            await conn.execute('DROP TABLE IF EXISTS tb_group')
            await conn.execute('''CREATE TABLE tb_group (
                               group_id serial PRIMARY KEY,
                               name varchar(50) NOT NULL UNIQUE)''')
            await conn.execute('DROP TABLE IF EXISTS tb_user_group')
            await conn.execute('''CREATE TABLE tb_user_group (
                               user_id int REFERENCES tb_user (user_id) ON UPDATE CASCADE ON DELETE CASCADE, 
                               group_id int REFERENCES tb_group (group_id) ON UPDATE CASCADE ON DELETE CASCADE)''')
            await conn.execute('DROP TABLE IF EXISTS tb_group_permission')
            await conn.execute(
                '''CREATE TABLE tb_group_permission (
                group_id int REFERENCES tb_group (group_id) ON UPDATE CASCADE ON DELETE CASCADE, 
                permission_id int REFERENCES tb_permission (permission_id) ON UPDATE CASCADE ON DELETE CASCADE)''')
