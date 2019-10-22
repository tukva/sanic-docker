from engine import Engine, Connection


async def prepare_db(app, loop):
    await Engine.init()
    async with Connection() as conn:
        await conn.execute('DROP TABLE IF EXISTS tb_user_group')
        await conn.execute('DROP TABLE IF EXISTS tb_group_permission')
        await conn.execute('DROP TABLE IF EXISTS tb_user')
        await conn.execute('DROP TABLE IF EXISTS tb_session')
        await conn.execute('DROP TABLE IF EXISTS tb_permission')
        await conn.execute('DROP TABLE IF EXISTS tb_group')

        await conn.execute('''CREATE TABLE tb_user (
                           user_id serial PRIMARY KEY,
                           username varchar(255) NOT NULL UNIQUE, 
                           password varchar(255) NOT NULL)''')
        await conn.execute('''CREATE TABLE tb_session (
                           session_id varchar(255) NOT NULL UNIQUE,
                           user_id INTEGER NOT NULL)''')
        await conn.execute('''CREATE TABLE tb_permission (
                           permission_id serial PRIMARY KEY,
                           name varchar(50) NOT NULL UNIQUE)''')
        await conn.execute('''INSERT INTO tb_permission (name) VALUES ('special')''')
        await conn.execute('''INSERT INTO tb_permission (name) VALUES ('view')''')
        await conn.execute('''INSERT INTO tb_permission (name) VALUES ('edit')''')
        await conn.execute('''CREATE TABLE tb_group (
                           group_id serial PRIMARY KEY,
                           name varchar(50) NOT NULL UNIQUE)''')
        await conn.execute('''INSERT INTO tb_group (name) VALUES ('admins')''')
        await conn.execute('''INSERT INTO tb_group (name) VALUES ('viewers')''')
        await conn.execute('''INSERT INTO tb_group (name) VALUES ('editors')''')
        await conn.execute('''CREATE TABLE tb_user_group (
                           user_id int REFERENCES tb_user (user_id) ON DELETE CASCADE, 
                           group_id int REFERENCES tb_group (group_id) ON DELETE CASCADE,
                           CONSTRAINT tb_user_group_pkey PRIMARY KEY (user_id, group_id))''')
        await conn.execute('''CREATE TABLE tb_group_permission (
                           group_id int REFERENCES tb_group (group_id) ON DELETE CASCADE, 
                           permission_id int REFERENCES tb_permission (permission_id) ON DELETE CASCADE,
                           CONSTRAINT tb_group_permission_pkey PRIMARY KEY (group_id, permission_id))''')
        await conn.execute('''INSERT INTO tb_group_permission VALUES (1, 1)''')
        await conn.execute('''INSERT INTO tb_group_permission VALUES (1, 2)''')
        await conn.execute('''INSERT INTO tb_group_permission VALUES (1, 3)''')
        await conn.execute('''INSERT INTO tb_group_permission VALUES (2, 2)''')
        await conn.execute('''INSERT INTO tb_group_permission VALUES (3, 3)''')
