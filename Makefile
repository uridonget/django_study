all : up

up :
	docker-compose -f srcs/docker-compose.yml up --build

down :
	docker-compose -f srcs/docker-compose.yml down

clean : down
	docker stop $$(docker ps -q); \
	docker image rmi -f $$(docker image ls -q); \
	docker volume rm $$(docker volume ls -q); \
	docker builder prune -f

.PHONY : all up down clean