# Решение для тестового задания: https://sugary-tax-511.notion.site/8ab7671af4c3493f8cb120d7619f7c8e

## Как запустить проект:
## bakend
1. Зайти в папку backend
2. Создать файл .env
3. Заполнить полями:
DJANGO_KEY=YUIR_KEY
DB_USER=YOU_USER
DB_PASSWORD=YOU_PASSWORD
DB_HOST=localhost
DB_PORT=5432
DB_NAME=todo
4. Создать сеть в докере: docker network create backend_network
5. Поднять компоуз: docker-compose up --build -d
6. Чтобы остановить контейнер: docker-compose stop или docker-compose down

###
После того, как был поднят контейнер, будут доступны url-ы:
**127.0.0.1:8000/admin --- админ панель, чтобы войти, нужно написать:
login: admin
password: adminpass

**127.0.0.1:8000/api/docs --- документация со всеми эндпоинтами

## microservice
1. Зайти в папку microservice
2. Создать файл .env
3. Заполнить полями:
WEB_HOST=localhost
WEB_PORT=8080
DEBUG=True
BACKEND_API_URL=http://django-app:8000
DB_HOST=localhost
DB_PORT=5432
DB_NAME=microservice_todo
DB_USER=YOU_USER
DB_PASSWORD=YOU_PASSWORD
DB_DRIVER=postgresql+asyncpg
REDIS_HOST=localhost
REDIS_PORT=6379

4. Создать файл alembic.ini:
1) alembic init alembic
2) В script_location поменять на: src/infrastructure/postgres/migrations
3) в sqlalchemy.url = postgresql+asyncpg://YOU_DATABASE_USER:YOU_DATABASE_PASSWORD@localhost:5432/microservice_todo

5. Поднять компоуз: docker-compose up --build -d
6. Чтобы остановить контейнер: docker-compose stop или docker-compose down

Далее перейти на 127.0.0.1:8080/docs, где будут показаны все эндпоинты

### tb_bot
1. Перейти в папку tg_bot
2. Создать файл .env
3. Заполнить полями:
TOKEN_BOT=YOU_TOKEN
BACKEND_URL=http://django-app:8000
MICROSERVICE_URL=http://fastapi-app:8080
4. Поднять компоуз: docker-compose up --build -d
5. Чтобы остановить контейнер: docker-compose stop или docker-compose down
6. Далее перейти в своего бота и нажать на /start
7. После чего будут доступны команды:
/add_tasks --- добавляет задачу
/tasks --- просматривает текущие задачи пользователя

## Трудности возникшие при решении тестового:
** Как таковых сложностей не было, обычный CRUD, со связью тг-бота через REST-http
