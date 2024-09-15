# The class `UserRole` defines a SQLAlchemy model for user roles within organizations, including
# attributes like role, user ID, organization ID, and timestamps.
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime
from src.resource.user.model import User
from src.resource.organization.model import Organization

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
