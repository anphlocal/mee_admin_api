from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.database import Base
from sqlalchemy import DateTime
from app.utils.time import get_vietnam_time

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=get_vietnam_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_vietnam_time, onupdate=get_vietnam_time, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    roles = relationship("Role", secondary=user_roles, backref="users")
