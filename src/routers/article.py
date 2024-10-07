from fastapi import APIRouter, Depends, HTTPException, Response, Request
from starlette.responses import JSONResponse
from src.users import *
from fastapi import APIRouter, Depends, HTTPException
from src.users import fastapi_users
from sqlalchemy.exc import SQLAlchemyError
from src.models import User, Article
from starlette import status
from src.users import current_active_user ,current_superuser
from src.schemas import ArticleCreate, ArticleRead,ListArticles
from src.db import AsyncSession, get_async_session
from sqlalchemy import select, update
from starlette import status
from fastapi_cache.decorator import cache as cache_decorator
from fastapi_redis_cache import cache_one_minute
from src.custom_responses import CustomizedORJSONResponse, ROUTER_API_RESPONSES_OPEN_API


current_user = fastapi_users.current_user(active=True)

article_router = APIRouter(prefix="/article",
    responses=ROUTER_API_RESPONSES_OPEN_API
)




@article_router.post("/add",response_class=CustomizedORJSONResponse)
async def create_article(
    article: ArticleCreate,
    user: User = Depends(current_active_user), # T E M P O R A R Y implementation are current_userlater it should do superuser
    # user: User = Depends(current_active_user)     
    session: AsyncSession = Depends(get_async_session),
    ):
    try:
        if article: # temporary check
            new_article = Article(
                  position_id = article.position_id,
                  subject = article.subject,
                  title = article.title,
                  article = article.article,
                  picture = article.picture
            )
            session.add(new_article)
            await session.commit()
        return new_article
    except SQLAlchemyError as e:
        return e    




@article_router.put("/update/{article_id}")
async def update_article(
    article_id: int,
    article: ArticleCreate,
    user: User = Depends(current_active_user), 
    # user: User = Depends(current_superuser)
    session: AsyncSession = Depends(get_async_session),
    ):

    try:
        if user:
            statement = update(
            Article).where(
                Article.id == article_id).values(
                  position_id = article.position_id,
                  subject = article.subject,
                  title = article.title,
                  article = article.article,
                  picture = article.picture
                )
            await session.execute(statement)
            await session.commit()
            return CustomizedORJSONResponse(content={"detail":"created"},status_code=status.HTTP_201_CREATED,background=None)
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)},background=None)
    # return Response(status_code=201)



# DELETE COMPANY

@article_router.delete("/delete/{article_id}")
async def delete_article(
    article_id: int,
    user: User = Depends(current_active_user), # T E M P O R A R Y - only superuser may update Employee
    session: AsyncSession = Depends(get_async_session),
    ):
    try:
        if user and article_id:
            del_article = await session.get(Article, article_id)
            if del_article:
                await session.delete(del_article)
                await session.commit()
            elif not del_article:
                return CustomizedORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"detail":"not found"},background=None) # Logger binding with background param
            return CustomizedORJSONResponse(status_code=status.HTTP_201_CREATED,content={"detail":"created"})            
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)})
    


@article_router.get("/get/{article_id}",response_model=ArticleRead)
async def get_article_id(
    article_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    ):
    try:
        if user and article_id:
            article = await session.get(Article, article_id)
            if article:
                return article
                # return CustomizedORJSONResponse(status_code=status.HTTP_200_OK,content={"detail":article},background=None)
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)},background=None)


# Response.background = logger


@article_router.get("/all",response_model=ListArticles)
async def get_article_all(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    ):
    try:
        if user:
            statement = select(Article).limit(100)
            result = await session.execute(statement=statement)
            articles = dict(data=result.scalars().all())
            if articles:
                return articles
                #return CustomizedORJSONResponse(status_code=status.HTTP_200_OK,content=str({"data":articles}),background=None)
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)},background=None)



