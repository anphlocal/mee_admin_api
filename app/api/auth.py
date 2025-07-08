from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from app.core.security import get_password_hash, verify_password, create_access_token
from app.db.database import SessionLocal
from app.core.config import settings
from datetime import timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from fastapi import Request
from app.core.helpers import get_current_user
from app.core.helpers import APIResponse
from app.enums.status_code import ResponseCode
from app.core.db_session import DBSession
from app.core.helpers import APIException

router = APIRouter(prefix="/auth", tags=["auth"])

http_bearer = HTTPBearer()

# Đăng ký tài khoản
@router.post("/register", response_model=APIResponse)
async def register(user: UserCreate, db: Session = Depends(DBSession.dependency)):
    try:
        db_user = db.query(User).filter((User.username == user.username) | (User.email == user.email)).first()
        if db_user:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Tài khoản đã tồn tại trên hệ thống"
            )
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return APIResponse(data=UserRead.model_validate(new_user))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

# Đăng nhập
@router.post("/login")
async def login(user: UserCreate, db: Session = Depends(DBSession.dependency)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if not db_user or db_user.deleted_at is not None:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Tài khoản đã bị khóa hoặc không tồn tại"
            )
        if not verify_password(user.password, db_user.hashed_password):
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Tài khoản hoặc mật khẩu không chính xác"
            )
        access_token = create_access_token(
            data={"sub": db_user.username},
            expires_delta=timedelta(minutes=30)
        )
        return APIResponse(data={"access_token": access_token, "token_type": "bearer"})
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

# Làm mới token
@router.post("/refresh-token")
async def refresh_token(request: Request, db: Session = Depends(DBSession.dependency)):
    try:
        token = request.headers.get("authorization")
        if not token or not token.startswith("Bearer "):
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Token không hợp lệ"
            )
        token = token.split(" ", 1)[1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False})
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
        if not user:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Tài khoản không tồn tại"
            )
        new_token = create_access_token(data={"sub": user.username})
        return APIResponse(data={"access_token": new_token, "token_type": "bearer"})
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

# Lấy thông tin tài khoản
@router.get("/me", response_model=UserRead)
async def me(credentials: HTTPAuthorizationCredentials = Depends(http_bearer), db: Session = Depends(DBSession.dependency)):
    try:
        token = credentials.credentials
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
        if not user:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Tài khoản không tồn tại"
            )
        return APIResponse(data=UserRead.model_validate(user))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )
