** Users management **

> [!NOTE]
> Backend for Ableton school ( В процессе разработки ).
> Можно запустить !

### Auth User App - Микросервис 
### environment variables are forbidden in Git Repositories so make env files by yourself then copy/past content.

### .env.app
```.env

# Open API inform
PRODUCTION_BUILD = True
CONTACT_NAME = 'Ivan Goncharov'
CONTACT_EMAIL = 'ivan.stereotekk@gmail.com'
API_TITLE = 'Ableton Live School - Backend App'
API_DESCRIPTION ='Ableton School API'
# Password hashing base64 -  Fernet.generate_key()
HASH_CRYPTO_KEY ='aAGKiORWZxJc8vwnuE4xKmTkFNPK8k_UiYVkOBdWGoA='
RESET_PASSWORD_SECRET_KEY = '7TZx6EmUG8k4HJ4c7p6NHhBZw-cs1PuEBBVyp28ENik='
# J W T 
JWT_TOKEN_LIFETIME = 3600
JWT_SECRET_KEY = e8cd77e6d45d7aa887a1a81d13512e135d9dbe9a62d16c3ee73bc51e2bb00c3f
JWT_TOKEN_LIFETIME = 10080
JWT_ALGORITHM = "HS256"

# CORS ORIGIN URL:PORT
ORIGIN_URL = localhost
ORIGIN_PORT = 8000

```

### .env.postgres

```.env
POSTGRES_PRODUCTION_URL = postgres_db
POSTGRES_DEVELOPMENT_URL = localhost
POSTGRES_PASSWORD = secret123
POSTGRES_USER = postgres
# Inner Postgres option: If it is not specified, then the value of POSTGRES_USER will be used.
POSTGRES_DB = xdb #database name look in the docker run command POSTGRES_DB
POSTGRES_DB_DEFAULT = postgres
POSTGRES_PORT = 5432
# This command  will run docker container while running app
DOCKER_RUN_PG = 'docker run -it --name postgres_dev -e POSTGRES_DB=xdb -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=secret123 -p 5432:5432 -d postgres:latest'


```

### .env.redis

```.env

CACHE_EXP = 90
LOCAL_REDIS_URL = 'redis://localhost'
CACHE_PREFIX = 'veles-app'
DEV_REDIS_URL = 'redis://localhost'
PROD_REDIS_URL = 'redis://redis_cache'
CACHE_EXP = 3600
CACHE_PREFIX = 'Veles-app:'

```
#### Если возникнет желание запустить:
- создайте в папке проекта файлы: .env.app | .env.postgres | .env.redis 
- скопируйте переменные окружения из текущего файла согласно секциям которые видите
- перейдите в директорию и запустите docker compose up --build
- подождите сборку и запуск
- проект проверен,запускается и исправно работает (MAC OS)

