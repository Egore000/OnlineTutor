include .env

DC = docker-compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env.docker
APP_FILE = docker-compose.yaml
APP_CONTAINER = ${PROJECTNAME}_app
DB_CONTAINER = ${PROJECTNAME}_db
RUN_COMMAND = ${EXEC} ${APP_CONTAINER} bash -c

# Сборка и запуск контейнеров
.PHONY: build
build:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

# Запуск контейнеров с логами
.PHONY: start
start:
	${DC} -f ${APP_FILE} ${ENV} up

# Запуск контейнеров в фоновом режиме
.PHONY: up
up:
	${DC} -f ${APP_FILE} ${ENV} up -d

# Остановка и удаление контейнеров
.PHONY: down
down:
	${DC} -f ${APP_FILE} down

# Перезапуск контейнеров
.PHONY: restart
restart:
	make down && make up

# Подключение к контейнеру приложения
.PHONY: shell
shell:
	${EXEC} ${APP_CONTAINER} bash

# Вывод логов приложения
.PHONY: logs
logs:
	${LOGS} ${APP_CONTAINER} -f

# Выполнение команды внутри контейнера приложения
.PHONY: run
run:
	${RUN_COMMAND} "$(COMMAND)"

# Создание миграции базы данных
.PHONY: migration
migration:
	${RUN_COMMAND} "alembic revision --autogenerate -m \"$(NAME)\""

# Применение миграций базы данных
.PHONY: migrate
migrate:
	${RUN_COMMAND} "alembic upgrade head"

# Отмена последней миграции БД
.PHONY: downgrade
downgrade:
	${RUN_COMMAND} "alembic downgrade -1"

# Запуск тестов
.PHONY: test
test:
	${RUN_COMMAND} "pytest"

# Подключение к базе данных
.PHONY: db
db:
	${EXEC} ${DB_CONTAINER} psql -U ${DB_USER} -d ${DB_NAME}

# Логи базы данных
.PHONY: dblogs
dblogs:
	${LOGS} ${DB_CONTAINER} -f

# Локальное юнит-тестирование
.PHONY: test-unit
test-unit:
	pytest -m unit

# Локальное интеграционное тестирование
.PHONY: test-int:
test-int:
	pytest -m integration

# Покрытие тестами
.PHONY: test-cov
test-cov:
	pytest --cov=app --cov-report=term-missing
