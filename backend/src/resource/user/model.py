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
    address = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)

    # Relationships
    # roles = relationship("UserRole", back_populates="user")
    # customers = relationship("Customer", back_populates="created_by")
    # items = relationship("Item", back_populates="creator")
    # invoices = relationship("Invoice", back_populates="creator")


class Subscription(Base):
    __tablename__ = 'subscription'
    id = Column(String,primary_key=True)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.now())