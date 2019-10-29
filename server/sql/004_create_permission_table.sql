CREATE TABLE tb_permission (
    permission_id serial PRIMARY KEY,
    name varchar(50) NOT NULL UNIQUE
)
