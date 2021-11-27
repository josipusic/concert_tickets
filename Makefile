PROJECT_NAME=$(notdir $(shell pwd))
LOCAL_DB_NAME=${PROJECT_NAME}
LOCAL_DB_USER=${PROJECT_NAME}

# local commands

generate-local-env-file:
	@cd config/local && bash ./setup.sh

start: generate-local-env-file
	@echo "== Starting local environment"
	@cd config/local && docker-compose up -d
	@cd config/local && rm -f requirements.txt

start-with-logs: generate-local-env-file
	@echo "== Starting local environment with dynamic logs"
	@cd config/local && docker-compose up
	@cd config/local && rm -f requirements.txt

start-build: generate-local-env-file
	@echo "== Rebuilding images and starting local environment"
	@cd config/local && docker-compose up --build -d
	@cd config/local && rm -f requirements.txt

start-with-logs-build: generate-local-env-file
	@echo "== Rebuilding images and starting local environment with dynamic logs"
	@cd config/local && docker-compose up --build
	@cd config/local && rm -f requirements.txt

stop:
	@echo "== Stopping local environment"
	@cd config/local && docker-compose down

stop-v:
	@echo "== Stopping local environment and destroying database"
	@cd config/local && docker-compose down -v

stop-all:
	@echo "== Stopping local environment, destroying database and related images"
	@cd config/local && docker-compose down -v --rm all

new-app:
	@read -p "What will the new app be called: " app_name; \
	docker container exec ${PROJECT_NAME}_local_backend python manage.py startapp $$app_name
	@echo "App created"

migrations:
	@echo "== Creating migration file(s) for ${PROJECT_NAME} project"
	@docker container exec -it ${PROJECT_NAME}_local_backend python manage.py makemigrations

migrate:
	@echo "== Applying migrations for ${PROJECT_NAME} project"
	@docker container exec -it ${PROJECT_NAME}_local_backend python manage.py migrate

db:
	@echo "== Entering postgres shell for ${PROJECT_NAME} project"
	@echo "== Connecting to database"
	@docker container exec -it ${PROJECT_NAME}_local_db psql -U ${LOCAL_DB_USER} ${LOCAL_DB_NAME}

db-help:
	@echo "== Entering postgres shell for ${PROJECT_NAME} project"
	@echo "== Connecting to database"
	@docker container exec -it ${PROJECT_NAME}_local_db psql --help

backend:
	@echo "== Entering backend container tty"
	@docker container exec -it ${PROJECT_NAME}_local_backend bash

backend-logs:
	@docker container logs ${PROJECT_NAME}_local_backend --tail 50

backend-logs-2m:
	@docker container logs ${PROJECT_NAME}_local_backend --since=2m

backend-logs-all:
	@docker container logs ${PROJECT_NAME}_local_backend

db-logs:
	@docker container logs ${PROJECT_NAME}_local_db

style-check:
	@docker container exec -t ${PROJECT_NAME}_local_backend bash -c "flake8"

django-shell:
	@docker container exec -it ${PROJECT_NAME}_local_backend python manage.py shell

docker-list:
	@echo ""
	@echo "============ IMAGES =====================================================================================\
	================================================================================================================"
	@echo ""
	@docker image ls
	@echo ""
	@echo "============ NETWORKS ===================================================================================\
	================================================================================================================"
	@echo ""
	@docker network ls
	@echo ""
	@echo "============ VOLUMES ====================================================================================\
	================================================================================================================"
	@echo ""
	@docker volume ls
	@echo ""
	@echo "============ ALL CONTAINERS =============================================================================\
	================================================================================================================"
	@echo ""
	@docker container ls -a
	@echo ""
	@echo "============ RUNNING CONTAINERS =========================================================================\
	================================================================================================================"
	@echo ""
	@docker container ls
	@echo ""
