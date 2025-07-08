from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate, RoleRead, RoleUpdate
from app.core.helpers import APIResponse, APIException
from app.enums.status_code import ResponseCode
from app.core.db_session import DBSession
from typing import List
from app.models.permission import Permission
from app.schemas.permission import PermissionRead

router = APIRouter(prefix="/role", tags=["role"])

@router.post("/", response_model=APIResponse)
async def create_role(role: RoleCreate, db: Session = Depends(DBSession.dependency)):
    try:
        db_role = db.query(Role).filter(Role.name == role.name).first()
        if db_role:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Role đã tồn tại"
            )
        new_role = Role(name=role.name, description=role.description)
        db.add(new_role)
        db.commit()
        db.refresh(new_role)
        return APIResponse(data=RoleRead.model_validate(new_role))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.get("/", response_model=APIResponse)
async def list_roles(db: Session = Depends(DBSession.dependency)):
    try:
        roles = db.query(Role).all()
        return APIResponse(data=[RoleRead.model_validate(r) for r in roles])
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.get("/{role_id}", response_model=APIResponse)
async def get_role(role_id: int, db: Session = Depends(DBSession.dependency)):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Role không tồn tại"
            )
        return APIResponse(data=RoleRead.model_validate(role))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.put("/{role_id}", response_model=APIResponse)
async def update_role(role_id: int, role: RoleUpdate, db: Session = Depends(DBSession.dependency)):
    try:
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Role không tồn tại"
            )
        db_role.name = role.name  # type: ignore
        db_role.description = role.description  # type: ignore
        db.commit()
        db.refresh(db_role)
        return APIResponse(data=RoleRead.model_validate(db_role))
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

@router.delete("/{role_id}", response_model=APIResponse)
async def delete_role(role_id: int, db: Session = Depends(DBSession.dependency)):
    try:
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Role không tồn tại"
            )
        db.delete(db_role)
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

# Gán permission cho role
@router.post("/{role_id}/permissions/{permission_id}", response_model=APIResponse)
async def add_permission_to_role(role_id: int, permission_id: int, db: Session = Depends(DBSession.dependency)):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Role không tồn tại"
            )
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Permission không tồn tại"
            )
        if permission in role.permissions:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Permission đã được gán cho role này"
            )
        role.permissions.append(permission)
        db.commit()
        db.refresh(role)
        return APIResponse(data=[PermissionRead.model_validate(p) for p in role.permissions])
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

# Huỷ gán permission khỏi role
@router.delete("/{role_id}/permissions/{permission_id}", response_model=APIResponse)
async def remove_permission_from_role(role_id: int, permission_id: int, db: Session = Depends(DBSession.dependency)):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Role không tồn tại"
            )
        permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Permission không tồn tại"
            )
        if permission not in role.permissions:
            raise APIException(
                code=ResponseCode.UNAUTHORIZED,
                message="Permission chưa được gán cho role này"
            )
        role.permissions.remove(permission)
        db.commit()
        db.refresh(role)
        return APIResponse(data=[PermissionRead.model_validate(p) for p in role.permissions])
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        )

# Lấy danh sách permission của role
@router.get("/{role_id}/permissions", response_model=APIResponse)
async def get_permissions_of_role(role_id: int, db: Session = Depends(DBSession.dependency)):
    try:
        role = db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise APIException(
                code=ResponseCode.NOT_FOUND,
                message="Role không tồn tại"
            )
        return APIResponse(data=[PermissionRead.model_validate(p) for p in role.permissions])
    except APIException:
        raise
    except Exception:
        raise APIException(
            code=ResponseCode.INTERNAL_ERROR,
            message="Lỗi hệ thống",
            data=None
        ) 