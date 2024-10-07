from fastapi import  FastAPI
from src.schemas import UserCreate, UserRead, UserUpdate
from src.users import auth_backend,  fastapi_users
from fastapi.middleware.cors import CORSMiddleware
from src.routers.article import article_router 
from src.routers.comment import comment_router
from settings import config, swagger_ui_default_parameters
from src.db import Base 
from src.db import engine
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from settings import REDIS_URL,CACHE_PREFIX,CONTACT_EMAIL,CONTACT_NAME,\
    API_DESCRIPTION,API_TITLE,CORS_ORIGIN_URLS,ALLOWED_METHODS




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
        "name": "Company",
        "description": "***Company*** ORM model and it's methods for making CRUD operations. Company - represents company item with data fields.",
        "externalDocs": {
            "description": "Any question?",
            "url": "https://t.me/ewanG808",
        
        
        },

    },
    {
        "name": "Employee",
        "description": "***Employee*** Methods for ORM model that extends User model. Employee - gives additional data structure to user that became as employee. Logically user may change the employment position so someone may substitute **user** on particular position. When particular _user_ is unemployed he has no Employee table...\nThis table extends user which works in the company on a position.",
        "externalDocs": {
            "description": "Any question?",
            "url": "https://t.me/ewanG808",
        
        
        },
    },
]

# OpenAPI  - P R E S E N T A T I O N    D A T A
contact_dict = dict(name=CONTACT_NAME,
                    email=CONTACT_EMAIL,
                                  )


app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    contact=contact_dict,
    openapi_tags=tags_meta,
    swagger_ui_parameters=swagger_ui_default_parameters,
    swagger_ui_init_oauth={"null"},
    swagger_ui_oauth2_redirect_url="/auth/jwt/login",
    )


# CORS SETTINGS

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGIN_URLS,
    allow_credentials=True,
    allow_methods=ALLOWED_METHODS,
    allow_headers=["*"],
)

# Article Router - Imported from module employee.py
app.include_router(
    article_router,tags=['Article Methods']
    )
# Comment Router - cmp.py
app.include_router(
    comment_router,tags=['Comment Methods ']
    )

# users backend
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Login / Logout Methods"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Register User Methods"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Reset Password Methods"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["Veryfy Methods"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["User CRUD Methods"],
)


# @app.get("/drop-create",tags=['Base Migrations Method'])
# async def metadata_route(command:str = None):
#     """Dev usage cludge:
#     For making migrations use this route by writing in command query - create_all | drop_all

#     "details":\n
#                 {
#                 "drop_all": "deletes all tables in database",
#                 "create_all": "creates all tables using Metadata object."
#                 }
#     """
#     if command:
#         match command:
#             case "create_all":
#                 async with engine.begin() as conn:
#                     await conn.run_sync(Base.metadata.create_all)
#             case "drop_all":
#                 async with engine.begin() as conn:
#                     await conn.run_sync(Base.metadata.drop_all)
                    
#     return {"message": f"Hello Word!" }


import importlib
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# REDIS startup
@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix=CACHE_PREFIX)
