## Setup with docker

1. Set environment variable in `.env` file
1. Install `docker` and `docker-compose`
1. Setup project via `make setup_project`

## Run with docker

1. Run via `make run_project`

## Run psql

docker-compose run --rm database psql -U test -h database
