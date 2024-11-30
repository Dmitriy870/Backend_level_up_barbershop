from fastapi import Cookie, Depends, Header, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db_helper import db_helper
from app.models.user import User

from . import jwt
from .shemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    authorization: str = Header(None),
    access_token: str = Cookie(None),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    elif access_token:
        token = access_token

    if not token:
        raise credentials_exception

    token_data: TokenData = await jwt.verify_token(
        token, credentials_exception, session
    )

    stmt = Select(User).where(User.id == token_data.user_id)
    result = await session.execute(stmt)
    user = result.scalars().first()

    if user is None:
        raise credentials_exception

    return user


async def get_current_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
        )
    return current_user