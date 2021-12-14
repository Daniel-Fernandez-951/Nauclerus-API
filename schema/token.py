from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from schema.tokenSchema import TokenData
import os


basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = str(os.environ.get("SECRET_KEY"))
ALGORITHM = "HS256"
TOKEN_TTL_EXPIRE_MINUTES = 52 or int(os.environ.get("TOKEN_TTL_EXPIRE_MINUTES"))


def create_access_token(data: dict,
                        expires_delta: Optional[timedelta] = None):
    to_encode: dict = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=TOKEN_TTL_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get("sub")
        pilot_id: str = payload.get("id")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email,
                               pilot_id=pilot_id)
        return token_data
    except JWTError:
        raise credentials_exception
