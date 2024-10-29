import uuid
from typing import Optional,Union,AnyStr,Any,List,Dict
from datetime import datetime, date
from fastapi_users import schemas
from pydantic import field_validator,Field,Json


from pydantic import (
    ValidationInfo,
    field_validator,
    BaseModel,
    Field,
    EmailStr,
)



# Base User
class UserRead(schemas.BaseUser[int]):
    firstname: str 
    lastname: str 
    email: str
    phone: str
    picture: str | None
    birth_date: date


class UserCreate(schemas.BaseUserCreate):
    firstname: str = Field()
    lastname: str = Field()
    email: str = Field()
    phone: str = Field()
    picture: str = Field(default=None)
    birth_date: date | None
    password: str = Field()
    @field_validator('phone')
    @classmethod
    def check_numeric(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            is_numeric = v.replace(' ', '').isnumeric()
            assert is_numeric, f'{info.field_name} phone number must be numeric'
        return v





class UserUpdate(BaseModel):
    firstname: Optional[str] = Field()
    lastname: Optional[str] = Field()
    email: Optional[str] = Field()
    phone: Optional[str] = Field()
    picture: Optional[str] = Field()
    birth_date: date | None
    @field_validator('phone')
    @classmethod
    def check_numeric(cls, v: str, info: ValidationInfo) -> str:
        if isinstance(v, str):
            is_numeric = v.replace(' ', '').isnumeric()
            assert is_numeric, f'{info.field_name} phone number must be numeric'
        return v
    
 


# A R T I C L E     S C H E M A S

class ArticleRead(BaseModel):
    id: int
    position_id: int
    subject: str
    title: str
    article: str
    picture: str



class ArticleCreate(BaseModel):
    position_id: Optional[int] = Field()
    subject: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    article: Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)

class ListArticles(BaseModel):
    data: List[ArticleRead]

# C O M M E N T   S C H E M A S


class CommentRead(BaseModel):
    id: int
    author_id: int
    article_id: int
    post_time: datetime
    body_text: str
    picture: str


class CommentCreate(BaseModel):
    article_id: Optional[int] = Field(default=None)
    body_text: Optional[str] = Field(default=None)
    picture: Optional[str] = Field(default=None)


class ListComments(BaseModel):
    data: List[CommentRead]