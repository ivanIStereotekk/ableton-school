import time
import base64
import subprocess
import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated, Any, Dict
from pydantic import AnyUrl
from typing_extensions import Doc

# the class that imports from .envs
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=['.env.app','.env.postgres','.env.redis'], env_file_encoding='utf-8',extra='allow')

    
config = Settings().model_dump()    
# VARIABLES

# it is a key that used for build or not to build docker compose
PRODUCTION_BUILD = config['production_build']
# while building in docker compose the url gets container or service name that's why it should be interchanged 
PG_HOST = config['postgres_production_url'] if config['production_build'] == 'True' else config['postgres_development_url']
PG_PASS = config['postgres_password']
PG_USER = config['postgres_user']
PG_DB_NAME = config['postgres_db'] if config['production_build'] == 'False' else config['postgres_db_default']
PG_PORT=config['postgres_port']
    # N O T I C E   ---    While building app dev mode this part running "docker run postgres container" outside app
DOCKER_RUN = config['docker_run_pg'] if config['production_build'] == 'False' else config['hello']
result = subprocess.run(str(config['docker_run_pg']), shell=True, \
                            stdout=subprocess.PIPE, encoding='utf-8')  
# this need to wait a little until docker container is up         
print(result.stdout)
time.sleep(5)
# Swagger info on web page
CONTACT_NAME = config['contact_name']
CONTACT_EMAIL = config['contact_email']
API_DESCRIPTION = config['api_description']
API_TITLE = config['api_title']

# REDIS cache
CACHE_EXP = config['cache_exp']
REDIS_URL = config['prod_redis_url'] if config['production_build'] == 'True' else config['dev_redis_url']
CACHE_PREFIX = config['cache_prefix']

# jwt things
JWT_TOKEN_LIFETIME = config['jwt_token_lifetime']
JWT_SECRET_KEY = config['jwt_secret_key']
JWT_ALGORITHM = config['jwt_algorithm']
JWT_TOKEN_LIFETIME = config['jwt_token_lifetime']  

# Password Hashing - Since the beginning that was bytes but i cut b then made it bytes
HASH_CRYPTO_KEY = bytes(config['hash_crypto_key'],'utf-8')
RESET_PASSWORD_SECRET_KEY = bytes(config['reset_password_secret_key'],'utf-8')

# CORS ORIGIN URLS - while development mode is - ['*'] allow all
ORIGIN_URL = config['origin_url']
ORIGIN_PORT = config['origin_port']
FRONT_PORT = config['front_port']
# It's important to change port in compose.yaml while running in docker(production)

CORS_ORIGIN_URLS = [
    f"http://{ORIGIN_URL}",
    f"https://{ORIGIN_URL}/docs",
    f"http://{ORIGIN_URL}",
    f"http://{ORIGIN_URL}:{ORIGIN_PORT}",
    f"http://{ORIGIN_URL}:{FRONT_PORT}",
    'http://localhost:3000/registration',
] #if PRODUCTION_BUILD == 'True' else ['*']

ALLOWED_METHODS = [
    "DELETE", 
    "GET", 
    "HEAD", 
    "OPTIONS", 
    "PATCH", 
    "POST", 
    "PUT"] if PRODUCTION_BUILD == 'True' else ['*']






# OPEN API TAGS

tags_meta = [
    {
        "name": "Users",
        "description": "***User Management Authentication[UMA]*** methods flow. Registration, Authentication, Reset password, typical UMA user flow.",
        "externalDocs": {
            "description": "Any question?",
            "url": "https://t.me/ewanG808",
        
        },

    },
    {
        "name": "Article",
        "description": "***Article*** ORM model and it's methods for making CRUD operations.",


    },
    {
        "name": "Comment",
        "description": "***Comment*** Methods for ORM model.",

    },
]


swagger_ui_default_parameters: Annotated[
    Dict[str, Any],
    Doc(
        """
        Default configurations for Swagger UI.
        """
    ),
] = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": False,
    "showExtensions": True,
    "showCommonExtensions": True,
    "syntaxHighlight.theme": "obsidian"
}
