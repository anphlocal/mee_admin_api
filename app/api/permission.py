from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionRead, PermissionUpdate
from app.core.helpers import APIResponse, APIException
from app.enums.status_code import ResponseCode
from app.core.db_session import DBSession
from typing import List

router = APIRouter(prefix="/permission", tags=["permission"])

@router.post("/", response_model=APIResponse)
async def create_permission(permission: PermissionCreate, db: Session = Depends(DBSession.dependency)):
    try:
        db_permission = db.query(Permission).filter(Permission.name == permission.name).first()
        if db_permission:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Permission đã tồn tại"
            )
        new_permission = Permission(name=permission.name, description=permission.description)
        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)
        return APIResponse(data=PermissionRead.model_validate(new_permission))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.get("/", response_model=APIResponse)
async def list_permissions(db: Session = Depends(DBSession.dependency)):
    try:
        permissions = db.query(Permission).all()
        return APIResponse(data=[PermissionRead.model_validate(p) for p in permissions])
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.get("/{permission_id}", response_model=APIResponse)
async def get_permission(permission_id: int, db: Session = Depends(DBSession.dependency)):
    try:
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Permission không tồn tại"
            )
        return APIResponse(data=PermissionRead.model_validate(permission))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.put("/{permission_id}", response_model=APIResponse)
async def update_permission(permission_id: int, permission: PermissionUpdate, db: Session = Depends(DBSession.dependency)):
    try:
        db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not db_permission:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Permission không tồn tại"
            )
        db_permission.name = permission.name  # type: ignore
        db_permission.description = permission.description  # type: ignore
        db.commit()
        db.refresh(db_permission)
        return APIResponse(data=PermissionRead.model_validate(db_permission))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.delete("/{permission_id}", response_model=APIResponse)
async def delete_permission(permission_id: int, db: Session = Depends(DBSession.dependency)):
    try:
        db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not db_permission:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Permission không tồn tại"
            )
        db.delete(db_permission)
        db.commit()
        return APIResponse(data=True)
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        ) 