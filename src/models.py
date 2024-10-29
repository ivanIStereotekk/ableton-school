from typing import Optional,List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from fastapi_users.db import SQLAlchemyBaseUserTable
from settings import *
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy import String, Date, ForeignKey,LargeBinary,Integer,Boolean, DateTime
from datetime import date
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
import uuid
import json

Base: DeclarativeMeta = declarative_base()

UUID_ID = uuid.UUID


class User(SQLAlchemyBaseUserTable[int],Base):
    """
    User table with obvious and visible fields and options.
    
    """
    __tablename__ = 'user_table'
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    firstname: Mapped[str] = mapped_column(String,nullable=False)
    lastname: Mapped[str] = mapped_column(String,nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True,nullable=False)
    phone: Mapped[str] = mapped_column(String,unique=True, nullable=False)
    picture: Mapped[str] = mapped_column(String,nullable=True)
    birth_date: Mapped[date] = mapped_column(Date,nullable=True) 
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self):
        return f" id={self.id} firstname= {self.firstname} lastname={self.lastname}"



class Article(Base):
    """ Article Model:

    """
    __tablename__ = 'article_table'
    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    position_id: Mapped[int] = mapped_column(Integer,unique=True)
    subject: Mapped[str] = mapped_column(String,nullable=True) # add enum later
    title: Mapped[str] = mapped_column(String,nullable=True)
    article: Mapped[str] = mapped_column(String,nullable=True)
    picture: Mapped[str] = mapped_column(String,nullable=True)
    
    def __repr__(self):
        return f"id={self.id}   position_id={self.position_id} title={self.title}"
    
class Comment(Base):
    """ Comment Model:

    """
    __tablename__ = 'comment_table'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    article_id: Mapped[int] = mapped_column(ForeignKey("article_table.id"))
    post_time: Mapped[date] = mapped_column(DateTime(timezone=True),server_default=func.now())
    body_text: Mapped[str] = mapped_column(String,nullable=True)
    picture: Mapped[str] = mapped_column(String,nullable=True)
    
    def __repr__(self):
        return f"id={self.id}  author_id={self.author_id} time={self.post_time}"
    
    