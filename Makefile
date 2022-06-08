APP_NAME=cs50x-blockchain
APP_DIR=/${APP_NAME}/app
DOCKER_BASE_IMAGE=python:3.10
COMMAND?=bash

# text colors
YELLOW=\e[1m\033[33m
COLOR_OFF=\e[0m

welcome:
	@clear
	@echo "${YELLOW}"
	@echo " ██████╗ ██████╗███████╗ ██████╗  ██████╗██╗  ██╗ █████╗ ██╗███╗   ██╗" && sleep .02
	@echo "██╔════╝██╔════╝██╔════╝██╔═████╗██╔════╝██║  ██║██╔══██╗██║████╗  ██║" && sleep .02
	@echo "██║     ███████╗███████╗██║██╔██║██║     ███████║███████║██║██╔██╗ ██║" && sleep .02
	@echo "██║     ╚════██║╚════██║████╔╝██║██║     ██╔══██║██╔══██║██║██║╚██╗██║" && sleep .02
	@echo "╚██████╗██████╔╝███████║╚██████╔╝╚██████╗██║  ██║██║  ██║██║██║ ╚████║" && sleep .02
	@echo " ╚═════╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝" && sleep .02
	@echo "${NOCOLOR}"
	@# http://patorjk.com/software/taag font ANSI Shadow

remove-containers:
ifneq ($(shell docker ps -a --filter "name=${APP_NAME}" -aq 2> /dev/null | wc -l | bc), 0)
	@echo "${YELLOW}removing containers${COLOR_OFF}"
	@docker ps -a --filter "name=${APP_NAME}" -aq | xargs docker rm -f
endif

docker-command: remove-containers
	@docker run -it -v $(shell pwd):${APP_DIR} -w ${APP_DIR} \
		--name ${APP_NAME} \
		--env-file .env \
		-p 5000:5000 \
		${DOCKER_BASE_IMAGE} bash -c "\
			python3 -m pip install --upgrade pip && \
			pip3 install -r requirements.txt && \
			${COMMAND}"

docker-debug: welcome
	@echo "${YELLOW}debug mode${COLOR_OFF}"
	@make docker-command

docker-test: welcome
	@echo "${YELLOW}tests${COLOR_OFF}"
	@make docker-command COMMAND="\
		pip3 install -r requirements.txt && \
		python3 -m unittest -v"

ip:
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${APP_NAME}
