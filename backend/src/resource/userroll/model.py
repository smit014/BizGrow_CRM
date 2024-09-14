from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from backend.database.database import Base
from datetime import datetime
from backend.src.resource.user.model import User
from backend.src.resource.organization.model import Organization

class UserRole(Base):
    __tablename__ = 'user_roles'

    id = Column(String, primary_key=True, index=True)
    role = Column(String, index=True)  # e.g., "admin", "member"
    user_id = Column(String, ForeignKey(User.id))
    organization_id = Column(String, ForeignKey(Organization.id))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    # Relationships
    # user = relationship("User", back_populates="roles")
    # organization = relationship("Organization", back_populates="users")
