from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(String, primary_key=True, index=True)
    role = Column(String, index=True)  # e.g., "admin", "member"
    user_id = Column(String, ForeignKey('users.id'))
    organization_id = Column(String, ForeignKey('organizations.id'))
    created_at = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="user_roles")
    organization = relationship("Organization", back_populates="user_roles")
