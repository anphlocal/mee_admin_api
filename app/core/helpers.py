from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Any, Optional
from app.enums.status_code import ResponseCode
from app.models.user import User
from app.schemas.user import UserRead

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(SessionLocal)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Token không hợp lệ"
            )
    except JWTError:
        raise APIException(
            code=ResponseCode.UNAUTHORIZED,
            message="Token không hợp lệ"
        )
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise APIException(
            code=ResponseCode.UNAUTHORIZED,
            message="Tài khoản không tồn tại"
        )
    return APIResponse(data=UserRead.model_validate(user))

class APIResponse(BaseModel):
    code: int = ResponseCode.SUCCESS
    message: str = "Success"
    data: Optional[Any] = None

class APIException(HTTPException):
    def __init__(self, code: int, message: str, data: Any = None, status_code: int = 400):
        super().__init__(
            status_code=status_code,
            detail=APIResponse(
                code=code,
                message=message,
                data=data
            ).model_dump()
        )

    