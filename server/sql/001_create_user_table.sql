CREATE TABLE tb_user (
    user_id serial PRIMARY KEY,
    username varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
)