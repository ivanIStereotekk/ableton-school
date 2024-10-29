import uuid
from typing import Optional
from settings import JWT_SECRET_KEY, JWT_TOKEN_LIFETIME,RESET_PASSWORD_SECRET_KEY, HASH_CRYPTO_KEY
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from src.db import User, get_user_db

# Token generating

# token lifetime
lifetime_seconds = int(JWT_TOKEN_LIFETIME)
# Password management
class UserManager(IntegerIDMixin, BaseUserManager[User,int]):
    reset_password_token_secret = RESET_PASSWORD_SECRET_KEY
    verification_token_secret = HASH_CRYPTO_KEY

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=JWT_SECRET_KEY, lifetime_seconds=lifetime_seconds)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int ](get_user_manager, [auth_backend]) # or int added


#simple active user
current_active_user = fastapi_users.current_user(active=True)

# super user
current_superuser = fastapi_users.current_user(active=True, superuser=True)

