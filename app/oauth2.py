from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(user_information: dict):
    encode = user_information.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp": expire})

    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    return token


def verify_access_token(token, credentials_exception):
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = token_data.get("user_id")

        if not user_id:
            raise credentials_exception

        validated_token = schemas.TokenData(id=user_id)

    except JWTError:
        raise credentials_exception

    return validated_token


def get_current_user(token=Depends(oauth2_schema), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
