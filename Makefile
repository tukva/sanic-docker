setup_project:
		docker-compose up -d database
		docker-compose build

run_project:
		docker-compose up
