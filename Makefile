APP_NAME=cs50chain
APP_DIR=/${APP_NAME}/app
DOCKER_BASE_IMAGE=python:3.10
COMMAND?=bash
PORT=5000

# text colors https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux
BOLD_YELLOW=\033[1;33m
COLOR_OFF=\033[0m

welcome:
	@clear
	@echo "${BOLD_YELLOW}"
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
	@echo "${BOLD_YELLOW}removing containers${COLOR_OFF}"
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

docker-migration: welcome
	@docker run -it \
		-v $(shell pwd):/root/db --workdir /root/db \
		--rm \
		--name sqlite \
		nouchka/sqlite3 \
		database.db -init migration/20220612034805__create_blockchain_table.sql

docker-debug: welcome
	@echo "${BOLD_YELLOW}debug mode${COLOR_OFF}"
	@make docker-command

docker-run: welcome
	@echo "${BOLD_YELLOW}running app${COLOR_OFF}"
	@make docker-command COMMAND="python3 app.py"

docker-test: welcome
	@echo "${BOLD_YELLOW}testing app${COLOR_OFF}"
	@make docker-command \
		APP_NAME=${APP_NAME}-test \
		PORT=4999 \
		COMMAND="coverage run -m unittest discover && \
			coverage report && \
			coverage html"
	@echo "${BOLD_YELLOW}$(shell date)${COLOR_OFF}"
	@echo "${BOLD_YELLOW}coverage report at htmlcov/index.html${COLOR_OFF}"

ip:
	@docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" ${APP_NAME}
