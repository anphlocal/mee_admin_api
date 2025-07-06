from sqlalchemy import Column, Integer, String
from app.db.database import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from app.utils.time import get_vietnam_time

class Permission(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=get_vietnam_time, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_vietnam_time, onupdate=get_vietnam_time, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
