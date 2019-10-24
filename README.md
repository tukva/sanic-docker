## Setup with docker

1. Install `docker` and `docker-compose`
1. Set environment variable in `.env` file
1. Setup project via `make setup_project`
1. Create migrations via `docker-compose run --rm liquibase update`

## Run with docker

1. Run via `make run_project`

## Run psql

Run via `make run_psql`


##Create a migration on DB schema change

1. Add new sql script to server/sql  with semantic name like "001_create_user_table"
1. Create change via `docker-compose run --rm liquibase update` 