all:
	echo "Hello, Make!"

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