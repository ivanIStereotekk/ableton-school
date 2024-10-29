
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel, Field, Json
from starlette.responses import JSONResponse
from src.users import *
from sqlalchemy.exc import SQLAlchemyError
from src.models import User, Comment
from starlette import status
from src.users import current_active_user,current_superuser
from src.db import AsyncSession, get_async_session
from src.schemas import CommentCreate,CommentRead,ListComments
from sqlalchemy import select, update
from starlette import status
from src.custom_responses import *
import json
from sqlalchemy import bindparam
import datetime


comment_router = APIRouter(
    prefix="/comment",
    responses=ROUTER_API_RESPONSES_OPEN_API,
)


@comment_router.post("/add",response_class=CustomizedORJSONResponse)
async def create_comment(
    comment: CommentCreate,
    user: User = Depends(current_active_user),      
    session: AsyncSession = Depends(get_async_session),
    ):
    try:
        if comment: 
            new_comment = Comment(
            author_id=user.id,
            # article_id= comment.article_id,
            # body_text= comment.body_text,
            # picture=comment.picture,
            )
            new_comment.__dict__.update(comment.__dict__)
            session.add(new_comment)
            await session.commit()
            return CustomizedORJSONResponse(content={"detail": "created"},status_code=status.HTTP_201_CREATED)
    except SQLAlchemyError as e:
        return CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content=str(e))






@comment_router.delete(
        "/delete/{comment_id}",
        summary="Summary Of Comment",
        response_class=CustomizedORJSONResponse,
        )
async def delete_comment(
    comment_id: int,
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    ):

    try:
        if user and comment_id:
            del_comment = await session.get(Comment, comment_id)
            if del_comment and del_comment.id == comment_id:
                await session.delete(del_comment)
                await session.commit()
                return CustomizedORJSONResponse(status_code=status.HTTP_202_ACCEPTED,content={"detail":"deleted"})
            else:
                return CustomizedORJSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"detail":"not found"})

    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        return CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e)})




@comment_router.get("/all",response_model=ListComments)
async def get_comments_all(
    user: User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session),
    ):
    try:
        if user:
            statement = select(Comment).limit(100)
            result = await session.execute(statement=statement)
            comments = dict(data=result.scalars().all())
            if comments:
                return comments
                #return CustomizedORJSONResponse(status_code=status.HTTP_200_OK,content=str({"data":articles}),background=None)
    except SQLAlchemyError as e:                            # <<<< later will do e  to logger
        raise CustomizedORJSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"detail":str(e._message)},background=None)
