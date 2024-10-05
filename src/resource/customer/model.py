# The `Customer` class represents a table in a database with attributes such as id, name, email,
# phone, company name, address, and relationships with Organization and User entities.
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Boolean,BigInteger
from datetime import datetime
from database.database import Base
from sqlalchemy.orm import relationship
from src.resource.organization.model import Organization
from src.resource.user.model import User

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(BigInteger, unique=False, index=True)  # phone can be same in different orgs
    company_name = Column(String, nullable=True, index=True)
    bill_address = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    pincode_no = Column(Integer, nullable=True)
    organization_id = Column(String, ForeignKey('organizations.id'))
    created_by = Column(String, ForeignKey('users.id'))  # Track who created
    status = Column(String, default="Active")  # Active & inactive status
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    # organization = relationship("Organization", back_populates="customers")
    # created_by = relationship("User", back_populates="customers")
    # invoices = relationship("Invoice", back_populates="customer") 
    invoices = relationship("Invoice", back_populates="customer")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at
            # Include other fields as needed
        }