all: build up

build:
	docker-compose -f myproject/docker-compose.yml build

up:
	docker-compose -f myproject/docker-compose.yml up

down:
	docker-compose -f myproject/docker-compose.yml down

clean: down
	docker stop $$(docker ps -q); \
	docker image rmi -f $$(docker image ls -q); \
	docker volume rm $$(docker volume ls -q); \
	docker builder prune -f

.PHONY: all build up down clean