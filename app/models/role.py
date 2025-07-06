from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import DateTime
from app.utils.time import get_vietnam_time

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    permissions = relationship("Permission", secondary=role_permissions, backref="roles")
    created_at = Column(DateTime(timezone=True), default=get_vietnam_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_vietnam_time, onupdate=get_vietnam_time, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
