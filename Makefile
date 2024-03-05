all:
	@echo "make gamefied - Starts script to run the gamefied"
	@echo "make up - Start the containers"
	@echo "make upd - Start the containers in background"
	@echo "make down - Stop the containers"
	@echo "make stop - Stop the containers"
	@echo "make start - Start the containers"
	@echo "make restart - Restart the containers"
	@echo "make logs - Show the logs"
	@echo "make ps - Show the status of the containers"
	@echo "make exec - Enter the container"
	@echo "make build - Build the containers"
	@echo "make rebuild - Rebuild the containers"
	@echo "make status - Show the status of the containers, images, volumes and networks"
	@echo "make fclean - Stop and remove the containers, images, volumes and networks"

gamefied:
	@echo "Starting the gamefied"
	@echo "Please, wait a moment"
	@echo "Starting the containers"
	@docker-compose -f docker-compose.yml up -d --build
	@echo "Launching the gamefied"
	@python3 -m venv .venv
	@. .venv/bin/activate && pip install -r requirements.txt
	@pip install -r requirements.txt
	@python3 gamefied.py

up:
	docker-compose -f docker-compose.yml up -d --build
	docker-compose up

upd:
	docker-compose -f docker-compose.yml up -d --build

down:
	docker-compose down

stop:
	docker-compose stop

start:
	docker-compose start

restart:
	docker-compose restart

logs:
	docker-compose logs -f

ps:
	docker-compose ps

exec:
	docker-compose exec -it app /bin/bash

build:
	docker-compose build

rebuild:
	docker-compose down
	docker-compose build
	docker-compose up -d

status:
	@echo "\n\033[1;33mContainers\033[0m"
	@docker-compose ps
	@echo "\n\033[1;33mImages\033[0m"
	@docker-compose images
	@echo "\n\033[1;33mVolumes\033[0m"
	@docker volume ls
	@echo "\n\033[1;33mNetworks\033[0m"
	@docker network ls

fclean:
	docker-compose down
	docker-compose rm -f
	docker system prune -a -f
	docker volume prune -f
	docker network prune -f
	-docker volume ls -qf dangling=true | xargs -r docker volume rm