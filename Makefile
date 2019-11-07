include .env
export

setup_project:
		docker-compose up -d database
		docker-compose build
run_project:
		docker-compose up server
run_psql:
		docker-compose run --rm database psql -U $(POSTGRES_DB) -h $(POSTGRES_HOST)
run_tests:
		docker-compose -f docker-compose.testing.yml up -d test_database
		docker-compose -f docker-compose.testing.yml build
		docker-compose -f docker-compose.testing.yml run --rm test_server
		docker-compose -f docker-compose.testing.yml down