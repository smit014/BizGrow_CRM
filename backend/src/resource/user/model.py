from backend.database.database import Base
from sqlalchemy import Column, String, VARCHAR, Boolean, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True)
    name = Column(VARCHAR(30))
    phone_no = Column(VARCHAR(255))
    email = Column(String(255), nullable=False, unique=True)
    password = Column(VARCHAR(1024), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    organization_id = Column(String, ForeignKey("organizations.id"))

    organization = relationship("Organization", back_populates="users")
    user_roles = relationship("UserRole", back_populates="user")
    invoices = relationship("Invoice", back_populates="user")
    # transactions = relationship("Transaction", back_populates="user")
