APP_NAME=cs50x-blockchain
APP_DIR=/${APP_NAME}/app
DOCKER_BASE_IMAGE=python:3.10-alpine
COMMAND?=sh

# text colors
YELLOW=\e[1m\033[33m
COLOR_OFF=\e[0m

remove-containers:
ifneq ($(shell docker ps -a --filter "name=${APP_NAME}" -aq 2> /dev/null | wc -l | bc), 0)
	@echo "${YELLOW}Removing containers${COLOR_OFF}"
	@docker ps -a --filter "name=${APP_NAME}" -aq | xargs docker rm -f
endif

docker-command: remove-containers
	@echo "${YELLOW}Initiating container ${APP_NAME}${COLOR_OFF}"
	@docker run -it -v $(shell pwd):${APP_DIR} -w ${APP_DIR} \
		--name ${APP_NAME} \
		${DOCKER_BASE_IMAGE} sh -c "pip3 install -r requirements.txt && ${COMMAND}"
