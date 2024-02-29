all:
	@echo "make up"
	@echo "make upd"
	@echo "make down"
	@echo "make stop"
	@echo "make start"
	@echo "make restart"
	@echo "make logs"
	@echo "make ps"
	@echo "make exec"
	@echo "make build"
	@echo "make rebuild"
	@echo "make status"

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