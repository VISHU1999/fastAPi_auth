
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from http import HTTPStatus as status_code

from schemas.users import TokenPayload
from fastapi import HTTPException, Request

from models.users import User
from services.db import users as user_db_services
from db_initializer import SessionLocal
import settings
from jose import jwt
from datetime import datetime, timedelta



class JWTBearer(HTTPBearer):
    """JWT verify class"""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(
            request
        )
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not await self.verify_jwt(credentials.credentials, request):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
            )

    async def verify_jwt(
        self, token: str, request: Request, secret_key: str = settings.SECRET_KEY
    ):
        """Verifying JWT token exp time and check valid user"""
        try:
            token = token.split()[1]
            payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
            token_data = TokenPayload(**payload)

            if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
                raise HTTPException(
                    status_code=status_code.UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status_code.FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = user_db_services.get_user(session=SessionLocal(), email=token_data.email)

        if user is None:
            raise HTTPException(
                status_code=status_code.NOT_FOUND,
                detail="Invalid User",
            )

        return token_data

        
        