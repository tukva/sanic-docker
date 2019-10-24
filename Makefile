include .env
export

setup_project:
		docker-compose up -d database
		docker-compose build
run_project:
		docker-compose up

run_psql:
		docker-compose run --rm database psql -U $(POSTGRES_DB) -h $(POSTGRES_HOST)