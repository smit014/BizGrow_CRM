from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Boolean
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship
from backend.src.resource.organization.model import Organization

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(Integer, unique=True, index=True)
    company_name = Column(String, notnull=False, index=True)
    bill_address = Column(String)
    city = Column(String)
    state = Column(String)
    pincode_no =Column(Integer)
    organization_id = Column(String,ForeignKey(Organization.id),notnull = False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    status = Column(String) #  Active & inactive status

    invoices = relationship("Invoice", back_populates="customer")
    organizations = relationship("Organization", back_populates="customer")