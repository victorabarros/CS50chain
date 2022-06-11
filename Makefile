APP_NAME=cs50chain
APP_DIR=/${APP_NAME}/app
DOCKER_BASE_IMAGE=python:3.10
COMMAND?=bash
PORT=5000

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
		-p ${PORT}:5000 \
		${DOCKER_BASE_IMAGE} bash -c "\
			pip3 install -r requirements.txt && \
			${COMMAND}"

docker-debug: welcome
	@echo "${YELLOW}debug mode${COLOR_OFF}"
	@make docker-command

docker-run: welcome
	@echo "${YELLOW}running app${COLOR_OFF}"
	@make docker-command COMMAND="python3 app.py"

docker-test: welcome
	@echo "${YELLOW}testing app${COLOR_OFF}"
	@make docker-command APP_NAME=${APP_NAME}-test PORT=4999 COMMAND="python3 -m unittest -v"

ip:
	@docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ${APP_NAME}
