from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception: Exception):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM,
            ],
        )
        user_email: str = payload.get("user_email")

        if user_email is None:
            raise credentials_exception

        token_data = schemas.TokenData(user_email=user_email)
    except jwt.PyJWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credetials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token=token, credentials_exception=credetials_exception)

    stmt = select(models.User).where(models.User.email == token.user_email)
    user = db.execute(stmt).scalar_one_or_none()

    return user
