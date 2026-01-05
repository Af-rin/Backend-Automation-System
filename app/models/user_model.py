from sqlalchemy import Boolean, Column, Enum, Integer, String, DateTime, func
from app.connections.db_connector import Base
from app.helpers.enums.enum_config import userRoles

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=False, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(userRoles, name="user_roles_enum"), nullable=False, default='USER')
    is_active = Column(Boolean, nullable=False, default=True)
    last_login = Column(DateTime(timezone=True), nullable=True, default=None)
    access_token = Column(String, nullable=True, default=None)
    created_at = Column(DateTime(timezone=True), default=func.now())  
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
