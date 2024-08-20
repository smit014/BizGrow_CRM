from backend.database.database import Base
from sqlalchemy import Column, String, DateTime, Integer,ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from backend.src.resource.user.model import User


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    industry = Column(String, nullable=False)
    country = Column(String, nullable=False)
    country_state = Column(String, nullable=False)
    address = Column(String)
    GST_no = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    users = relationship("UserRole", back_populates="organization")
    invoices = relationship("Invoice", back_populates="organization")
    customer = relationship("Customer", back_populates="organization")
    # reports = relationship("Report", back_populates="organization")
    # forecasts = relationship("Forecast", back_populates="organization")
    # inventory = relationship("Inventory", back_populates="organization")

    # todo: add Base currency support
    # todo: add image logo of business
