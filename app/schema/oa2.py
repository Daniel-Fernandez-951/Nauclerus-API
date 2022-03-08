from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.schema.token import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credential validation failed",
        headers={"WWW-Authenticate": "bearer"},
    )
    return verify_token(token,
                        credentials_exception=credentials_exception)
